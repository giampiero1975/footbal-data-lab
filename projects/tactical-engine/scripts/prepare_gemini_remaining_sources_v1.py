#!/usr/bin/env python3
"""Build private, read-only source bundles for fresh_02 through fresh_10."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDS = {
    "ussia": "0B6maey1azXc5bUlKVEh4S0JUMjQ",
    "foscarini": "0B6maey1azXc5bUJGaV9rak02WjQ",
    "transizioni": "1ADTvDfyRdq3cUQFMN3WG1a5BwHlBytl8",
    "ampiezza": "1I9JZV2iYj_4XKvq4jH-6bZYwt0vORZ5O",
}
CASES = {
    "fresh_02": [("ussia", 11)],
    "fresh_03": [("transizioni", 4), ("transizioni", 5)],
    "fresh_04": [("ussia", 14)],
    "fresh_05": [("ampiezza", 3), ("ampiezza", 4)],
    "fresh_06": [("ussia", 24)],
    "fresh_07": [("foscarini", 22)],
    "fresh_08": [("foscarini", 22)],
    "fresh_09": [("transizioni", 4)],
    "fresh_10": [("ussia", 17), ("transizioni", 3)],
}

def main():
    ap = argparse.ArgumentParser()
    for key in IDS:
        ap.add_argument("--" + key, type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, default=ROOT / "evaluation")
    args = ap.parse_args()
    import pymupdf
    output = args.output_dir
    destinations = [output / (qid + "_sources.json") for qid in CASES]
    if any(p.exists() for p in destinations):
        raise SystemExit("REFUSING_OVERWRITE_EXISTING_BUNDLE")
    docs, hashes = {}, {}
    for key, sid in IDS.items():
        path = getattr(args, key)
        raw = path.read_bytes()
        hashes[key] = hashlib.sha256(raw).hexdigest()
        pdf = pymupdf.open(stream=raw, filetype="pdf")
        for page_no in sorted({n for rows in CASES.values() for k, n in rows if k == key}):
            matches = []
            for index, page in enumerate(pdf):
                text = page.get_text("text", sort=True).strip()
                if key == "ussia":
                    found = ("Pasquale Ussia Pagina " + str(page_no)) in " ".join(text.split())
                else:
                    found = index + 1 == page_no
                if found:
                    matches.append((index + 1, text))
            if len(matches) != 1 or len(matches[0][1]) < 100:
                raise SystemExit("PAGE_NOT_VERIFIED: " + key + " " + str(page_no))
            pdf_index, text = matches[0]
            docs[(key, page_no)] = {
                "source_file_id": sid,
                "source_title": path.name,
                "origin_url": "https://drive.google.com/file/d/" + sid + "/view",
                "page": str(page_no),
                "pdf_page_index": pdf_index,
                "text": text,
            }
    for qid, pages in CASES.items():
        payload = {
            "question_id": qid,
            "source_pdf_sha256_by_id": {IDS[k]: hashes[k] for k, _ in pages},
            "documents": [docs[(k, n)] for k, n in pages],
        }
        target = output / (qid + "_sources.json")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        target.chmod(0o600)
        print("PREPARED", qid, target)
    print("API_REQUESTS=0; verify printed page labels manually before reviewer approval")

if __name__ == "__main__":
    main()
