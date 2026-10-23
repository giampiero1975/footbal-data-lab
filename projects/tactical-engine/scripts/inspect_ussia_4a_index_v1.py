#!/usr/bin/env python3
"""Read-only inspection of indexed Ussia 4/A text; no retrieval or generation."""
import json
import re
from pathlib import Path
import chromadb

DB="/opt/football-data-lab/knowledge/rag/chroma"
COLLECTION="dribbling_tactics_v5_multisource"
SOURCE="Transizioni.Ussia"
OUT=Path("projects/tactical-engine/evaluation/ussia_4a_index_inspection_v1.json")
pattern=re.compile(r"(?i)(?:fig(?:ura)?\.?\s*4\s*[/.-]?\s*a\b|esercitazione\s*(?:n\.?\s*)?4\s*[/.-]?\s*a\b|\b4\s*[/.-]\s*a\b)")
coll=chromadb.PersistentClient(path=DB).get_collection(COLLECTION)
before=coll.count()
res=coll.get(where={"source":SOURCE},include=["documents","metadatas"])
items=[]
for cid,doc,meta in zip(res["ids"],res["documents"],res["metadatas"]):
    raw=(meta or {}).get("raw_text") or doc or ""
    hits=[{"offset":m.start(),"context":raw[max(0,m.start()-500):min(len(raw),m.end()+1100)]} for m in pattern.finditer(raw)]
    if hits:
        items.append({"id":cid,"source":meta.get("source"),"pages":meta.get("pages"),"source_relative":meta.get("source_relative"),"matches":hits})
report={"collection":COLLECTION,"source":SOURCE,"count_before":before,"source_chunks":len(res["ids"]),"matched_chunks":len(items),"matches":items,"count_after":coll.count()}
report["index_unchanged"]=report["count_before"]==report["count_after"]
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str),encoding="utf-8")
print(f"SOURCE_CHUNKS={report['source_chunks']} MATCHED_CHUNKS={len(items)} INDEX_UNCHANGED={report['index_unchanged']}")
for item in items:
    print(f"\nID={item['id']} PAGES={item['pages']}")
    for hit in item["matches"]:
        print(hit["context"][:1400])
print(f"REPORT={OUT}")
