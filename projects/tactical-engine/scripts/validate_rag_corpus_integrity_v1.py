#!/usr/bin/env python3
"""Validate a RAG corpus provenance manifest against isolated offline inputs.

The validator is standard-library only.  It reads a declarative manifest,
ordinary files below an input root and a JSON export of Chroma records.  It
does not import Chroma, Ollama or an embedding model and exposes no mutating
collection operations.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "rag_corpus_integrity_manifest_v1"
SNAPSHOT_SCHEMA_VERSION = "rag_chroma_snapshot_v1"
REPORT_SCHEMA_VERSION = "rag_corpus_integrity_report_v1"
CANONICALIZATION = "RFC 8785 restricted profile"
SHA256_CHARS = frozenset("0123456789abcdef")
VERIFICATION_STATUSES = {
    "verified", "declared", "not_accessible", "not_declared", "mismatch"
}
IDENTITY_BASES = {
    "current_verified", "historically_verified", "declared_only", "none"
}
INVENTORY_COMPLETENESS = {"complete", "partial", "unknown"}
SUPPORTED_CHUNKER_VERSIONS = {
    # Support here means that the manifest/snapshot contract is understood.
    # Byte-for-byte chunk reconstruction remains a separate adapter concern.
    "rag-v5-docling-hybrid-v1",
    "synthetic-fixture-v1",
}
MUTATING_METHODS = ("add", "upsert", "update", "delete", "create_collection")


def _load_gold_canonicalizer() -> Any:
    path = Path(__file__).with_name("validate_relational_gold_preparation_v2.py")
    spec = importlib.util.spec_from_file_location("_gold_v2_canonicalizer", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("GOLD_V2_CANONICALIZER_UNAVAILABLE")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_GOLD = _load_gold_canonicalizer()
canonicalize_rfc8785 = _GOLD.canonicalize_rfc8785
sha256_document = _GOLD.sha256_document


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: root must be an object")
    return value


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _is_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(char in SHA256_CHARS for char in value)
    )


def _safe_relative(root: Path, value: Any) -> Path | None:
    if not isinstance(value, str) or not value:
        return None
    relative = Path(value)
    if relative.is_absolute():
        return None
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None
    return candidate


def _anomaly(
    code: str,
    *,
    document_id: str | None = None,
    source_ref: str | None = None,
    chunk_id: str | None = None,
    record_id: str | None = None,
    detail: str,
) -> dict[str, Any]:
    return {
        "code": code,
        "document_id": document_id,
        "source_ref": source_ref,
        "chunk_id": chunk_id,
        "record_id": record_id,
        "detail": detail,
    }


def _anomaly_key(item: dict[str, Any]) -> tuple[str, ...]:
    return tuple(str(item.get(key) or "") for key in (
        "code", "document_id", "source_ref", "chunk_id", "record_id", "detail"
    ))


def normatively_order(value: Any) -> Any:
    """Deep-copy and sort only arrays defined as set-like by this contract."""
    document = copy.deepcopy(value)

    def visit(node: Any) -> None:
        if isinstance(node, dict):
            for child in node.values():
                visit(child)
            documents = node.get("documents")
            if isinstance(documents, list):
                documents.sort(key=lambda item: (
                    str(item.get("document_id") or ""),
                    str(item.get("source_ref") or ""),
                ) if isinstance(item, dict) else ("", str(item)))
            chunks = node.get("chunks")
            if isinstance(chunks, list):
                chunks.sort(key=lambda item: str(item.get("chunk_id") or "") if isinstance(item, dict) else str(item))
            anomalies = node.get("anomalies")
            if isinstance(anomalies, list):
                anomalies.sort(key=lambda item: _anomaly_key(item) if isinstance(item, dict) else (str(item),))
            records = node.get("records")
            if isinstance(records, list):
                records.sort(key=lambda item: str(item.get("id") or "") if isinstance(item, dict) else str(item))
            available = node.get("available_document_ids")
            if isinstance(available, list):
                available.sort(key=str)
        elif isinstance(node, list):
            for child in node:
                visit(child)

    visit(document)
    return document


def technical_hash(verified_content: dict[str, Any]) -> str:
    return sha256_document(normatively_order(verified_content))


def manifest_hash(manifest: dict[str, Any]) -> str:
    payload = copy.deepcopy(manifest)
    payload.pop("manifest_sha256", None)
    return sha256_document(normatively_order(payload))


def validate_manifest_contract(manifest: dict[str, Any]) -> list[str]:
    """Validate invariants needed by the verifier without external packages."""
    errors: list[str] = []
    required = {
        "schema_version", "manifest_version", "snapshot_id", "snapshot_kind",
        "canonicalization", "collection", "documents",
    }
    missing = sorted(required - set(manifest))
    errors.extend(f"MANIFEST_REQUIRED_FIELD_MISSING:{name}" for name in missing)
    if manifest.get("schema_version") != SCHEMA_VERSION:
        errors.append("MANIFEST_SCHEMA_VERSION_UNSUPPORTED")
    if manifest.get("canonicalization") != CANONICALIZATION:
        errors.append("MANIFEST_CANONICALIZATION_UNSUPPORTED")
    if not isinstance(manifest.get("documents"), list):
        errors.append("MANIFEST_DOCUMENTS_NOT_ARRAY")
        return sorted(errors)

    collection = manifest.get("collection")
    if not isinstance(collection, dict):
        errors.append("MANIFEST_COLLECTION_MISSING")
        return sorted(errors)
    if collection.get("inventory_completeness") not in INVENTORY_COMPLETENESS:
        errors.append("INVENTORY_COMPLETENESS_INVALID")
    if collection.get("inventory_completeness") == "complete" and not collection.get("inventory_completeness_evidence_ref"):
        errors.append("INVENTORY_COMPLETENESS_EVIDENCE_MISSING")
    snapshot = collection.get("snapshot_consistency")
    if not isinstance(snapshot, dict) or snapshot.get("status") not in {"certifiable", "not_certifiable"}:
        errors.append("SNAPSHOT_CONSISTENCY_INVALID")
    elif snapshot.get("status") == "certifiable" and (not snapshot.get("method") or not snapshot.get("evidence_ref")):
        errors.append("SNAPSHOT_CONSISTENCY_EVIDENCE_MISSING")

    document_ids: set[str] = set()
    source_refs: set[str] = set()
    chunk_ids: set[str] = set()
    for index, document in enumerate(manifest["documents"]):
        if not isinstance(document, dict):
            errors.append(f"DOCUMENT_NOT_OBJECT:{index}")
            continue
        source_ref = document.get("source_ref")
        if not isinstance(source_ref, str) or not source_ref:
            errors.append(f"DOCUMENT_SOURCE_REF_MISSING:{index}")
            source_ref = f"<index:{index}>"
        elif source_ref in source_refs:
            errors.append(f"DOCUMENT_SOURCE_REF_DUPLICATE:{source_ref}")
        source_refs.add(source_ref)
        identity = document.get("identity_evidence")
        document_id = document.get("document_id")
        if not isinstance(identity, dict) or identity.get("basis") not in IDENTITY_BASES:
            errors.append(f"DOCUMENT_IDENTITY_EVIDENCE_INVALID:{source_ref}")
            basis = None
        else:
            basis = identity.get("basis")
        if basis in {"current_verified", "historically_verified"}:
            if not isinstance(document_id, str) or not document_id.startswith("sha256:") or not _is_sha256(document_id[7:]):
                errors.append(f"DOCUMENT_VERIFIED_ID_MISSING:{source_ref}")
            if basis == "historically_verified" and (not identity.get("evidence_ref") or not _is_sha256(identity.get("evidence_sha256"))):
                errors.append(f"DOCUMENT_HISTORICAL_EVIDENCE_MISSING:{source_ref}")
        elif document_id is not None:
            errors.append(f"DOCUMENT_UNVERIFIED_ID_PROMOTED:{source_ref}")
        if isinstance(document_id, str):
            if document_id in document_ids:
                errors.append(f"DOCUMENT_ID_DUPLICATE:{document_id}")
            document_ids.add(document_id)

        for artifact_name in ("original", "extraction"):
            artifact = document.get(artifact_name)
            if not isinstance(artifact, dict):
                errors.append(f"DOCUMENT_ARTIFACT_MISSING:{source_ref}:{artifact_name}")
                continue
            if artifact.get("verification_status") not in VERIFICATION_STATUSES:
                errors.append(f"DOCUMENT_ARTIFACT_STATUS_INVALID:{source_ref}:{artifact_name}")
            digest = artifact.get("sha256")
            if digest is not None and not _is_sha256(digest):
                errors.append(f"DOCUMENT_ARTIFACT_HASH_INVALID:{source_ref}:{artifact_name}")

        chunks = document.get("chunks")
        if not isinstance(chunks, list):
            errors.append(f"DOCUMENT_CHUNKS_NOT_ARRAY:{source_ref}")
            continue
        for chunk in chunks:
            if not isinstance(chunk, dict):
                errors.append(f"CHUNK_NOT_OBJECT:{source_ref}")
                continue
            chunk_id = chunk.get("chunk_id")
            if not isinstance(chunk_id, str) or not chunk_id:
                errors.append(f"CHUNK_ID_MISSING:{source_ref}")
                continue
            if chunk_id in chunk_ids:
                errors.append(f"CHUNK_ID_DUPLICATE:{chunk_id}")
            chunk_ids.add(chunk_id)
            if not _is_sha256(chunk.get("content_sha256")):
                errors.append(f"CHUNK_CONTENT_HASH_INVALID:{chunk_id}")
            if not _is_sha256(chunk.get("metadata_sha256")):
                errors.append(f"CHUNK_METADATA_HASH_INVALID:{chunk_id}")
            extraction_path = document.get("extraction", {}).get("relative_path")
            if extraction_path and chunk.get("source_relative") != extraction_path:
                errors.append(f"CHUNK_EXTRACTION_LINK_MISMATCH:{chunk_id}")
    return sorted(errors)


class ReadOnlySnapshotAdapter:
    """Minimal adapter for an exported JSON snapshot; mutation always fails."""

    def __init__(self, snapshot: dict[str, Any]):
        if snapshot.get("schema_version") != SNAPSHOT_SCHEMA_VERSION:
            raise ValueError("SNAPSHOT_SCHEMA_VERSION_UNSUPPORTED")
        records = snapshot.get("records")
        if not isinstance(records, list):
            raise ValueError("SNAPSHOT_RECORDS_NOT_ARRAY")
        self._snapshot = copy.deepcopy(snapshot)

    @property
    def collection_name(self) -> str | None:
        return self._snapshot.get("collection_name")

    def count(self) -> int:
        return len(self._snapshot["records"])

    def records(self) -> list[dict[str, Any]]:
        return copy.deepcopy(self._snapshot["records"])

    def get(self, record_id: str) -> dict[str, Any] | None:
        for record in self._snapshot["records"]:
            if record.get("id") == record_id:
                return copy.deepcopy(record)
        return None

    @staticmethod
    def _refuse() -> None:
        raise RuntimeError("READ_ONLY_ADAPTER_MUTATION_REFUSED")

    add = upsert = update = delete = create_collection = _refuse


def _verify_artifact(
    root: Path,
    document: dict[str, Any],
    artifact_name: str,
    anomalies: list[dict[str, Any]],
) -> None:
    artifact = document[artifact_name]
    source_ref = document.get("source_ref")
    document_id = document.get("document_id")
    path = _safe_relative(root, artifact.get("relative_path"))
    if path is None:
        anomalies.append(_anomaly(
            "NOT_DECLARED", document_id=document_id, source_ref=source_ref,
            detail=f"{artifact_name}: relative path missing or unsafe",
        ))
        return
    if not path.is_file():
        anomalies.append(_anomaly(
            "NOT_ACCESSIBLE", document_id=document_id, source_ref=source_ref,
            detail=f"{artifact_name}: file not accessible",
        ))
        return
    expected = artifact.get("sha256")
    if not _is_sha256(expected):
        anomalies.append(_anomaly(
            "NOT_DECLARED", document_id=document_id, source_ref=source_ref,
            detail=f"{artifact_name}: sha256 not declared",
        ))
        return
    actual = sha256_file(path)
    if actual != expected:
        anomalies.append(_anomaly(
            "MISMATCH", document_id=document_id, source_ref=source_ref,
            detail=f"{artifact_name}: sha256 mismatch",
        ))
    expected_size = artifact.get("size_bytes")
    if isinstance(expected_size, int) and path.stat().st_size != expected_size:
        anomalies.append(_anomaly(
            "MISMATCH", document_id=document_id, source_ref=source_ref,
            detail=f"{artifact_name}: size mismatch",
        ))
    if artifact_name == "original" and document.get("identity_evidence", {}).get("basis") == "current_verified":
        if document_id != f"sha256:{actual}":
            anomalies.append(_anomaly(
                "MISMATCH", document_id=document_id, source_ref=source_ref,
                detail="original: document_id does not match current bytes",
            ))


def verify_integrity(
    manifest: dict[str, Any],
    snapshot: dict[str, Any],
    input_root: Path,
    *,
    generated_at: str | None = None,
) -> dict[str, Any]:
    started = time.monotonic()
    anomalies: list[dict[str, Any]] = []
    for error in validate_manifest_contract(manifest):
        anomalies.append(_anomaly("METADATA_INCOMPLETE", detail=error))
    declared_manifest_hash = manifest.get("manifest_sha256")
    if declared_manifest_hash is not None:
        if not _is_sha256(declared_manifest_hash):
            anomalies.append(_anomaly(
                "METADATA_INCOMPLETE", detail="manifest_sha256 is invalid"
            ))
        elif declared_manifest_hash != manifest_hash(manifest):
            anomalies.append(_anomaly("MISMATCH", detail="manifest_sha256 mismatch"))

    collection = manifest.get("collection", {}) if isinstance(manifest.get("collection"), dict) else {}
    chunker_version = collection.get("chunker_version")
    if chunker_version not in SUPPORTED_CHUNKER_VERSIONS:
        anomalies.append(_anomaly(
            "UNSUPPORTED_VERSION", detail=f"chunker_version={chunker_version!r}"
        ))
    consistency = collection.get("snapshot_consistency", {})
    if consistency.get("status") != "certifiable":
        anomalies.append(_anomaly(
            "SNAPSHOT_NOT_CERTIFIABLE",
            detail="snapshot lacks documented consistent acquisition",
        ))

    adapter = ReadOnlySnapshotAdapter(snapshot)
    if adapter.collection_name != collection.get("name"):
        anomalies.append(_anomaly(
            "MISMATCH", detail="snapshot collection name differs from manifest"
        ))

    documents = manifest.get("documents", []) if isinstance(manifest.get("documents"), list) else []
    expected: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    for document in documents:
        if not isinstance(document, dict) or not isinstance(document.get("chunks"), list):
            continue
        if isinstance(document.get("original"), dict):
            _verify_artifact(input_root, document, "original", anomalies)
        if isinstance(document.get("extraction"), dict):
            _verify_artifact(input_root, document, "extraction", anomalies)
        basis = document.get("identity_evidence", {}).get("basis")
        if basis == "declared_only":
            anomalies.append(_anomaly(
                "NOT_DECLARED", source_ref=document.get("source_ref"),
                detail="declared hash is not a verified document identity",
            ))
        for chunk in document["chunks"]:
            if isinstance(chunk, dict) and isinstance(chunk.get("chunk_id"), str):
                expected.setdefault(chunk["chunk_id"], (document, chunk))

    actual_records = adapter.records()
    actual: dict[str, dict[str, Any]] = {}
    for record in actual_records:
        record_id = record.get("id") if isinstance(record, dict) else None
        if not isinstance(record_id, str) or not record_id:
            anomalies.append(_anomaly("METADATA_INCOMPLETE", detail="snapshot record id missing"))
            continue
        if record_id in actual:
            anomalies.append(_anomaly(
                "METADATA_INCOMPLETE", record_id=record_id,
                detail="duplicate record id in snapshot",
            ))
        actual.setdefault(record_id, record)

    expected_ids = set(expected)
    actual_ids = set(actual)
    for chunk_id in sorted(expected_ids - actual_ids):
        document, _ = expected[chunk_id]
        anomalies.append(_anomaly(
            "MISSING_RECORD", document_id=document.get("document_id"),
            source_ref=document.get("source_ref"), chunk_id=chunk_id,
            detail="expected chunk absent from snapshot",
        ))
    extra_code = "ORPHAN_RECORD" if collection.get("inventory_completeness") == "complete" else "UNRECONCILED_RECORD"
    for record_id in sorted(actual_ids - expected_ids):
        anomalies.append(_anomaly(
            extra_code, record_id=record_id,
            detail="snapshot record is outside manifest inventory",
        ))

    matched_chunk_ids: set[str] = set()
    content_groups: dict[str, list[str]] = defaultdict(list)
    required_metadata = {"source_relative", "page_numbers", "headings"}
    for record_id, record in actual.items():
        stored_document = record.get("document")
        metadata = record.get("metadata")
        if isinstance(stored_document, str):
            content_groups[sha256_bytes(stored_document.encode("utf-8"))].append(record_id)
        if record_id not in expected:
            continue
        document, chunk = expected[record_id]
        record_ok = True
        if not isinstance(stored_document, str):
            anomalies.append(_anomaly(
                "METADATA_INCOMPLETE", document_id=document.get("document_id"),
                source_ref=document.get("source_ref"), chunk_id=record_id,
                record_id=record_id, detail="stored document missing",
            ))
            record_ok = False
        elif sha256_bytes(stored_document.encode("utf-8")) != chunk.get("content_sha256"):
            anomalies.append(_anomaly(
                "MISMATCH", document_id=document.get("document_id"),
                source_ref=document.get("source_ref"), chunk_id=record_id,
                record_id=record_id, detail="stored document hash mismatch",
            ))
            record_ok = False
        if not isinstance(metadata, dict):
            anomalies.append(_anomaly(
                "METADATA_INCOMPLETE", document_id=document.get("document_id"),
                source_ref=document.get("source_ref"), chunk_id=record_id,
                record_id=record_id, detail="metadata missing",
            ))
            record_ok = False
        else:
            missing_fields = sorted(required_metadata - set(metadata))
            if missing_fields:
                anomalies.append(_anomaly(
                    "METADATA_INCOMPLETE", document_id=document.get("document_id"),
                    source_ref=document.get("source_ref"), chunk_id=record_id,
                    record_id=record_id,
                    detail=f"metadata fields missing: {','.join(missing_fields)}",
                ))
                record_ok = False
            if sha256_document(metadata) != chunk.get("metadata_sha256"):
                anomalies.append(_anomaly(
                    "MISMATCH", document_id=document.get("document_id"),
                    source_ref=document.get("source_ref"), chunk_id=record_id,
                    record_id=record_id, detail="metadata hash mismatch",
                ))
                record_ok = False
        if record_ok:
            matched_chunk_ids.add(record_id)

    declared_ids_hash = collection.get("sorted_record_ids_sha256")
    if declared_ids_hash is not None:
        actual_ids_hash = sha256_document(sorted(actual_ids))
        if declared_ids_hash != actual_ids_hash:
            anomalies.append(_anomaly(
                "MISMATCH", detail="sorted_record_ids_sha256 mismatch"
            ))

    for digest, ids in sorted(content_groups.items()):
        if len(ids) > 1:
            anomalies.append(_anomaly(
                "DUPLICATE_CONTENT", record_id=sorted(ids)[0],
                detail=f"content_sha256={digest}; ids={','.join(sorted(ids))}",
            ))

    declared_count = collection.get("record_count")
    if isinstance(declared_count, int) and declared_count != adapter.count():
        anomalies.append(_anomaly(
            "MISMATCH", detail=f"record count declared={declared_count} actual={adapter.count()}"
        ))

    available_document_ids: list[str] = []
    for document in documents:
        if not isinstance(document, dict):
            continue
        ids = {
            chunk.get("chunk_id") for chunk in document.get("chunks", [])
            if isinstance(chunk, dict)
        }
        if ids & matched_chunk_ids:
            available_document_ids.append(document.get("document_id") or document.get("source_ref"))

    anomalies.sort(key=_anomaly_key)
    counts: dict[str, int] = defaultdict(int)
    for anomaly in anomalies:
        counts[anomaly["code"]] += 1
    verified_content = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "manifest_schema_version": manifest.get("schema_version"),
        "snapshot_id": manifest.get("snapshot_id"),
        "collection_name": collection.get("name"),
        "inventory_completeness": collection.get("inventory_completeness"),
        "snapshot_certifiability": consistency.get("status", "not_certifiable"),
        "integrity_status": "verified" if not anomalies else "not_verified",
        "expected_record_count": len(expected_ids),
        "actual_record_count": len(actual_ids),
        "available_document_ids": sorted(available_document_ids),
        "anomaly_counts": dict(sorted(counts.items())),
        "anomalies": anomalies,
    }
    ordered_content = normatively_order(verified_content)
    timestamp = generated_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return {
        "verified_content": ordered_content,
        "verified_content_sha256": technical_hash(ordered_content),
        "run_metadata": {
            "generated_at": timestamp,
            "elapsed_ms": int((time.monotonic() - started) * 1000),
            "tool": "validate_rag_corpus_integrity_v1.py",
            "canonicalization": CANONICALIZATION,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--input-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--run-timestamp")
    args = parser.parse_args()
    for path in (args.manifest, args.snapshot):
        if not path.is_file():
            parser.error(f"input not found: {path}")
    if not args.input_root.is_dir():
        parser.error(f"input root not found: {args.input_root}")
    if args.output.exists():
        parser.error(f"refusing overwrite: {args.output}")
    output_resolved = args.output.resolve()
    if output_resolved in {args.manifest.resolve(), args.snapshot.resolve()}:
        parser.error("output must be separate from inputs")

    report = verify_integrity(
        load_json(args.manifest), load_json(args.snapshot), args.input_root,
        generated_at=args.run_timestamp,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(args.output)
    print(f"REPORT {args.output}")
    print(f"STATUS {report['verified_content']['integrity_status']}")
    print(f"TECHNICAL_SHA256 {report['verified_content_sha256']}")
    return 0 if report["verified_content"]["integrity_status"] == "verified" else 3


if __name__ == "__main__":
    raise SystemExit(main())
