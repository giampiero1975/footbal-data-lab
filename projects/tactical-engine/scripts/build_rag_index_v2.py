#!/usr/bin/env python3
"""Indicizzazione Docling -> LlamaIndex -> Ollama -> Chroma (collezione V2).

Dry-run predefinito: nessuna modifica a Chroma, nessun embedding.
"""
import argparse
import hashlib
import json
import statistics
from pathlib import Path

import chromadb
from docling.chunking import HybridChunker
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
from transformers import AutoTokenizer
from docling_core.types.doc import DoclingDocument
from pydantic import ValidationError
from llama_index.core import Document, Settings, StorageContext, VectorStoreIndex
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.node_parser.docling import DoclingNodeParser
from llama_index.vector_stores.chroma import ChromaVectorStore

ROOT = Path('/opt/football-data-lab')
PROCESSED = ROOT / 'knowledge/processed/formations-and-systems'
CHROMA = ROOT / 'knowledge/rag/chroma'
COLLECTION = 'dribbling_tactics_v2'
OLLAMA_URL = 'http://127.0.0.1:11434'
EMBED_MODEL = 'nomic-embed-text'
TOKENIZER_MODEL = 'nomic-ai/nomic-embed-text-v1.5'
CHUNK_MAX_TOKENS = 512


def stable_id(i, node):
    return hashlib.sha256(f'{node.id_}:{i}'.encode('utf-8')).hexdigest()


def build_nodes(files):
    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_MODEL, trust_remote_code=True)
    chunker = HybridChunker(
        tokenizer=HuggingFaceTokenizer(tokenizer=tokenizer, max_tokens=CHUNK_MAX_TOKENS),
        merge_peers=True,
    )
    print(f'Tokenizer: {TOKENIZER_MODEL}; limite chunk: {CHUNK_MAX_TOKENS} token')
    parser = DoclingNodeParser(
        chunker=chunker,
        include_metadata=True,
        include_prev_next_rel=True,
        id_func=stable_id,
    )
    result = []
    for path in files:
        payload = json.loads(path.read_text(encoding='utf-8'))
        try:
            docling_doc = DoclingDocument.model_validate(payload)
        except ValidationError:
            print(f'SALTATO (non è un documento Docling): {path.name}')
            continue
        # Il parser ufficiale richiede Document.text contenente il JSON Docling.
        source = str(path.relative_to(ROOT / 'knowledge/processed'))
        input_doc = Document(
            text=docling_doc.model_dump_json(),
            id_=hashlib.sha256(source.encode('utf-8')).hexdigest(),
            metadata={'source': source},
        )
        nodes = parser.get_nodes_from_documents([input_doc])
        for n in nodes:
            # Il parser ufficiale imposta metadata dal chunk: aggiungiamo solo
            # un identificativo di provenienza, senza modificare il chunking.
            n.metadata['source'] = source
            n.metadata['source_pdf'] = docling_doc.origin.filename if docling_doc.origin else path.stem + '.pdf'
            # Chroma accetta metadati scalari: quelli Docling strutturati
            # vengono serializzati, senza perdere i riferimenti originali.
            for key, value in list(n.metadata.items()):
                if isinstance(value, (dict, list)):
                    n.metadata[key] = json.dumps(value, ensure_ascii=False, default=str)
                elif value is None:
                    del n.metadata[key]
            # Non inserire JSON dei metadati nel testo usato per embedding/LLM.
            n.excluded_embed_metadata_keys = list(n.metadata.keys())
            n.excluded_llm_metadata_keys = list(n.metadata.keys())
        print(f'{source}: {len(nodes)} nodi')
        result.extend(nodes)
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--write', action='store_true', help='Crea/aggiorna la collezione V2 (default: dry-run)')
    ap.add_argument('--source', help='Nome del JSON da elaborare, es. il_3412_Giustinetti.json')
    args = ap.parse_args()

    files = sorted(PROCESSED.glob('*.json'))
    if args.source:
        files = [p for p in files if p.name == args.source]
    if not files:
        ap.error('Nessun JSON Docling trovato')

    nodes = build_nodes(files)
    if not nodes:
        ap.error('Nessun nodo generato')
    lengths = [len(n.text) for n in nodes]
    print('Totale nodi:', len(nodes))
    print('Lunghezze (caratteri) min/mediana/media/max:', min(lengths),
          statistics.median(lengths), round(statistics.mean(lengths)), max(lengths))
    print('Sotto 180 caratteri:', sum(x < 180 for x in lengths))
    print('Primo nodo:', repr(nodes[0].text[:160]))
    print('Chiavi metadati:', sorted(nodes[0].metadata.keys()))

    if not args.write:
        print('DRY RUN: nessun embedding generato, nessun database modificato.')
        return

    client = chromadb.PersistentClient(path=str(CHROMA))
    collection = client.get_or_create_collection(name=COLLECTION, metadata={'hnsw:space': 'cosine'})
    Settings.embed_model = OllamaEmbedding(model_name=EMBED_MODEL, base_url=OLLAMA_URL)
    store = ChromaVectorStore(chroma_collection=collection)
    storage = StorageContext.from_defaults(vector_store=store)
    VectorStoreIndex(nodes=nodes, storage_context=storage, embed_model=Settings.embed_model,
                     show_progress=True, insert_batch_size=12)
    print(f'Indicizzazione completata: {COLLECTION}; record attuali: {collection.count()}')
    print('Nota: --write aggiorna i nodi con ID stabili ma non rimuove eventuali nodi obsoleti.')


if __name__ == '__main__':
    main()
