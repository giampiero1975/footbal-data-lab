#!/usr/bin/env python3
"""Confronto read-only: Chroma semantico vs LlamaIndex SentenceTransformerRerank."""
import time
import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.postprocessor.sbert_rerank import SentenceTransformerRerank
from llama_index.core.schema import QueryBundle

PATH = "/opt/football-data-lab/knowledge/rag/chroma"
COLLECTION = "dribbling_tactics_v1"
SOURCE = "formations-and-systems/il_3412_Giustinetti.json"
QUESTION = "Secondo il manuale di Giustinetti, come viene organizzata la fase di non possesso nel 3-4-1-2?"
MODEL = "BAAI/bge-reranker-v2-m3"

collection = chromadb.PersistentClient(path=PATH).get_collection(COLLECTION)
index = VectorStoreIndex.from_vector_store(
    ChromaVectorStore(chroma_collection=collection),
    embed_model=OllamaEmbedding(model_name="nomic-embed-text", base_url="http://127.0.0.1:11434"),
)
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=15,
    filters=MetadataFilters(filters=[ExactMatchFilter(key="source", value=SOURCE)]),
)

def show(title, results):
    print("\n" + title)
    for pos, result in enumerate(results, 1):
        m = result.node.metadata
        score = "n/d" if result.score is None else f"{result.score:.4f}"
        print(f"{pos}. score={score} | pag={m.get('page')} | sezione={m.get('section')}")
        print("   " + " ".join(result.node.text.split())[:220])

print("DOMANDA:", QUESTION, flush=True)
print("INDICE:", collection.count(), "blocchi", flush=True)
start = time.perf_counter()
candidates = retriever.retrieve(QUESTION)
retrieval_seconds = time.perf_counter() - start
show("SEMANTICA — primi 5 di 15", candidates[:5])
print(f"Tempo recupero semantico: {retrieval_seconds:.2f}s", flush=True)
print("\nCaricamento reranker", MODEL, "(il primo avvio scarica il modello)...", flush=True)
start = time.perf_counter()
reranker = SentenceTransformerRerank(model=MODEL, top_n=5, device="cpu")
load_seconds = time.perf_counter() - start
start = time.perf_counter()
ranked = reranker.postprocess_nodes(candidates, query_bundle=QueryBundle(query_str=QUESTION))
rerank_seconds = time.perf_counter() - start
show("SEMANTICA + RERANKER — migliori 5", ranked)
print(f"Tempo caricamento modello: {load_seconds:.2f}s")
print(f"Tempo reranking CPU: {rerank_seconds:.2f}s")
print(f"Tempo totale per richiesta a modello caricato: {retrieval_seconds + rerank_seconds:.2f}s")
