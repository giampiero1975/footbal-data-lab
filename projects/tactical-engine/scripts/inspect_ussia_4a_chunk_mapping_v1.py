#!/usr/bin/env python3
"""Read-only diagnostic of Ussia 4/A source-to-Chroma chunk mapping; no inference."""
import json
from pathlib import Path
import chromadb

ROOT = Path("/opt/football-data-lab")
SOURCE = ROOT / "knowledge/processed/formations-and-systems/Transizioni.Ussia.json"
DB = ROOT / "knowledge/rag/chroma"
COLLECTION = "dribbling_tactics_v5_multisource"
TARGET = "ece84a07265cfef1078c9fdd42027511dd8d27053d014dfe2b98e49e52c465b6"
NEEDLES = ("esercitazione 4/a", "figura 4/a", "8 contro 8 + 2 portieri", "otto contro otto 2 portieri", "5 secondi")
def main():
    doc = json.loads(SOURCE.read_text(encoding="utf-8"))
    texts = doc.get("texts", [])
    selected = []
    for i, item in enumerate(texts):
        if item.get("self_ref") in ("#/texts/151", "#/texts/152", "#/texts/153", "#/texts/154"):
            selected.append({"ref":item.get("self_ref"),"page":(item.get("prov") or [{}])[0].get("page_no"),"label":item.get("label"),"text":item.get("text")})
    coll = chromadb.PersistentClient(path=str(DB)).get_collection(COLLECTION)
    before = coll.count()
    got = coll.get(where={"source":"Transizioni.Ussia"},include=["documents","metadatas"])
    matches = []
    for cid, txt, meta in zip(got["ids"],got["documents"],got["metadatas"]):
        hits = [x for x in NEEDLES if x in (txt or "").casefold()]
        if hits or cid == TARGET:
            matches.append({"id":cid,"pages":(meta or {}).get("pages"),"metadata":meta,"needles":hits,"text":txt})
    report = {"inspection":"V5-USSIA-4A-MAP-01","source":str(SOURCE),"source_elements":selected,"collection":COLLECTION,"count_before":before,"source_chunks":len(got["ids"]),"matching_chunks":matches,"count_after":coll.count(),"index_unchanged":before==coll.count(),"read_only":True}
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__ == "__main__": main()
