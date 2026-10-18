#!/usr/bin/env python3
"""DRIBBLING Tactical Engine: PDF -> Docling Markdown/JSON + PyMuPDF figure PNGs.

Usage: python scripts/ingest_pdfs.py --limit 1
       python scripts/ingest_pdfs.py --force --limit 1
"""
import argparse
import hashlib
import json
import os
import sys
import tempfile
import traceback
from datetime import datetime, timezone
from pathlib import Path

for variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(variable, "1")

ROOT = Path("/opt/football-data-lab")
DEFAULT_SOURCES = ROOT / "knowledge" / "sources"
DEFAULT_PROCESSED = ROOT / "knowledge" / "processed"
PIPELINE_VERSION = 2


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_atomic(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def extract_figures(pdf, structure, base, scale=2.0):
    import pymupdf

    pictures = structure.get("pictures", [])
    output_dir = base.parent / (base.name + "_images")
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = []
    with pymupdf.open(pdf) as doc:
        for index, picture in enumerate(pictures, 1):
            provenance = picture.get("prov") or []
            if not provenance:
                print(f"  [FIG SKIP] {index}: coordinate assenti", flush=True)
                continue
            prov = provenance[0]
            page_no = prov.get("page_no")
            if not isinstance(page_no, int) or not (1 <= page_no <= len(doc)):
                print(f"  [FIG SKIP] {index}: pagina non valida", flush=True)
                continue
            bbox = prov.get("bbox") or {}
            try:
                l, t, r, b = (float(bbox[k]) for k in ("l", "t", "r", "b"))
            except (KeyError, TypeError, ValueError):
                print(f"  [FIG SKIP] {index}: bbox non valido", flush=True)
                continue
            page = doc[page_no - 1]
            origin = bbox.get("coord_origin", "BOTTOMLEFT")
            if origin == "BOTTOMLEFT":
                rect = pymupdf.Rect(l, page.rect.height - t, r, page.rect.height - b)
            elif origin == "TOPLEFT":
                rect = pymupdf.Rect(l, t, r, b)
            else:
                print(f"  [FIG SKIP] {index}: origine {origin} non supportata", flush=True)
                continue
            rect = rect.normalize() & page.rect
            if rect.is_empty or rect.is_infinite:
                print(f"  [FIG SKIP] {index}: ritaglio vuoto", flush=True)
                continue
            filename = f"figure_{index:03d}_page_{page_no:02d}.png"
            output_file = output_dir / filename
            # Existing figures need not be rendered again when backfilling metadata.
            if not output_file.is_file() or output_file.stat().st_size == 0:
                page.get_pixmap(matrix=pymupdf.Matrix(scale, scale), clip=rect, alpha=False).save(str(output_file))
            manifest.append({
                "figure_index": index,
                "self_ref": picture.get("self_ref"),
                "page": page_no,
                "file": filename,
                "bbox": bbox,
                "captions": [c.get("$ref") for c in picture.get("captions", [])],
            })
    write_atomic(output_dir / "images.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    return len(manifest), len(pictures)


def main():
    parser = argparse.ArgumentParser(description="Estrai PDF in Markdown, JSON e immagini")
    parser.add_argument("--sources", type=Path, default=DEFAULT_SOURCES)
    parser.add_argument("--processed", type=Path, default=DEFAULT_PROCESSED)
    parser.add_argument("--limit", type=int, default=None, help="Numero massimo di PDF da elaborare")
    parser.add_argument("--force", action="store_true", help="Rielabora anche PDF invariati")
    args = parser.parse_args()

    sources = args.sources.expanduser().resolve()
    processed = args.processed.expanduser().resolve()
    if not sources.is_dir():
        parser.error(f"Cartella sorgente inesistente: {sources}")
    if args.limit is not None and args.limit < 1:
        parser.error("--limit deve essere maggiore di zero")
    if sources == processed or sources in processed.parents or processed in sources.parents:
        parser.error("Le cartelle sorgente e destinazione devono essere separate")

    pdfs = sorted(p for p in sources.rglob("*") if p.is_file() and p.suffix.lower() == ".pdf")
    if not pdfs:
        print(f"Nessun PDF trovato in {sources}")
        return 0

    processed.mkdir(parents=True, exist_ok=True)
    errors_path = processed / "ingestion_errors.jsonl"
    stats = {"ok": 0, "updated": 0, "skip": 0, "error": 0}
    attempted = 0
    converter = None

    for pdf in pdfs:
        relative = pdf.relative_to(sources)
        base = processed / relative.parent / relative.stem
        markdown_path = base.with_suffix(".md")
        json_path = base.with_suffix(".json")
        meta_path = base.with_suffix(".meta.json")
        try:
            fingerprint = sha256_file(pdf)
            existing = all(p.exists() for p in (markdown_path, json_path, meta_path))
            old_meta = json.loads(meta_path.read_text(encoding="utf-8")) if existing else {}
            same_pdf = existing and old_meta.get("sha256") == fingerprint
            images_index = base.parent / (base.name + "_images") / "images.json"
            already_complete = (
                same_pdf and old_meta.get("pipeline_version") == PIPELINE_VERSION
                and images_index.is_file()
            )
            if not args.force and already_complete:
                stats["skip"] += 1
                print(f"[SKIP] {relative}", flush=True)
                continue
            if args.limit is not None and attempted >= args.limit:
                break
            attempted += 1

            # Upgrade v1 -> v2 without running Docling again for unchanged PDFs.
            if not args.force and same_pdf and old_meta.get("pipeline_version") in (1, 2):
                print(f"[FIGURES] {relative} — riuso JSON esistente", flush=True)
                structure = json.loads(json_path.read_text(encoding="utf-8"))
                count, total = extract_figures(pdf, structure, base)
                old_meta.update({
                    "pipeline_version": PIPELINE_VERSION,
                    "figures_extracted": count,
                    "figures_detected": total,
                    "figures_index": (base.name + "_images/images.json"),
                    "figures_processed_at_utc": utc_now(),
                })
                write_atomic(meta_path, json.dumps(old_meta, ensure_ascii=False, indent=2) + "\n")
                stats["updated"] += 1
                print(f"[UPDATED] {relative} — figure {count}/{total}", flush=True)
                continue

            print(f"[START] {relative}", flush=True)
            if converter is None:
                import torch
                torch.backends.mkldnn.enabled = False
                from docling.document_converter import DocumentConverter
                converter = DocumentConverter()
            document = converter.convert(str(pdf)).document
            markdown = document.export_to_markdown()
            structure = document.export_to_dict()
            # Store the source extraction before figure rendering; a failed render can be retried.
            write_atomic(markdown_path, markdown)
            write_atomic(json_path, json.dumps(structure, ensure_ascii=False, indent=2))
            metadata = {
                "source": relative.as_posix(),
                "sha256": fingerprint,
                "source_size_bytes": pdf.stat().st_size,
                "processed_at_utc": utc_now(),
                "pipeline_version": 1,
                "markdown_characters": len(markdown),
            }
            write_atomic(meta_path, json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
            count, total = extract_figures(pdf, structure, base)
            metadata.update({
                "pipeline_version": PIPELINE_VERSION,
                "figures_extracted": count,
                "figures_detected": total,
                "figures_index": base.name + "_images/images.json",
                "figures_processed_at_utc": utc_now(),
            })
            write_atomic(meta_path, json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
            stats["ok"] += 1
            print(f"[OK] {relative} — {len(markdown)} caratteri, figure {count}/{total}", flush=True)
        except Exception as exc:
            stats["error"] += 1
            record = {
                "source": relative.as_posix(), "at_utc": utc_now(),
                "error": str(exc), "traceback": traceback.format_exc(),
            }
            with errors_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            print(f"[ERROR] {relative}: {exc}", file=sys.stderr, flush=True)

    print(f"Riepilogo: {stats['ok']} nuovi, {stats['updated']} aggiornati, "
          f"{stats['skip']} invariati, {stats['error']} errori")
    return 1 if stats["error"] else 0


if __name__ == "__main__":
    sys.exit(main())
