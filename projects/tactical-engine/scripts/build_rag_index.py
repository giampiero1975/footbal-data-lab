#!/usr/bin/env python3
"""DRIBBLING Tactical Engine - indicizzazione Docling JSON in ChromaDB.

Dipendenze: chromadb, requests. Embeddings: Ollama nomic-embed-text.
Non interpreta il contenuto visivo delle figure; le associa per pagina.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import chromadb
import requests

BASE = Path('/opt/football-data-lab')
PROCESSED = BASE / 'knowledge/processed'
INDEX = BASE / 'knowledge/rag/chroma'
COLLECTION = 'dribbling_tactics_v1'
OLLAMA = 'http://127.0.0.1:11434/api/embed'
EMBED_MODEL = 'nomic-embed-text'
TARGET_CHARS = 1050
MAX_CHARS = 1450
MIN_CHARS = 180
KEEP = {'text', 'section_header', 'list_item', 'caption'}


def normalize(s: str) -> str:
    return re.sub(r'\s+', ' ', s or '').strip()


def get_page(item: dict) -> int | None:
    prov = item.get('prov') or []
    return prov[0].get('page_no') if prov else None


def ordered_texts(doc: dict) -> list[dict]:
    """Use Docling body reading order, including nested groups; fallback to texts list."""
    text_by_ref = {t['self_ref']: t for t in doc.get('texts', []) if 'self_ref' in t}
    groups = {g['self_ref']: g for g in doc.get('groups', []) if 'self_ref' in g}
    seen: set[str] = set()
    result: list[dict] = []

    def visit(ref: str, depth: int = 0) -> None:
        if depth > 50 or ref in seen:
            return
        seen.add(ref)
        if ref in text_by_ref:
            result.append(text_by_ref[ref])
        elif ref in groups:
            for child in groups[ref].get('children', []):
                visit(child.get('$ref', ''), depth + 1)

    for child in doc.get('body', {}).get('children', []):
        visit(child.get('$ref', ''))
    # Some document exports omit group hierarchy; preserve remaining text order.
    for t in doc.get('texts', []):
        if t.get('self_ref') not in seen:
            result.append(t)
    return [t for t in result if t.get('label') in KEEP and normalize(t.get('text', '')) and get_page(t)]


def page_figures(json_path: Path) -> dict[int, list[dict]]:
    index_path = json_path.with_name(json_path.stem + '_images') / 'images.json'
    if not index_path.exists():
        return {}
    mapping: dict[int, list[dict]] = defaultdict(list)
    for f in json.loads(index_path.read_text(encoding='utf-8')):
        page = f.get('page')
        name = f.get('file')
        if isinstance(page, int) and isinstance(name, str):
            mapping[page].append({
                'file': str(index_path.parent / name),
                'self_ref': f.get('self_ref', ''),
            })
    return mapping


def make_chunks(doc: dict, source: Path) -> list[dict]:
    items = ordered_texts(doc)
    figures = page_figures(source)
    chunks: list[dict] = []
    current: list[str] = []
    current_refs: list[str] = []
    page: int | None = None
    heading = ''
    current_heading = ''

    def flush() -> None:
        nonlocal current, current_refs
        if not current or page is None:
            current, current_refs = [], []
            return
        content = '\n'.join(current)
        figs = figures.get(page, [])
        chunks.append({
            'text': content,
            'page': page,
            'heading': current_heading,
            'refs': list(current_refs),
            'figures': figs,
        })
        current, current_refs = [], []

    for item in items:
        item_page = get_page(item)
        label = item.get('label', '')
        txt = normalize(item.get('text', ''))
        if label == 'section_header':
            flush()
            heading = txt
            continue
        if item_page != page:
            flush()
            page = item_page
        if not current:
            current_heading = heading
        # Split unusually long paragraphs without dropping text.
        pieces = [txt[i:i + MAX_CHARS] for i in range(0, len(txt), MAX_CHARS)]
        for piece in pieces:
            if current and sum(map(len, current)) + len(piece) + len(current) > TARGET_CHARS:
                flush()
                current_heading = heading
            current.append(('- ' if label == 'list_item' else '') + piece)
            current_refs.append(item.get('self_ref', ''))
            if sum(map(len, current)) >= MAX_CHARS:
                flush()
    flush()
    return chunks


def embed(texts: list[str], session: requests.Session) -> list[list[float]]:
    response = session.post(OLLAMA, json={'model': EMBED_MODEL, 'input': texts}, timeout=240)
    response.raise_for_status()
    data = response.json()
    vectors = data.get('embeddings')
    if not isinstance(vectors, list) or len(vectors) != len(texts):
        raise RuntimeError('Ollama non ha restituito il numero atteso di embeddings')
    return vectors


def main() -> None:
    sources = sorted(PROCESSED.rglob('*.json'))
    sources = [p for p in sources if not p.name.endswith('.meta.json') and p.name != 'images.json' and not any(part.endswith('_images') for part in p.parts)]
    if not sources:
        sys.exit('Nessun JSON Docling trovato.')
    INDEX.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(INDEX))
    collection = client.get_or_create_collection(name=COLLECTION, metadata={'hnsw:space': 'cosine'})
    session = requests.Session()
    total = 0
    active_ids: set[str] = set()
    for path in sources:
        try:
            doc = json.loads(path.read_text(encoding='utf-8'))
            if not isinstance(doc, dict) or 'texts' not in doc or 'body' not in doc:
                print(f'SALTO (non Docling): {path.name}', flush=True)
                continue
            chunks = make_chunks(doc, path)
            if not chunks:
                print(f'SALTO (nessun testo): {path.name}', flush=True)
                continue
            rel = str(path.relative_to(PROCESSED))
            ids, documents, metadata = [], [], []
            for idx, chunk in enumerate(chunks):
                cid = hashlib.sha256(f'{rel}|{idx}|{chunk["text"]}'.encode()).hexdigest()[:32]
                ids.append(cid)
                active_ids.add(cid)
                documents.append(chunk['text'])
                metadata.append({
                    'source': rel,
                    'source_pdf': str((BASE / 'knowledge/sources' / rel).with_suffix('.pdf')),
                    'page': chunk['page'],
                    'section': chunk['heading'],
                    'text_refs_json': json.dumps(chunk['refs'], ensure_ascii=False),
                    'figures_json': json.dumps(chunk['figures'], ensure_ascii=False),
                })
            for start in range(0, len(ids), 12):
                end = start + 12
                vectors = embed(documents[start:end], session)
                collection.upsert(ids=ids[start:end], documents=documents[start:end], metadatas=metadata[start:end], embeddings=vectors)
            total += len(ids)
            print(f'OK {rel}: {len(ids)} blocchi, {len(page_figures(path))} pagine con figure', flush=True)
        except Exception as exc:
            print(f'ERRORE {path}: {exc}', file=sys.stderr, flush=True)
            sys.exit(1)
    # Only remove stale records after a fully successful pass.
    existing = collection.get(include=[])['ids']
    stale = [cid for cid in existing if cid not in active_ids]
    for start in range(0, len(stale), 500):
        collection.delete(ids=stale[start:start + 500])
    print(f'INDICE COMPLETATO: {total} blocchi, {collection.count()} presenti, {len(stale)} obsoleti rimossi')
    print(f'Database: {INDEX}')


if __name__ == '__main__':
    main()
