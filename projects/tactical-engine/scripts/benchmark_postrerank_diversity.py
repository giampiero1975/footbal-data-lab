#!/usr/bin/env python3
"""DRIBBLING Q8: benchmark diversificazione DOPO mMARCO (sola lettura)."""
import time
import numpy as np
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


def label(cid):
    return next((v for k, v in GOLD.items() if cid.startswith(k)), '')


def report(name, order, ids):
    selected = [ids[i] for i in order]
    found = sum(any(cid.startswith(k) for cid in selected) for k in GOLD)
    print(f'\n{name} | GOLD@{len(selected)}={found}/3', flush=True)
    for pos, cid in enumerate(selected, 1):
        print(f' {pos:2}. {cid[:12]}' + (f' | GOLD: {label(cid)}' if label(cid) else ''), flush=True)


def diversify(scores, vectors, k, alpha):
    """Greedy: alpha * pertinenza mMARCO + (1-alpha) * novita embedding.

    Pertinenza = percentile del ranking mMARCO [0,1].
    Novita = 1 - massima similarita coseno con frammenti gia scelti.
    Non e' l'MMR nativo Chroma: qui il segnale di rilevanza e' mMARCO.
    """
    n = len(scores)
    rank = sorted(range(n), key=lambda i: (-float(scores[i]), i))
    relevance = np.empty(n, dtype=float)
    for position, idx in enumerate(rank):
        relevance[idx] = 1 - position / max(1, n - 1)
    vec = np.asarray(vectors, dtype=float)
    vec /= np.maximum(np.linalg.norm(vec, axis=1, keepdims=True), 1e-12)
    similarity = vec @ vec.T
    selected = []
    while len(selected) < min(k, n):
        best_idx, best_value = None, -float('inf')
        for idx in range(n):
            if idx in selected:
                continue
            novelty = 1 - max(float(similarity[idx, j]) for j in selected) if selected else 1.0
            value = alpha * relevance[idx] + (1 - alpha) * novelty
            if value > best_value:
                best_idx, best_value = idx, value
        selected.append(best_idx)
    return selected


def main():
    collection = chromadb.PersistentClient(path=DB).get_collection(COLLECTION)
    print(f'Collection: {COLLECTION} | record: {collection.count()} | filtro: {SOURCE}', flush=True)
    if collection.count() != 86:
        raise RuntimeError('Numero record diverso da 86: verificare collection')
    embedding = OllamaEmbedding(model_name='qwen3-embedding:0.6b', base_url='http://127.0.0.1:11434')
    t0 = time.perf_counter()
    query_vector = embedding.get_query_embedding(QUESTION)
    print(f'Embedding query: {time.perf_counter()-t0:.2f}s', flush=True)
    result = collection.query(query_embeddings=[query_vector], n_results=15,
                              where={'source': SOURCE},
                              include=['documents', 'embeddings', 'distances'])
    ids = result['ids'][0]
    docs = result['documents'][0]
    vectors = result['embeddings'][0]
    if len(ids) != 15 or vectors is None or len(vectors) != 15:
        raise RuntimeError('Retrieval non completo: attesi 15 documenti con embedding')
    print('Caricamento mMARCO...', flush=True)
    model = CrossEncoder('cross-encoder/mmarco-mMiniLMv2-L12-H384-v1', device='cpu', max_length=512)
    t0 = time.perf_counter()
    scores = model.predict([(QUESTION, doc) for doc in docs], batch_size=1, show_progress_bar=False)
    print(f'Reranking mMARCO: {time.perf_counter()-t0:.2f}s', flush=True)
    ranking = sorted(range(len(ids)), key=lambda i: -float(scores[i]))
    report('BASELINE mMARCO top5', ranking[:5], ids)
    report('BASELINE mMARCO top10 (controllo)', ranking[:10], ids)
    for alpha in (0.3, 0.5, 0.7, 0.85, 0.95):
        t0 = time.perf_counter()
        chosen = diversify(scores, vectors, 5, alpha)
        report(f'POST-RERANK diversity top5 | alpha={alpha:.2f} | {time.perf_counter()-t0:.4f}s', chosen, ids)
    print('\nNOTA: test diagnostico su una sola domanda, non prova di miglioramento generale.', flush=True)
    print('FINE: sola lettura, nessuna modifica a Chroma o modelli.', flush=True)


if __name__ == '__main__':
    main()
