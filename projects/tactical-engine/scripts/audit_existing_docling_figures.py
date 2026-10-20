"""Read-only audit of already-processed Docling JSON and image manifests.

No imports of Docling, no PDF conversion, no index writes.
"""
import argparse
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--processed", type=Path, default=Path("/opt/football-data-lab/knowledge/processed"))
    args = parser.parse_args()
    root = args.processed.resolve()
    if not root.is_dir():
        parser.error("Processed directory not found: " + str(root))
    rows = []
    for meta in sorted(root.rglob("*.meta.json")):
        try:
            data = json.loads(meta.read_text(encoding="utf-8"))
            stem = meta.name[:-len(".meta.json")]
            doc = meta.with_name(stem + ".json")
            manifest = meta.with_name(stem + "_images") / "images.json"
            structure = json.loads(doc.read_text(encoding="utf-8")) if doc.is_file() else {}
            images = json.loads(manifest.read_text(encoding="utf-8")) if manifest.is_file() else []
            rows.append({
                "source": data.get("source"),
                "pipeline_version": data.get("pipeline_version"),
                "docling_pictures": len(structure.get("pictures", [])),
                "manifest_figures": len(images),
                "figures_detected_metadata": data.get("figures_detected"),
                "figures_extracted_metadata": data.get("figures_extracted"),
                "missing_structure": not doc.is_file(),
                "missing_manifest": not manifest.is_file(),
            })
        except (OSError, ValueError, TypeError) as exc:
            rows.append({"metadata_file": str(meta.relative_to(root)), "error": str(exc)})
    print(json.dumps({"processed": str(root), "documents": len(rows), "results": rows}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
