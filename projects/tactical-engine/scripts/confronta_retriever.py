#!/usr/bin/env python3
"""Confronto controllato tra retriever ufficiali LlamaIndex; sola lettura."""
import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.core.schema import TextNode
from llama_index.core.retrievers import VectorIndexRetriever, QueryFusionRetriever
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.retrievers.bm25 import BM25Retriever

PATH = "/opt/football-data-lab/knowledge/rag/chroma"
COLLECTION = "dribbling_tactics_v1"
SOURCE = "formations-and-systems/il_3412_Giustinetti.json"
QUESTION = "Secondo il manuale di Giustinetti, come viene organizzata la fase di non possesso nel 3-4-1-2?"
TOP_K = 8

collection = chromadb.PersistentClient(path=PATH).get_collection(COLLECTION)
data = collection.get(include=["documents", "metadatas"])
nodes = [
    TextNode(id_=identifier, text=document, metadata=metadata or {})
    for identifier, document, metadata in zip(
        data["ids"], data["documents"], data["metadatas"]
    )
    if document and (metadata or {}).get("source") == SOURCE
]
if not nodes:
    raise SystemExit("ERRORE: nessun blocco trovato per il manuale Giustinetti.")

embed = OllamaEmbedding(model_name="nomic-embed-text", base_url="http://127.0.0.1:11434")
store = ChromaVectorStore(chroma_collection=collection)
index = VectorStoreIndex.from_vector_store(store, embed_model=embed)
filters = MetadataFilters(filters=[ExactMatchFilter(key="source", value=SOURCE)])
semantic = VectorIndexRetriever(index=index, similarity_top_k=TOP_K, filters=filters)
bm25 = BM25Retriever.from_defaults(nodes=nodes, similarity_top_k=TOP_K, language="italian")
hybrid = QueryFusionRetriever(
    retrievers=[semantic, bm25],
    similarity_top_k=TOP_K,
    num_queries=1,
    llm=__import__("llama_index.core.llms", fromlist=["MockLLM"]).MockLLM(),
    mode="reciprocal_rerank",
    use_async=False,
)

print("DOMANDA:", QUESTION)
print("BLOCCHI TOTALI:", collection.count(), "| GIUSTINETTI:", len(nodes))
for label, retriever in [
    ("SEMANTICA", semantic),
    ("BM25", bm25),
    ("IBRIDA RRF", hybrid),
]:
    print("\\n" + "=" * 24 + " " + label + " " + "=" * 24)
    try:
        results = retriever.retrieve(QUESTION)
        for rank, result in enumerate(results, 1):
            meta = result.node.metadata
            print(
                f"{rank}. score={result.score:.4f} | "
                f"pagina={meta.get('page')} | "
                f"sezione={meta.get('section')} | "
                f"fonte={meta.get('source')}"
            )
            print("   ", " ".join(result.node.text.split())[:230])
    except Exception as exc:
        print(f"ERRORE {label}: {type(exc).__name__}: {exc}")
