#!/usr/bin/env python3
"""Diagnosi Q8: copertura dei passaggi in dense top15/top30 e reranking top15. Solo lettura."""
import time
import chromadb
from llama_index.embeddings.ollama import OllamaEmbedding
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

def label(chunk_id):
    return next((name for prefix, name in GOLD.items() if chunk_id.startswith(prefix)), '')

def main():
    coll = chromadb.PersistentClient(path=DB).get_collection(COLLECTION)
    print('COLLECTION:', COLLECTION, '| totale:', coll.count(), flush=True)
    emb = OllamaEmbedding(model_name='qwen3-embedding:0.6b', base_url='http://127.0.0.1:11434')
    t0 = time.perf_counter()
    vector = emb.get_query_embedding(QUESTION)
    print('Embedding:', round(time.perf_counter()-t0, 2), 's', flush=True)
    res = coll.query(query_embeddings=[vector], n_results=30,
                     where={'source': SOURCE}, include=['documents', 'metadatas', 'distances'])
    ids, docs, distances = res['ids'][0], res['documents'][0], res['distances'][0]
    print('\nPOSIZIONE DENSE (top30, filtro Glerean):', flush=True)
    for prefix, desc in GOLD.items():
        found = next((i for i, chunk_id in enumerate(ids, 1) if chunk_id.startswith(prefix)), None)
        print(f'  {prefix} | {desc}: posizione {found if found else "OLTRE 30"}' +
              (f' | distanza={distances[found-1]:.4f}' if found else ''), flush=True)
    print('\nDENSE TOP15:', flush=True)
    for i, (chunk_id, distance) in enumerate(zip(ids[:15], distances[:15]), 1):
        print(f'  {i:2}. {chunk_id[:12]} | dist={distance:.4f}' + (f' | GOLD: {label(chunk_id)}' if label(chunk_id) else ''), flush=True)
    print('\nCarico mMARCO...', flush=True)
    model = CrossEncoder('cross-encoder/mmarco-mMiniLMv2-L12-H384-v1', device='cpu', max_length=512)
    t0 = time.perf_counter()
    scores = model.predict([(QUESTION, doc) for doc in docs[:15]], batch_size=1, show_progress_bar=False)
    ranking = sorted(range(15), key=lambda i: float(scores[i]), reverse=True)
    print(f'mMARCO top15: {time.perf_counter()-t0:.2f}s', flush=True)
    for rank, i in enumerate(ranking, 1):
        chunk_id = ids[i]
        print(f'  {rank:2}. {chunk_id[:12]} | dense_pos={i+1} | score={float(scores[i]):.3f}' +
              (f' | GOLD: {label(chunk_id)}' if label(chunk_id) else ''), flush=True)
    print('\nCOPERTURA GOLD nei primi 5 mMARCO:',
          sum(bool(label(ids[i])) for i in ranking[:5]), '/ 3', flush=True)
    print('FINE: nessuna modifica a collection, modelli o configurazione.', flush=True)

if __name__ == '__main__':
    main()
