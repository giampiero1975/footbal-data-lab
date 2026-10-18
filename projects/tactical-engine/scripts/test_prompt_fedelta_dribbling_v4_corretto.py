#!/usr/bin/env python3
"""DRIBBLING V4: genera solo la risposta B (TOP 10), senza baseline esterna.
Non modifica ChromaDB e non installa nulla.
"""
import argparse
import re
import time
from pathlib import Path

import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.core.prompts import PromptTemplate
from llama_index.core.query_engine import CitationQueryEngine
from llama_index.core.vector_stores import MetadataFilter, MetadataFilters
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.postprocessor.sbert_rerank import SentenceTransformerRerank
from llama_index.vector_stores.chroma import ChromaVectorStore

from test_dribbling_v4_top5_top10 import DB, COLLECTION, SOURCE, QUESTION

QA_B = PromptTemplate(
    'Sei DRIBBLING, analista tattico del calcio. Rispondi in italiano usando '
    'ESCLUSIVAMENTE le fonti numerate qui sotto. Non integrare conoscenze esterne.\n'
    'Per ogni situazione descrivi con precisione: (1) DOVE si trova la palla '
    '(nostra zona difensiva, centrocampo, zona d’attacco), (2) QUALI giocatori '
    'si muovono, (3) COME si muovono. Non scambiare la nostra zona difensiva '
    'con quella avversaria.\n'
    'Distingui i movimenti dei centrocampisti esterni da quelli degli attaccanti '
    'esterni; distingui ampiezza e profondita. Non confondere autori diversi.\n'
    'Ogni affermazione specifica deve citare [N], dove N e il numero della '
    'Source N che contiene ESATTAMENTE quell’informazione. Non citare una '
    'fonte soltanto perche tratta un argomento simile. Se non puoi identificare '
    'la fonte precisa, non formulare l’affermazione come fatto documentato.\n'
    'Prima di rispondere, controlla mentalmente la corrispondenza tra '
    'affermazioni, zona della palla e numeri di fonte. Non mostrare il controllo.\n'
    'Le figure non sono state analizzate visivamente; non dedurne dettagli.\n\n'
    'FONTI:\n{context_str}\n\nDOMANDA: {query_str}\n\nRISPOSTA:'
)
REFINE_B = PromptTemplate(
    'Sei DRIBBLING. Usa soltanto le fonti numerate.\n'
    'DOMANDA: {query_str}\nRISPOSTA PRECEDENTE: {existing_answer}\n'
    'NUOVE FONTI:\n{context_msg}\n\n'
    'Integra solo informazioni esplicitamente documentate. Non confondere '
    'nostra difesa e difesa avversaria, ne centrocampisti esterni e attaccanti '
    'esterni. Ogni [N] deve riferirsi alla Source N pertinente. '
    'Se necessario correggi contenuti e citazioni precedenti.\n'
    'RISPOSTA AGGIORNATA:'
)


def diagnostics(answer, n_sources):
    citations = [int(n) for n in re.findall(r'\[(\d+)\]', answer)]
    invalid = sorted(set(citations) - set(range(1, n_sources + 1)))
    wrong_zone = bool(re.search(r'zona difensiva avversaria', answer, re.I))
    return citations, invalid, wrong_zone


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='/opt/football-data-lab/projects/tactical-engine/test_prompt_fedelta_v4.txt')
    args = parser.parse_args()
    collection = chromadb.PersistentClient(path=DB).get_collection(COLLECTION)
    if collection.count() != 86:
        raise RuntimeError(f'Collection V4 inattesa: {collection.count()} record anziche 86')
    index = VectorStoreIndex.from_vector_store(
        ChromaVectorStore(chroma_collection=collection),
        embed_model=OllamaEmbedding(model_name='qwen3-embedding:0.6b', base_url='http://127.0.0.1:11434'),
    )
    filters = MetadataFilters(filters=[MetadataFilter(key='source', value=SOURCE)])
    llm = Ollama(model='qwen3.5:9b', base_url='http://127.0.0.1:11434',
                 request_timeout=900.0, temperature=0.1, context_window=8192, thinking=False)
    retriever = index.as_retriever(similarity_top_k=15, filters=filters)
    reranker = SentenceTransformerRerank(
        model='cross-encoder/mmarco-mMiniLMv2-L12-H384-v1', top_n=10, device='cpu')
    engine = CitationQueryEngine.from_args(
        index=index, retriever=retriever, llm=llm, node_postprocessors=[reranker],
        citation_chunk_size=2048, citation_chunk_overlap=0,
        citation_qa_template=QA_B, citation_refine_template=REFINE_B,
        response_mode='compact',
    )
    print('Generazione TOP 10 con prompt B in corso...', flush=True)
    started = time.monotonic()
    response = engine.query(QUESTION)
    elapsed = time.monotonic() - started
    nodes = list(response.source_nodes or [])
    answer = str(response)
    cites, invalid, wrong_zone = diagnostics(answer, len(nodes))
    lines = [
        'DRIBBLING V4 - TEST PROMPT B (SENZA BASELINE ESTERNA)',
        f'Domanda: {QUESTION}', f'Tempo B: {elapsed:.1f}s',
        'Parametri: V4 Qwen3-Embedding, mMARCO TOP 10, Qwen3.5 9B, compact',
        '\n=== RISPOSTA B ===', answer,
        f'Citazioni B: {cites}; fuori intervallo: {invalid}; '
        f'contiene "zona difensiva avversaria": {wrong_zone}',
        '\n=== FONTI NUMERATE DEL TEST B ===',
    ]
    for i, node in enumerate(nodes, 1):
        lines.append(f'[{i}] source={node.node.metadata.get("source", "?")} | score={node.score}\n{node.node.get_content()}')
    lines.extend([
        '\nATTENZIONE: citazioni nel range NON significa citazioni corrette.',
        'Verificare manualmente corrispondenza fonte-affermazione e completezza dei tre principi.',
        'Una singola generazione B non dimostra miglioramento sistematico.',
    ])
    out = Path(args.output)
    out.write_text('\n\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Completato in {elapsed:.1f}s | fonti: {len(nodes)} | citazioni fuori intervallo: {invalid}', flush=True)
    print(f'Errore testuale "zona difensiva avversaria": B={wrong_zone}', flush=True)
    print(f'Report: {out}', flush=True)


if __name__ == '__main__':
    main()
