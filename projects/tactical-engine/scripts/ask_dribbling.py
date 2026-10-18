#!/usr/bin/env python3
"""Interroga il RAG di DRIBBLING usando ChromaDB, Ollama embeddings e Qwen3 Instruct."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import chromadb
import requests

BASE = Path('/opt/football-data-lab')
DB = BASE / 'knowledge/rag/chroma'
COLLECTION = 'dribbling_tactics_v1'
OLLAMA = 'http://127.0.0.1:11434'
EMBED_MODEL = 'nomic-embed-text'
CHAT_MODEL = 'qwen3:4b-instruct'


def request_json(session: requests.Session, endpoint: str, payload: dict, timeout: int = 240) -> dict:
    response = session.post(f'{OLLAMA}{endpoint}', json=payload, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    if data.get('error'):
        raise RuntimeError(data['error'])
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description='Domande tattiche basate sui manuali indicizzati')
    parser.add_argument('question', nargs='*', help='Domanda; se omessa viene richiesta a video')
    parser.add_argument('--top-k', type=int, default=5, help='Numero di passaggi da recuperare (predefinito 5)')
    args = parser.parse_args()
    question = ' '.join(args.question).strip() or input('Domanda tattica: ').strip()
    if not question:
        sys.exit('Domanda vuota.')
    if not DB.exists():
        sys.exit(f'Indice non trovato: {DB}')

    session = requests.Session()
    client = chromadb.PersistentClient(path=str(DB))
    collection = client.get_collection(COLLECTION)
    count = collection.count()
    if count == 0:
        sys.exit('Indice vuoto.')

    emb = request_json(session, '/api/embed', {'model': EMBED_MODEL, 'input': question})
    vectors = emb.get('embeddings') or []
    if len(vectors) != 1:
        sys.exit('Embedding della domanda non valido.')

    result = collection.query(
        query_embeddings=vectors,
        n_results=min(max(1, args.top_k), count),
        include=['documents', 'metadatas', 'distances'],
    )
    docs = result['documents'][0]
    metas = result['metadatas'][0]
    distances = result['distances'][0]
    sources = []
    context = []
    for i, (doc, meta, dist) in enumerate(zip(docs, metas, distances), 1):
        source = meta.get('source', 'sconosciuto')
        page = meta.get('page', '?')
        section = meta.get('section', '')
        try:
            figures = json.loads(meta.get('figures_json', '[]'))
        except (TypeError, ValueError):
            figures = []
        sources.append((i, source, page, section, dist, figures))
        context.append(f'[FONTE {i}] Manuale: {source}; pagina PDF: {page}; sezione: {section or "non indicata"}\n{doc}')

    system = (
        'Sei DRIBBLING, assistente di analisi tattica calcistica. '
        'Rispondi esclusivamente in italiano, con precisione e senza divagazioni. '
        'Utilizza SOLO le informazioni presenti negli estratti forniti. '
        'Se gli estratti non bastano per rispondere, dichiaralo chiaramente. '
        'Non inventare fatti, pagine, citazioni o interpretazioni di immagini. '
        'Cita i passaggi usati con [FONTE 1], [FONTE 2] ecc.; '
        'non citare fonti che non sostengono le affermazioni. '
        'Non affermare di aver visto figure: sono disponibili solo i testi.'
    )
    prompt = (
        f'DOMANDA:\n{question}\n\n'
        'ESTRATTI DAI MANUALI (gli identificativi delle fonti sono utilizzabili nelle citazioni):\n\n'
        + '\n\n'.join(context)
        + '\n\nRispondi alla domanda usando solo gli estratti pertinenti e citando le fonti.'
    )
    reply = request_json(session, '/api/chat', {
        'model': CHAT_MODEL,
        'stream': False,
        'messages': [
            {'role': 'system', 'content': system},
            {'role': 'user', 'content': prompt},
        ],
        'options': {'temperature': 0.2, 'num_predict': 600},
    }, timeout=300)
    print('\n=== RISPOSTA DRIBBLING ===\n')
    print((reply.get('message') or {}).get('content', '').strip() or '(nessuna risposta)')
    print('\n=== FONTI RECUPERATE ===')
    for i, source, page, section, dist, figures in sources:
        print(f'[FONTE {i}] {Path(source).stem} | pagina PDF {page} | sezione: {section or "-"} | distanza: {dist:.3f}')
        if figures:
            names = ', '.join(Path(f.get('file', '')).name for f in figures if f.get('file'))
            if names:
                print(f'  Figure presenti nella pagina (non analizzate visivamente): {names}')
    print('\nNota: le fonti elencate sono i passaggi recuperati; verificare quali sono effettivamente citati nella risposta.')


if __name__ == '__main__':
    try:
        main()
    except (requests.RequestException, RuntimeError, ValueError, chromadb.errors.ChromaError) as exc:
        sys.exit(f'ERRORE: {exc}')
