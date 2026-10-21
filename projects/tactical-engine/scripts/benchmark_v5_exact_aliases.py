#!/usr/bin/env python3
"""Read-only A/B test: V5 reranking with exact-document alias collapsing.

Only the four verified full-text-identical pairs are collapsed. Similar but
non-identical 4-5-1 and 5-4-1 remain separate. No Chroma modifications.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import chromadb
from llama_index.embeddings.ollama import OllamaEmbedding
from sentence_transformers import CrossEncoder

DB="/opt/football-data-lab/knowledge/rag/chroma"
COLLECTION="dribbling_tactics_v5_multisource"
ALIASES=[
 ("Allegati_222010155625","LA TECNICA APPLICATA COME PRESUPPOSTO DEL GIOCO COLLETTIVO"),
 ("Allegati_45201211489","Conseiderazione sul sistema di gioco 4-3-2-1"),
 ("Allegati_71201095736","IL CONCETTO DI MARCAMENTO NELLA DIFESA AD UOMO E A ZONA"),
 ("Categoria_Tattiche del calcio - Wikipedia(1)","Categoria_Tattiche del calcio - Wikipedia"),
]
CANONICAL={alias:canonical for alias,canonical in ALIASES}
QUESTIONS=[
 "Come affrontare con il 4-4-2 una squadra schierata con il 3-4-1-2?",
 "Come creare superiorità numerica in fase di possesso palla?",
 "Quali principi favoriscono la verticalizzazione nella fase offensiva?",
 "Come sfruttare i triangoli per sviluppare il gioco di squadra?",
 "Quali vantaggi e rischi comporta variare il sistema di gioco durante una partita?",
]
def collapse(rows,k=8):
    selected=[];seen=set()
    for row in rows:
        canonical=CANONICAL.get(row["source"],row["source"])
        # Exact source alias collapse: suppress identical chunks across copies,
        # but retain distinct passages from a source.
        key=(canonical,row["normalized"])
        if key in seen:continue
        seen.add(key)
        selected.append({key:value for key,value in row.items() if key!="normalized"} |
                        {"canonical_source":canonical})
        if len(selected)==k:break
    return selected
def summarize(rows):
    return {"unique_source_names":len(set(r["source"] for r in rows)),
            "unique_canonical_sources":len(set(CANONICAL.get(r["source"],r["source"]) for r in rows)),
            "sources":dict(Counter(r["source"] for r in rows)),
            "top":[{"id":r["id"][:12],"source":r["source"],"canonical_source":CANONICAL.get(r["source"],r["source"]),
                    "pages":r["pages"],"distance":r["distance"]} for r in rows]}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    coll=chromadb.PersistentClient(path=DB).get_collection(COLLECTION)
    if coll.count()!=5319:raise RuntimeError("V5 size changed; abort")
    embed=OllamaEmbedding(model_name="qwen3-embedding:0.6b",base_url="http://127.0.0.1:11434")
    rerank=CrossEncoder("cross-encoder/mmarco-mMiniLMv2-L12-H384-v1",device="cpu",max_length=512)
    report={"collection":COLLECTION,"index_unchanged":True,"aliases":ALIASES,"queries":[]}
    for q in QUESTIONS:
        vector=embed.get_query_embedding(q)
        result=coll.query(query_embeddings=[vector],n_results=24,include=["documents","metadatas","distances"])
        rows=[]
        for cid,doc,meta,dist in zip(result["ids"][0],result["documents"][0],result["metadatas"][0],result["distances"][0]):
            import hashlib,re
            normalized=re.sub(r"\s+"," ",re.sub(r"[^\w\s]"," ",(meta.get("raw_text") or doc).casefold())).strip()
            rows.append({"id":cid,"source":meta["source"],"pages":meta.get("page_numbers"),
                         "distance":round(float(dist),5),"text":doc,"normalized":hashlib.sha256(normalized.encode()).hexdigest()})
        scores=rerank.predict([(q,r["text"]) for r in rows],batch_size=1,show_progress_bar=False)
        ordered=[rows[i] for i in sorted(range(len(rows)),key=lambda i:float(scores[i]),reverse=True)]
        before=ordered[:8]
        after=collapse(ordered,8)
        entry={"question":q,"before":summarize(before),"after":summarize(after),
               "removed_alias_chunks_from_top8":sum(1 for r in before if r["id"] not in {a["id"] for a in after})}
        report["queries"].append(entry)
        print("\nQUESTION:",q,flush=True)
        print("BEFORE:",entry["before"]["sources"],flush=True)
        print("AFTER: ",entry["after"]["sources"],flush=True)
        print("Alias duplicates displaced from top8:",entry["removed_alias_chunks_from_top8"],flush=True)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
        print("REPORT:",args.output,flush=True)
    print("PASS: V5 A/B test complete; Chroma unchanged.",flush=True)
if __name__=="__main__":main()
