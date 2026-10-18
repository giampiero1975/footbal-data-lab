#!/usr/bin/env python3
"""DRIBBLING V5 experimental structured claims + exact evidence validation.
Read-only ChromaDB. One Ollama generation. No new dependencies.
"""
import json
import re
import time
from pathlib import Path

import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.core.vector_stores import MetadataFilter, MetadataFilters
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.postprocessor.sbert_rerank import SentenceTransformerRerank
from llama_index.vector_stores.chroma import ChromaVectorStore

DB = '/opt/football-data-lab/knowledge/rag/chroma'
COLLECTION = 'dribbling_tactics_v4_qwen3_embedding_06b'
SOURCE = '334_principi_Glerean'
QUESTION = 'Come si sviluppa l’ampiezza offensiva nel 3-3-4 di Glerean?'
OUTPUT = Path('/opt/football-data-lab/projects/tactical-engine/test_v5_strutturato.json')


def extract_json(text):
    text = text.strip()
    text = re.sub(r'^```(?:json)?\s*|\s*```$', '', text, flags=re.I)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        decoder = json.JSONDecoder()
        for pos, char in enumerate(text):
            if char == '{':
                try:
                    obj, _ = decoder.raw_decode(text[pos:])
                    return obj
                except json.JSONDecodeError:
                    pass
        raise ValueError('Nessun JSON valido nella risposta del modello')


def normalize(s):
    return ' '.join(str(s).split())


def main():
    collection = chromadb.PersistentClient(path=DB).get_collection(COLLECTION)
    if collection.count() != 86:
        raise RuntimeError(f'Collection inattesa: {collection.count()} record (attesi 86)')
    index = VectorStoreIndex.from_vector_store(
        ChromaVectorStore(chroma_collection=collection),
        embed_model=OllamaEmbedding(model_name='qwen3-embedding:0.6b', base_url='http://127.0.0.1:11434'),
    )
    retriever = index.as_retriever(
        similarity_top_k=15,
        filters=MetadataFilters(filters=[MetadataFilter(key='source', value=SOURCE)]),
    )
    reranker = SentenceTransformerRerank(
        model='cross-encoder/mmarco-mMiniLMv2-L12-H384-v1', top_n=10, device='cpu'
    )
    from llama_index.core.schema import QueryBundle
    query = QueryBundle(QUESTION)
    nodes = reranker.postprocess_nodes(retriever.retrieve(query), query_bundle=query)
    sources = []
    for i, n in enumerate(nodes, 1):
        metadata = n.node.metadata
        sources.append({
            'numero': i,
            'chunk_id': n.node.node_id,
            'source': metadata.get('source'),
            'chunk_index': metadata.get('chunk_index'),
            'page_numbers': metadata.get('page_numbers'),
            'headings': metadata.get('headings'),
            'testo': n.node.get_content(),
        })
    context = '\n\n'.join(f"SOURCE {s['numero']}\n{s['testo']}" for s in sources)
    prompt = (
        'Sei DRIBBLING, analista tattico. Usa SOLO le fonti fornite, senza conoscenze esterne.\n'
        'Rispondi ESCLUSIVAMENTE con un oggetto JSON valido, senza markdown, con questa struttura:\n'
        '{"affermazioni":[{"testo":"affermazione tattica specifica",'
        '"fonte":1,"estratto":"citazione letterale ESATTA dalla SOURCE indicata"}]}\n'
        'Per ciascuna affermazione usa UNA fonte numerata e un estratto testuale copiato '
        'letteralmente dalla stessa fonte. Non inventare estratti. '
        'Distingui esplicitamente nostra zona difensiva, centrocampo e zona di attacco SOLO '
        'se documentate. Distingui centrocampisti esterni, attaccanti esterni e centrali. '
        'Non confondere zona difensiva nostra con quella avversaria. '
        'Non inferire contenuti dalle figure, non analizzate visivamente. '
        'Non aggiungere conclusioni di prevalenza se non esplicite nelle fonti.\n\n'
        f'DOMANDA: {QUESTION}\n\nFONTI:\n{context}\n\nJSON:'
    )
    llm = Ollama(model='qwen3.5:9b', base_url='http://127.0.0.1:11434',
                 request_timeout=900.0, temperature=0.1, context_window=8192, thinking=False)
    print('Generazione strutturata V5 in corso (una chiamata Ollama)...', flush=True)
    started = time.monotonic()
    raw = str(llm.complete(prompt))
    elapsed = time.monotonic() - started
    result = {'domanda': QUESTION, 'tempo_secondi': round(elapsed, 1),
              'modello': 'qwen3.5:9b', 'fonti': sources, 'risposta_grezza': raw,
              'affermazioni_verificate': [], 'errore_parsing': None}
    try:
        obj = extract_json(raw)
        claims = obj.get('affermazioni', [])
        if not isinstance(claims, list):
            raise ValueError('affermazioni non è una lista')
        for claim in claims:
            if not isinstance(claim, dict):
                result['affermazioni_verificate'].append({'dato': claim, 'esito': 'FORMATO_NON_VALIDO'})
                continue
            number = claim.get('fonte')
            quote = claim.get('estratto', '')
            try:
                number = int(number)
            except (TypeError, ValueError):
                number = -1
            if not 1 <= number <= len(sources):
                status = 'FONTE_INESISTENTE'
            elif not isinstance(quote, str) or not quote.strip():
                status = 'ESTRATTO_MANCANTE'
            elif normalize(quote) not in normalize(sources[number - 1]['testo']):
                status = 'ESTRATTO_NON_PRESENTE_NELLA_FONTE'
            else:
                status = 'ESTRATTO_PRESENTE_SEMANTICA_NON_VERIFICATA'
            result['affermazioni_verificate'].append({**claim, 'esito': status})
    except (ValueError, json.JSONDecodeError) as exc:
        result['errore_parsing'] = str(exc)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Completato in {elapsed:.1f}s | affermazioni: {len(result["affermazioni_verificate"])}', flush=True)
    print(f'Report: {OUTPUT}', flush=True)
    print('NOTA: un estratto presente NON dimostra automaticamente la correttezza semantica.', flush=True)


if __name__ == '__main__':
    main()
