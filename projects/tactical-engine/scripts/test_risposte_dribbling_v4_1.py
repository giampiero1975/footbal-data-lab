#!/usr/bin/env python3
"""DRIBBLING V4.1 — prompt focalizzato, pipeline V3 invariata.

Solo lettura della collection V3. Nessuna modifica agli indici.
Dipendenze: llama-index-core, llama-index-vector-stores-chroma,
llama-index-llms-ollama, llama-index-embeddings-ollama,
llama-index-postprocessor-sbert-rerank, chromadb.
"""
from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path

import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.core.prompts import PromptTemplate
from llama_index.core.query_engine import CitationQueryEngine
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.postprocessor.sbert_rerank import SentenceTransformerRerank
from llama_index.vector_stores.chroma import ChromaVectorStore

CHROMA_PATH = '/opt/football-data-lab/knowledge/rag/chroma'
COLLECTION = 'dribbling_tactics_v3_contextualized'
QUESTIONS = [
    'Come si organizza il 3-4-1-2 in fase di non possesso?',
    'Come funzionano marcature e coperture difensive nel 3-4-1-2?',
    'Quali sono i compiti difensivi dei centrocampisti esterni?',
    'Come viene organizzato il pressing nel 3-4-1-2?',
    'Qual è il ruolo del trequartista in fase di non possesso?',
]

QA_PROMPT = PromptTemplate(
    'Sei DRIBBLING, analista tattico. Rispondi in italiano alla domanda specifica.\n'
    'Usa esclusivamente le fonti numerate fornite. Non aggiungere conoscenze esterne.\n'
    'PRIORITA: (1) rispondi direttamente; (2) spiega i movimenti e i compiti '
    'documentati; (3) cita ogni informazione tattica con [numero].\n'
    'Seleziona solo le informazioni pertinenti alla domanda. Non inserire '
    'svantaggi, classificazioni, confronti o avvertenze non richiesti.\n'
    'Prima di dichiarare che un dettaglio manca, verifica tutte le fonti. '
    'Non dichiarare assente una informazione che compare nel testo.\n'
    'Distingui sistemi misti e a zona SOLO se serve alla domanda e le fonti '
    'documentano la distinzione. Non confondere autori o sistemi.\n'
    'Non inventare riferimenti e non dedurre dettagli dalle figure.\n'
    'Usa una risposta compatta, concreta, senza note metatestuali.\n\n'
    'FONTI:\n{context_str}\n\nDOMANDA: {query_str}\n\nRISPOSTA:'
)
REFINE_PROMPT = PromptTemplate(
    'Sei DRIBBLING, analista tattico. Rispondi solo alla domanda.\n'
    'Domanda: {query_str}\n'
    'Risposta provvisoria: {existing_answer}\n'
    'Fonti aggiuntive:\n{context_msg}\n\n'
    'Controlla se le nuove fonti aggiungono fatti pertinenti o correggono '
    'errori della risposta. In tal caso aggiorna la risposta e le citazioni [numero]. '
    'Altrimenti mantieni il contenuto pertinente senza aggiungere digressioni.\n'
    'Elimina affermazioni non supportate, ripetizioni e informazioni fuori tema. '
    'Non dichiarare assenti fatti documentati nelle fonti. '
    'Non inventare riferimenti.\nRISPOSTA AGGIORNATA:'
)


def format_pages(meta: dict) -> str:
    try:
        return ','.join(str(n) for n in json.loads(meta.get('page_numbers', '[]'))) or '?'
    except (TypeError, ValueError):
        return '?'


def format_headings(meta: dict) -> str:
    try:
        values = json.loads(meta.get('headings', '[]'))
        return ' / '.join(str(x) for x in values) if values else '—'
    except (TypeError, ValueError):
        return '—'


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--question', type=int, choices=range(1, 6), default=5, help='Domanda da 1 a 5 (default: 5)')
    ap.add_argument('--candidates', type=int, default=15)
    ap.add_argument('--top', type=int, default=5)
    ap.add_argument('--output', default='/opt/football-data-lab/projects/tactical-engine/risposte_v4_1_qwen35_9b.txt')
    args = ap.parse_args()

    chroma = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = chroma.get_collection(COLLECTION)
    print(f'Collection: {COLLECTION} | record: {collection.count()}', flush=True)
    if collection.count() != 86:
        print('ATTENZIONE: la collection non contiene i 86 record attesi.', flush=True)

    embedding = OllamaEmbedding(model_name='nomic-embed-text', base_url='http://127.0.0.1:11434')
    vector_store = ChromaVectorStore(chroma_collection=collection)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store, embed_model=embedding)
    retriever = index.as_retriever(similarity_top_k=args.candidates)
    reranker = SentenceTransformerRerank(model='BAAI/bge-reranker-v2-m3', top_n=args.top, device='cpu')
    llm = Ollama(
        model='qwen3.5:9b',
        base_url='http://127.0.0.1:11434',
        request_timeout=600.0,
        temperature=0.1,
        context_window=8192,
        thinking=False,
    )
    engine = CitationQueryEngine.from_args(
        index=index,
        retriever=retriever,
        llm=llm,
        node_postprocessors=[reranker],
        citation_chunk_size=2048,
        citation_chunk_overlap=0,
        citation_qa_template=QA_PROMPT,
        citation_refine_template=REFINE_PROMPT,
        response_mode='compact',
    )

    print('V4.1 prompt focalizzato | LLM: qwen3.5:9b | thinking=False | context_window=8192 | temperature=0.1', flush=True)
    reports = []
    for number in [args.question]:
        question = QUESTIONS[number - 1]
        print(f'\nDOMANDA {number}: {question}', flush=True)
        start = time.monotonic()
        response = engine.query(question)
        elapsed = time.monotonic() - start
        answer = str(response)
        lines = [
            '=' * 78,
            f'DOMANDA {number}: {question}',
            f'Tempo totale: {elapsed:.1f}s',
            '\nRISPOSTA:\n' + answer,
            '\nFONTI FORNITE AL MODELLO:',
        ]
        source_nodes = list(response.source_nodes or [])
        for i, node in enumerate(source_nodes, 1):
            m = node.node.metadata or {}
            source = Path(m.get('source_json', m.get('source', '?'))).stem
            excerpt = node.node.get_content()
            score = f'{node.score:.3f}' if node.score is not None else '?'
            lines.append(
                f'[{i}] {source} | pagine {format_pages(m)} | '
                f'sezione {format_headings(m)} | score {score}\n    {excerpt}'
            )
        citations = [int(x) for x in re.findall(r'\[(\d+)\]', answer)]
        invalid = sorted(set(citations) - set(range(1, len(source_nodes) + 1)))
        lines.append(f'\nRiferimenti citati: {citations}; inesistenti: {invalid}')
        lines.append('NOTA: la presenza di una citazione non ne prova la correttezza; verificare manualmente.')
        report = '\n'.join(lines)
        print(report, flush=True)
        reports.append(report)
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text('\n\n'.join(reports) + '\n', encoding='utf-8')
    print(f'\nTEST COMPLETATO. Report: {args.output}', flush=True)


if __name__ == '__main__':
    main()
