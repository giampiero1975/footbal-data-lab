#!/usr/bin/env python3
"""Benchmark read-only LlamaIndex MMR / Chroma / mMARCO, Q8 Glerean."""
import time
import chromadb
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.vector_stores.types import VectorStoreQuery, VectorStoreQueryMode
from sentence_transformers import CrossEncoder

DB = '/opt/football-data-lab/knowledge/rag/chroma'
COLLECTION = 'dribbling_tactics_v4_qwen3_embedding_06b'
SOURCE = '334_principi_Glerean'
QUESTION = 'Come si sviluppa l’ampiezza offensiva nel 3-3-4 di Glerean?'
GOLD = {
    'f897ecc2c11e': 'Ampiezza centrocampisti con palla in difesa',
    '43c85faf1870': 'Ampiezza esterni con palla a centrocampo',
    '5319d503a8ec': 'Profondita e ampiezza attaccanti laterali',
}

def gold_name(cid):
    return next((name for prefix, name in GOLD.items() if cid.startswith(prefix)), None)

def print_ranking(title, ids, limit=10):
    found = {prefix for prefix in GOLD if any(cid.startswith(prefix) for cid in ids[:5])}
    print(f'\n{title} | GOLD@5={len(found)}/3 | GOLD@{len(ids)}={sum(any(cid.startswith(p) for cid in ids) for p in GOLD)}/3', flush=True)
    for pos, cid in enumerate(ids[:limit], 1):
        print(f' {pos:2}. {cid[:12]}' + (f' | GOLD: {gold_name(cid)}' if gold_name(cid) else ''), flush=True)

def main():
    coll = chromadb.PersistentClient(path=DB).get_collection(COLLECTION)
    print('COLLECTION:', COLLECTION, '| totale:', coll.count(), flush=True)
    embedding = OllamaEmbedding(model_name='qwen3-embedding:0.6b', base_url='http://127.0.0.1:11434')
    start = time.perf_counter()
    vector = embedding.get_query_embedding(QUESTION)
    print(f'Embedding: {time.perf_counter()-start:.2f}s | dimensione={len(vector)}', flush=True)
    store = ChromaVectorStore(chroma_collection=coll)
    dense = coll.query(query_embeddings=[vector], n_results=15, where={'source': SOURCE}, include=['documents'])
    dense_ids, dense_docs = dense['ids'][0], dense['documents'][0]
    print_ranking('BASELINE dense top15', dense_ids, 15)
    print('Carico mMARCO...', flush=True)
    model = CrossEncoder('cross-encoder/mmarco-mMiniLMv2-L12-H384-v1', device='cpu', max_length=512)

    def rerank(ids, docs, title):
        t = time.perf_counter()
        scores = model.predict([(QUESTION, doc) for doc in docs], batch_size=1, show_progress_bar=False)
        order = sorted(range(len(ids)), key=lambda i: float(scores[i]), reverse=True)
        ranked = [ids[i] for i in order]
        print_ranking(f'{title} | rerank={time.perf_counter()-t:.2f}s', ranked)
        return ranked

    rerank(dense_ids, dense_docs, 'BASELINE mMARCO dense15 -> top5')
    for k in (5, 10, 15):
        for threshold in (0.2, 0.5, 0.8):
            t = time.perf_counter()
            try:
                q = VectorStoreQuery(query_embedding=vector, similarity_top_k=k, mode=VectorStoreQueryMode.MMR)
                result = store.query(q, where={'source': SOURCE}, mmr_prefetch_k=15, mmr_threshold=threshold)
                ids = list(result.ids or [])
                docs = [node.get_content() for node in (result.nodes or [])]
                print(f'\nMMR nativo: k={k}, threshold={threshold} | tempo={time.perf_counter()-t:.3f}s', flush=True)
                print_ranking('MMR selezione', ids)
                rerank(ids, docs, f'MMR{k} -> mMARCO top5')
            except Exception as exc:
                print(f'ERRORE MMR k={k} threshold={threshold}: {type(exc).__name__}: {exc}', flush=True)
    print('\nFINE: benchmark in sola lettura; nessuna modifica agli indici.', flush=True)

if __name__ == '__main__':
    main()
