#!/usr/bin/env python3
"""Diagnosi read-only della copertura dei passaggi sull'ampiezza nel corpus Glerean."""
import json
import re
import chromadb

DB = '/opt/football-data-lab/knowledge/rag/chroma'
COLL = 'dribbling_tactics_v4_qwen3_embedding_06b'
SOURCE = '334_principi_Glerean'
TERMS = [r'ampiezza', r'si allargano', r'si allungano', r'attaccanti esterni', r'attaccanti laterali', r'sovrapposizion', r'linee laterali', r'spazi laterali']

def heading(m):
    raw = m.get('headings', '[]')
    try:
        val = json.loads(raw) if isinstance(raw, str) else raw
        return ' / '.join(map(str, val)) if isinstance(val, list) else str(val)
    except (ValueError, TypeError):
        return str(raw)

def main():
    c = chromadb.PersistentClient(path=DB).get_collection(COLL)
    rows = c.get(where={'source': SOURCE}, include=['documents', 'metadatas'])
    print(f'COLLECTION: {COLL} | FRAMMENTI GLEREAN: {len(rows["ids"])}', flush=True)
    matches = []
    for cid, doc, meta in zip(rows['ids'], rows['documents'], rows['metadatas']):
        hits = [term for term in TERMS if re.search(term, doc, flags=re.I)]
        if hits:
            matches.append((cid, doc, meta, hits))
    print(f'FRAMMENTI CON TERMINI MIRATI: {len(matches)}', flush=True)
    for cid, doc, meta, hits in matches:
        print('\n' + '=' * 95)
        print('ID:', cid)
        print('SEZIONE:', heading(meta))
        print('TERMINI:', ', '.join(hits))
        for line in doc.splitlines():
            if any(re.search(t, line, flags=re.I) for t in TERMS):
                print('PASSAGGIO:', line.strip()[:850])
    print('\nFINE: sola lettura, nessuna modifica.')

if __name__ == '__main__':
    main()
