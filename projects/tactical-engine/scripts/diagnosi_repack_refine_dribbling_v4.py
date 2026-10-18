#!/usr/bin/env python3
"""DRIBBLING V4: riproduce il repack iniziale di Refine senza generare risposte.

Sola lettura: retrieval + rerank + preparazione prompt. Richiede lo script
originale test_dribbling_v4_top5_top10.py nella stessa cartella.
"""
import re
import sys
from pathlib import Path

import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.core.query_engine import CitationQueryEngine
from llama_index.core.schema import MetadataMode, QueryBundle
from llama_index.core.vector_stores import MetadataFilter, MetadataFilters
from llama_index.core.response_synthesizers.refine import get_biggest_prompt
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.postprocessor.sbert_rerank import SentenceTransformerRerank
from llama_index.vector_stores.chroma import ChromaVectorStore

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_dribbling_v4_top5_top10 import DB, COLLECTION, SOURCE, QUESTION, QA, REFINE

collection = chromadb.PersistentClient(path=DB).get_collection(COLLECTION)
index = VectorStoreIndex.from_vector_store(
    ChromaVectorStore(chroma_collection=collection),
    embed_model=OllamaEmbedding(model_name='qwen3-embedding:0.6b', base_url='http://127.0.0.1:11434'),
)
filters = MetadataFilters(filters=[MetadataFilter(key='source', value=SOURCE)])
llm = Ollama(model='qwen3.5:9b', base_url='http://127.0.0.1:11434',
             request_timeout=900.0, temperature=0.1, context_window=8192, thinking=False)

for top in (5, 10):
    retriever = index.as_retriever(similarity_top_k=15, filters=filters)
    reranker = SentenceTransformerRerank(
        model='cross-encoder/mmarco-mMiniLMv2-L12-H384-v1', top_n=top, device='cpu')
    engine = CitationQueryEngine.from_args(
        index=index, retriever=retriever, llm=llm,
        node_postprocessors=[reranker], citation_chunk_size=2048,
        citation_chunk_overlap=0, citation_qa_template=QA,
        citation_refine_template=REFINE, response_mode='compact',
    )
    nodes = engine._create_citation_nodes(engine.retrieve(QueryBundle(query_str=QUESTION)))
    synth = engine._response_synthesizer
    texts = [n.node.get_content(metadata_mode=MetadataMode.LLM) for n in nodes]
    groups = synth._make_compact_text_chunks(QUESTION, texts)

    # Stesse operazioni dell'inizio di Refine._run_refine_loop, prima di ogni chiamata LLM.
    max_prompt = get_biggest_prompt([synth._text_qa_template, synth._refine_template])
    helper = synth._prompt_helper
    initial_chunks = [
        piece for group in groups
        for piece in helper.repack(max_prompt, [group], llm=synth._llm,
                                  padding=synth._response_padding_size)
    ]
    print(f'\n=== TOP {top} ===', flush=True)
    print(f'Fonti numerate: {len(nodes)} | Gruppi compact: {len(groups)} | '
          f'Frammenti dopo repack interno iniziale: {len(initial_chunks)}', flush=True)
    for i, piece in enumerate(initial_chunks, 1):
        markers = re.findall(r'Source\s+(\d+)\s*:', piece)
        print(f'  Frammento {i}: {len(piece)} caratteri | Source: {markers}', flush=True)
    if len(initial_chunks) == 1:
        print('ESITO: una sola chiamata di generazione prevista dal ciclo Refine '
              '(senza prev_response), salvo differenze di runtime.', flush=True)
    else:
        print('ESITO: il ciclo Refine prevede piu passaggi; '
              'il numero finale non e deducibile senza la risposta generata.', flush=True)

print('\nFine: nessuna chiamata di generazione Qwen3.5; nessuna modifica agli indici.', flush=True)
