#!/usr/bin/env python3
"""Read-only V5 source overlap audit with a configurable 75% threshold.

Compares exact normalized text chunks across source documents. The score is
Jaccard similarity of unique chunk texts, NOT full-document similarity.
Pairs below threshold are retained as distinct. Never changes Chroma.
"""
import argparse
from collections import defaultdict
import hashlib
import json
import re
from pathlib import Path
import chromadb

DB="/opt/football-data-lab/knowledge/rag/chroma"
COLLECTION="dribbling_tactics_v5_multisource"

def norm(s):
    return re.sub(r"\s+"," ",re.sub(r"[^\w\s]"," ",s.casefold())).strip()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--threshold",type=float,default=.75)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    if not 0<=args.threshold<=1: p.error("threshold must be in [0,1]")
    coll=chromadb.PersistentClient(path=DB).get_collection(COLLECTION)
    result=coll.get(include=["documents","metadatas"])
    sources=defaultdict(set)
    inverted=defaultdict(set)
    for doc,meta in zip(result["documents"],result["metadatas"]):
        source=meta["source_relative"]
        content=norm(meta.get("raw_text") or doc)
        if len(content)<100:continue
        digest=hashlib.sha256(content.encode("utf-8")).hexdigest()
        sources[source].add(digest)
        inverted[digest].add(source)
    pairs=set()
    for group in inverted.values():
        if len(group)>1:
            members=sorted(group)
            pairs.update((a,b) for i,a in enumerate(members) for b in members[i+1:])
    matches=[]
    for a,b in sorted(pairs):
        shared=len(sources[a]&sources[b])
        union=len(sources[a]|sources[b])
        score=shared/union if union else 0
        if score>=args.threshold:
            matches.append({"source_a":a,"source_b":b,"overlap_score":round(score,6),
                            "shared_chunks":shared,"chunks_a":len(sources[a]),"chunks_b":len(sources[b])})
    matches.sort(key=lambda x:(-x["overlap_score"],-x["shared_chunks"],x["source_a"]))
    report={"collection":COLLECTION,"threshold":args.threshold,
            "metric":"Jaccard of normalized unique chunk texts >=100 chars",
            "note":"High overlap is a duplicate candidate, not proof of identical PDF bytes; chunking can understate document similarity.",
            "source_count":len(sources),"candidate_count":len(matches),"candidates":matches}
    print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
        print("REPORT:",args.output,flush=True)
    print("PASS: read-only duplicate audit; V5 unchanged",flush=True)

if __name__=="__main__":main()
