#!/usr/bin/env python3
"""Validazione retrieval BGE: cinque domande, un solo caricamento modello, nessuna scrittura."""
import time
import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter
from llama_index.core.schema import QueryBundle
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.postprocessor.sbert_rerank import SentenceTransformerRerank

BASE = "/opt/football-data-lab/knowledge/rag/chroma"
SOURCE = "formations-and-systems/il_3412_Giustinetti.json"
QUESTIONS = [
    "Secondo il manuale di Giustinetti, come viene organizzata la fase di non possesso nel 3-4-1-2?",
    "Come si organizzano le marcature e le coperture reciproche dei tre difensori nel 3-4-1-2?",
    "Quali sono i compiti difensivi dei centrocampisti esterni nel 3-4-1-2?",
    "Quando e come viene applicato il pressing nel 3-4-1-2?",
    "Quali sono i compiti del trequartista nella fase di non possesso?",
]
collection = chromadb.PersistentClient(path=BASE).get_collection("dribbling_tactics_v1")
index = VectorStoreIndex.from_vector_store(
    ChromaVectorStore(chroma_collection=collection),
    embed_model=OllamaEmbedding(model_name="nomic-embed-text", base_url="http://127.0.0.1:11434"),
)
retriever = VectorIndexRetriever(
    index=index, similarity_top_k=15,
    filters=MetadataFilters(filters=[ExactMatchFilter(key="source", value=SOURCE)]),
)
print("Caricamento BGE-v2-m3...", flush=True)
reranker = SentenceTransformerRerank(model="BAAI/bge-reranker-v2-m3", top_n=5, device="cpu")
for number, question in enumerate(QUESTIONS, 1):
    print(f"\\n{'='*65}\\nDOMANDA {number}: {question}", flush=True)
    t0 = time.perf_counter()
    candidates = retriever.retrieve(question)
    t1 = time.perf_counter()
    ranked = reranker.postprocess_nodes(candidates, query_bundle=QueryBundle(query_str=question))
    t2 = time.perf_counter()
    print(f"Semantica: {t1-t0:.2f}s | Reranking: {t2-t1:.2f}s", flush=True)
    for i, item in enumerate(ranked, 1):
        meta = item.node.metadata
        snippet = " ".join(item.node.text.split())[:270]
        print(f"{i}. pagina={meta.get('page')} | sezione={meta.get('section')} | score={item.score:.4f}\\n   {snippet}", flush=True)
print("\\nTEST COMPLETATO: nessun dato modificato.", flush=True)
