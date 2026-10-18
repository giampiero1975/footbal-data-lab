#!/usr/bin/env python3
"""Test end-to-end RAG con soli componenti LlamaIndex. Nessuna scrittura su ChromaDB."""
import json
import time
from pathlib import Path

import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.core.query_engine import CitationQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.postprocessor.sbert_rerank import SentenceTransformerRerank
from llama_index.vector_stores.chroma import ChromaVectorStore

QUESTION = "Secondo il manuale di Giustinetti, come viene organizzata la fase di non possesso nel 3-4-1-2?"
SOURCE = "formations-and-systems/il_3412_Giustinetti.json"
DB_PATH = "/opt/football-data-lab/knowledge/rag/chroma"

collection = chromadb.PersistentClient(path=DB_PATH).get_collection("dribbling_tactics_v1")
index = VectorStoreIndex.from_vector_store(
    ChromaVectorStore(chroma_collection=collection),
    embed_model=OllamaEmbedding(model_name="nomic-embed-text", base_url="http://127.0.0.1:11434"),
)
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=15,
    filters=MetadataFilters(filters=[ExactMatchFilter(key="source", value=SOURCE)]),
)
reranker = SentenceTransformerRerank(
    model="BAAI/bge-reranker-v2-m3", top_n=5, device="cpu"
)
llm = Ollama(
    model="qwen3:4b-instruct",
    base_url="http://127.0.0.1:11434",
    request_timeout=300.0,
    temperature=0,
    context_window=8192,
)
engine = CitationQueryEngine.from_args(
    index=index,
    retriever=retriever,
    node_postprocessors=[reranker],
    llm=llm,
    citation_chunk_size=4096,
    citation_chunk_overlap=0,
    response_mode="compact",
)

print("DOMANDA:", QUESTION, flush=True)
print("Pipeline: LlamaIndex / ChromaDB / BGE-v2-m3 / Qwen3 Instruct", flush=True)
print("Elaborazione in corso: il reranking CPU richiede circa 18 secondi, poi parte Qwen3.", flush=True)
t0 = time.perf_counter()
response = engine.query(QUESTION)
print("\nRISPOSTA:\n" + str(response), flush=True)
print("\nFONTI EFFETTIVAMENTE FORNITE AL MODELLO:", flush=True)
for i, item in enumerate(response.source_nodes, 1):
    meta = item.node.metadata
    print(f"\n[Source {i}] manuale={meta.get('source')} | pagina={meta.get('page')} | sezione={meta.get('section')}")
    print("Estratto:", " ".join(item.node.text.split())[:320])
    try:
        figures = json.loads(meta.get("figures_json", "[]"))
        for fig in figures:
            print("Figura associata (non interpretata):", Path(fig.get("file", "")).name)
    except (ValueError, TypeError):
        print("Nota: metadati figure non leggibili")
print(f"\nTEMPO TOTALE: {time.perf_counter() - t0:.1f} secondi", flush=True)
print("NOTA: le citazioni vanno verificate contro gli estratti; le figure sono soltanto riferimenti associati.")
