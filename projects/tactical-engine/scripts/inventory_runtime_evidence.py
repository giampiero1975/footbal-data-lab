#!/usr/bin/env python3
"""Inventory untracked runtime JSON evidence without reading content into Git."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def classify(relative: str) -> str:
    lowered = relative.lower()
    if "gemini" in lowered or "source" in Path(relative).name.lower():
        return "restricted_review"
    if any(token in lowered for token in ("integrated_candidate_full_v2", "runtime_fingerprint_v2", "default_promotion_smoke", "v4_v5_locked_source_coverage")):
        return "certification_evidence"
    if "/reports/" in lowered or "benchmark" in lowered or "audit" in lowered:
        return "historical_evidence"
    return "diagnostic_evidence"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    raw = subprocess.check_output(
        ["git", "ls-files", "--others", "--exclude-standard", "-z"],
        cwd=repo,
    )
    entries = []
    for relative in sorted(filter(None, raw.decode().split("\0"))):
        if "/.venv" in relative or not relative.endswith(".json"):
            continue
        path = repo / relative
        entries.append({
            "path": relative,
            "bytes": path.stat().st_size,
            "sha256": digest(path),
            "classification": classify(relative),
        })
    counts: dict[str, int] = {}
    for entry in entries:
        key = entry["classification"]
        counts[key] = counts.get(key, 0) + 1
    report = {
        "schema": "runtime-evidence-manifest-v1",
        "entry_count": len(entries),
        "total_bytes": sum(item["bytes"] for item in entries),
        "classification_counts": dict(sorted(counts.items())),
        "entries": entries,
        "policy": "Preserve on VPS; do not publish report contents without privacy review.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
