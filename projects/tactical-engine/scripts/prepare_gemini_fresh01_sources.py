#!/usr/bin/env python3
"""Prepare private page-labelled source bundle from original Ussia PDF (no API calls)."""
import argparse
import hashlib
import json
from pathlib import Path

SOURCE_ID = "0B6maey1azXc5bUlKVEh4S0JUMjQ"
SOURCE_URL = "https://drive.google.com/file/d/" + SOURCE_ID + "/view"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pdf", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if args.output.exists():
        raise SystemExit("REFUSING_OVERWRITE")
    try:
        import fitz
    except ImportError:
        raise SystemExit("MISSING_DEPENDENCY: install PyMuPDF in a dedicated venv")
    pdfbytes = args.pdf.read_bytes()
    doc = fitz.open(stream=pdfbytes, filetype="pdf")
    pages = []
    for page in doc:
        text = page.get_text("text", sort=True)
        for num in (21, 22, 23):
            # Use page's printed heading, not an assumed PDF page index.
            if ("Pasquale Ussia Pagina " + str(num)) in " ".join(text.split()):
                pages.append({"source_file_id": SOURCE_ID,
                    "source_title": "Transizioni.Ussia. Master Allenatore PRO.pdf",
                    "origin_url": SOURCE_URL,
                    "page": str(num), "text": text.strip()})
    found = sorted(x["page"] for x in pages)
    if found != ["21", "22", "23"]:
        raise SystemExit("SOURCE_PAGES_MISSING_OR_DUPLICATED: " + str(found))
    if any(len(x["text"]) < 100 for x in pages):
        raise SystemExit("SOURCE_TEXT_TOO_SHORT")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"question_id": "fresh_01",
        "source_pdf_sha256": hashlib.sha256(pdfbytes).hexdigest(),
        "documents": pages}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.output.chmod(0o600)
    print("SOURCE_BUNDLE_PREPARED", args.output, "PAGES", ",".join(found))
    print("PDF_SHA256", hashlib.sha256(pdfbytes).hexdigest())

if __name__ == "__main__":
    main()
