#!/usr/bin/env python3
"""Diagnosi read-only: embedding, Chroma e BGE, con/senza filtro autore."""
import json
from collections import Counter
import chromadb
from llama_index.core.schema import NodeWithScore, QueryBundle, TextNode
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.postprocessor.sbert_rerank import SentenceTransformerRerank

DB='/opt/football-data-lab/knowledge/rag/chroma'
CONFIGS=[('NOMIC','dribbling_tactics_v3_contextualized','nomic-embed-text'),('QWEN_06B','dribbling_tactics_v4_qwen3_embedding_06b','qwen3-embedding:0.6b')]
TESTS=[(9,'Quali sono i compiti dei difensori nel 3-3-4 di Glerean?'),(8,'Come si sviluppa l’ampiezza offensiva nel 3-3-4 di Glerean?'),(7,'Come viene organizzata la fase di non possesso nel 3-3-4 di Glerean?')]
SOURCE='334_principi_Glerean'
client=chromadb.PersistentClient(path=DB)
reranker=SentenceTransformerRerank(model='BAAI/bge-reranker-v2-m3',top_n=5,device='cpu')
for label,collname,model in CONFIGS:
    coll=client.get_collection(collname)
    assert coll.count()==86,(label,coll.count())
    emb=OllamaEmbedding(model_name=model,base_url='http://127.0.0.1:11434')
    print('\n'+'#'*78+'\n'+label,flush=True)
    for number,question in TESTS:
        vec=emb.get_query_embedding(question)
        for filtered in (False,True):
            kw={'where':{'source':SOURCE}} if filtered else {}
            data=coll.query(query_embeddings=[vec],n_results=15,include=['documents','metadatas','distances'],**kw)
            nodes=[NodeWithScore(node=TextNode(id_=uid,text=doc,metadata=meta),score=1.0-dist)
                   for uid,doc,meta,dist in zip(data['ids'][0],data['documents'][0],data['metadatas'][0],data['distances'][0])]
            ranked=reranker.postprocess_nodes(nodes,query_bundle=QueryBundle(query_str=question))
            print(f'\nDOMANDA {number} | filtro={filtered} | dense15 fonti={dict(Counter(n.node.metadata["source"] for n in nodes))}',flush=True)
            for pos,n in enumerate(nodes,1):
                m=n.node.metadata
                heading=' / '.join(json.loads(m.get('headings','[]')))
                print(f'  DENSE {pos:02d} {m["source"]} | {heading[:75]} | {n.node.node_id[:12]}',flush=True)
            print('  BGE TOP5:',flush=True)
            for pos,n in enumerate(ranked,1):
                m=n.node.metadata
                heading=' / '.join(json.loads(m.get('headings','[]')))
                print(f'    {pos}. {m["source"]} | {heading[:75]} | {n.node.node_id[:12]} | score={n.score:.3f}',flush=True)
print('\nDIAGNOSI COMPLETATA: nessuna collection modificata.',flush=True)
