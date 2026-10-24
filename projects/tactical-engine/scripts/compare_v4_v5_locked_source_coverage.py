#!/usr/bin/env python3
"""Compare locked-gold source availability in immutable V4/V5 collections."""
import argparse
import hashlib
import json
from pathlib import Path

import chromadb

DB="/opt/football-data-lab/knowledge/rag/chroma"
V4="dribbling_tactics_v4_qwen3_embedding_06b"
V5="dribbling_tactics_v5_multisource"
EXPECTED_MANIFEST_SHA="c160a8a2128e05eda50842230c5f4aad2bf9a8085f4240c8ee893ed2e3a3fa71"
ALIASES={
    "ussia, le transizioni nel calcio moderno":"Transizioni.Ussia",
    "football-data-lab, le transizioni offensive e difensive":"FOOTBALL_DATA_LAB_Transizioni_Offensive_e_Difensive_Manuale",
    "football-data-lab, ampiezza e cambio gioco":"FOOTBALL_DATA_LAB_Ampiezza_e_Cambio_Gioco_Manuale",
    "foscarini, manovre offensive nei vari sistemi di gioco":"manovre_offensive_vari_sistemi_gioco_Foscarini",
}

def expected_sources(title):
    value=title.casefold()
    return [source for label,source in ALIASES.items() if label in value]

def source_counts(collection):
    result=collection.get(include=["metadatas"])
    counts={}
    for meta in result["metadatas"]:
        source=meta.get("source")
        counts[source]=counts.get(source,0)+1
    return counts

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("manifest",type=Path)
    parser.add_argument("output",type=Path)
    args=parser.parse_args()
    raw=args.manifest.read_bytes(); digest=hashlib.sha256(raw).hexdigest()
    if digest!=EXPECTED_MANIFEST_SHA:
        parser.error(f"manifest hash mismatch: {digest}")
    manifest=json.loads(raw)
    client=chromadb.PersistentClient(path=DB)
    collections={name:client.get_collection(name) for name in (V4,V5)}
    counts={name:source_counts(collection) for name,collection in collections.items()}
    cases=[]
    for item in manifest["questions"]:
        expected=expected_sources(item["source_title"])
        if not expected:
            raise RuntimeError(f"No source mapping for {item['id']}: {item['source_title']}")
        row={"id":item["id"],"expected_sources":expected}
        for name in (V4,V5):
            row[name]={source:counts[name].get(source,0) for source in expected}
            row[name+"_all_sources_present"]=all(counts[name].get(source,0)>0 for source in expected)
        cases.append(row)
    report={
        "manifest_sha256":digest,
        "database":DB,
        "collections":{name:{"count":collections[name].count(),"source_count":len(counts[name])} for name in (V4,V5)},
        "cases":cases,
        "summary":{name:{"cases_with_all_sources":sum(row[name+"_all_sources_present"] for row in cases),"total_cases":len(cases)} for name in (V4,V5)},
        "index_writes":False,
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
