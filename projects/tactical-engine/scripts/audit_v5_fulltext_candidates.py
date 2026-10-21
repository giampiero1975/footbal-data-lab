#!/usr/bin/env python3
"""Audit V5 candidate duplicate sources against complete Docling text (read-only).

Threshold is applied to normalized full-document token shingles (5 words).
No source, PDF, or Chroma records are modified. Output JSON is optional.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT=Path("/opt/football-data-lab")
PROCESSED=ROOT/"knowledge/processed"
CANDIDATES=[
 ("formations-and-systems/Allegati_222010155625.json","formations-and-systems/LA TECNICA APPLICATA COME PRESUPPOSTO DEL GIOCO COLLETTIVO.json"),
 ("formations-and-systems/Allegati_45201211489.json","formations-and-systems/Conseiderazione sul sistema di gioco 4-3-2-1.json"),
 ("formations-and-systems/Allegati_71201095736.json","formations-and-systems/IL CONCETTO DI MARCAMENTO NELLA DIFESA AD UOMO E A ZONA.json"),
 ("formations-and-systems/Categoria_Tattiche del calcio - Wikipedia(1).json","formations-and-systems/Categoria_Tattiche del calcio - Wikipedia.json"),
 ("formations-and-systems/La Tattica nel Calcio _ 4-5-1.json","formations-and-systems/La Tattica nel Calcio _ 5-4-1.json"),
]

def normalize(s):
    return re.sub(r"\s+"," ",re.sub(r"[^\w\s]"," ",s.casefold())).strip()

def read_text(relative):
    from docling_core.types.doc import DoclingDocument
    doc=DoclingDocument.model_validate_json((PROCESSED/relative).read_text(encoding="utf-8"))
    return normalize(doc.export_to_text())

def shingles(words,n=5):
    return set(tuple(words[i:i+n]) for i in range(len(words)-n+1))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--threshold",type=float,default=.75)
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    if not 0<=args.threshold<=1:ap.error("threshold must be in [0,1]")
    results=[]
    for a,b in CANDIDATES:
        ta,tb=read_text(a),read_text(b)
        wa,wb=ta.split(),tb.split()
        sa,sb=shingles(wa),shingles(wb)
        union=len(sa|sb)
        score=len(sa&sb)/union if union else None
        same=ta==tb
        row={"source_a":a,"source_b":b,"words_a":len(wa),"words_b":len(wb),
             "full_text_equal":same,"shingle_jaccard":round(score,5) if score is not None else None,
             "shingles_a":len(sa),"shingles_b":len(sb),
             "above_threshold":bool(score is not None and score>=args.threshold),
             "text_sha256_a":hashlib.sha256(ta.encode()).hexdigest(),
             "text_sha256_b":hashlib.sha256(tb.encode()).hexdigest()}
        results.append(row)
        print(json.dumps(row,ensure_ascii=False),flush=True)
    report={"metric":"5-word shingle Jaccard of normalized full Docling export_to_text",
            "threshold":args.threshold,"note":"Textual identity is not PDF byte identity; short documents require review.",
            "results":results}
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
        print("REPORT:",args.output,flush=True)
    print("PASS: full-text audit completed; original V5 untouched.",flush=True)

if __name__=="__main__":main()
