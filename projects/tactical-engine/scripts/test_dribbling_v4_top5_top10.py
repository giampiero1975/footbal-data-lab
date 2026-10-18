#!/usr/bin/env python3
"""DRIBBLING V4: confronto top5/top10, LlamaIndex CitationQueryEngine (sola lettura)."""
import argparse
import json
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

DB = '/opt/football-data-lab/knowledge/rag/chroma'
COLLECTION = 'dribbling_tactics_v4_qwen3_embedding_06b'
SOURCE = '334_principi_Glerean'
QUESTION = 'Come si sviluppa l’ampiezza offensiva nel 3-3-4 di Glerean?'
GOLD = {
    'f897ecc2c11e': 'Ampiezza centrocampisti con palla in difesa',
    '43c85faf1870': 'Ampiezza esterni con palla a centrocampo',
    '5319d503a8ec': 'Profondita e ampiezza attaccanti laterali',
}
QA = PromptTemplate(
    'Sei DRIBBLING, analista tattico del calcio. Rispondi in italiano.\n'
    'Usa esclusivamente le fonti numerate. Non integrare con conoscenze esterne.\n'
    'Descrivi distintamente i comportamenti tattici nelle diverse zone del campo, '
    'solo se documentati nelle fonti. Non confondere Glerean e Gustinetti.\n'
    'Cita le affermazioni con [numero]. Se manca un dettaglio, dichiaralo.\n'
    'Le figure non sono state analizzate visivamente.\n\n'
    'FONTI:\n{context_str}\n\nDOMANDA: {query_str}\n\nRISPOSTA:'
)
REFINE = PromptTemplate(
    'Sei DRIBBLING. Rispondi alla domanda usando esclusivamente le fonti.\n'
    'DOMANDA: {query_str}\nRISPOSTA PRECEDENTE: {existing_answer}\n'
    'NUOVE FONTI:\n{context_msg}\n\n'
    'Integra eventuali nuovi dettagli pertinenti senza perdere quelli gia documentati. '
    'Mantieni citazioni [numero] corrette; non inventare informazioni.\nRISPOSTA AGGIORNATA:'
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='/opt/football-data-lab/projects/tactical-engine/risposte_v4_top5_top10.txt')
    args = parser.parse_args()

    collection = chromadb.PersistentClient(path=DB).get_collection(COLLECTION)
    print(f'Collection: {COLLECTION} | record: {collection.count()} | source: {SOURCE}', flush=True)
    if collection.count() != 86:
        raise RuntimeError('Collection V4 inattesa: attesi 86 record')
    index = VectorStoreIndex.from_vector_store(
        ChromaVectorStore(chroma_collection=collection),
        embed_model=OllamaEmbedding(model_name='qwen3-embedding:0.6b', base_url='http://127.0.0.1:11434'),
    )
    filters = MetadataFilters(filters=[MetadataFilter(key='source', value=SOURCE)])
    llm = Ollama(model='qwen3.5:9b', base_url='http://127.0.0.1:11434',
                 request_timeout=900.0, temperature=0.1, context_window=8192, thinking=False)
    sections = []
    for top in (5, 10):
        print(f'\n=== TEST top {top} ===', flush=True)
        retriever = index.as_retriever(similarity_top_k=15, filters=filters)
        reranker = SentenceTransformerRerank(
            model='cross-encoder/mmarco-mMiniLMv2-L12-H384-v1',
            top_n=top, device='cpu',
        )
        engine = CitationQueryEngine.from_args(
            index=index, retriever=retriever, llm=llm,
            node_postprocessors=[reranker],
            citation_chunk_size=2048, citation_chunk_overlap=0,
            citation_qa_template=QA, citation_refine_template=REFINE,
            response_mode='compact',
        )
        started = time.monotonic()
        response = engine.query(QUESTION)
        elapsed = time.monotonic() - started
        nodes = list(response.source_nodes or [])
        gold_found = {}
        lines = [f'=== TOP {top} ===', f'Domanda: {QUESTION}', f'Tempo: {elapsed:.1f}s',
                 '\nRISPOSTA:\n' + str(response), '\nFONTI RESTITUITE DAL CITATION ENGINE:']
        for i, n in enumerate(nodes, 1):
            content = n.node.get_content()
            metadata = n.node.metadata or {}
            original_id = n.node.node_id
            for prefix, label in GOLD.items():
                if original_id.startswith(prefix):
                    gold_found[prefix] = label
            lines.append(f'[{i}] id={original_id} | source={metadata.get("source", "?")} '
                         f'| score={n.score}\n{content}')
        cites = [int(v) for v in re.findall(r'\[(\d+)\]', str(response))]
        invalid = sorted(set(cites) - set(range(1, len(nodes) + 1)))
        lines.append(f'\nCitazioni: {cites}; citazioni fuori intervallo: {invalid}')
        lines.append('NOTA: CitationQueryEngine puo suddividere i nodi e riassegnare gli ID; '
                     'la verifica GOLD basata sugli ID delle fonti di risposta non e affidabile. '
                     'Verificare il testo dei passaggi riportati qui sopra.')
        section = '\n'.join(lines)
        sections.append(section)
        Path(args.output).write_text('\n\n'.join(sections) + '\n', encoding='utf-8')
        print(f'Tempo: {elapsed:.1f}s | fonti: {len(nodes)} | citazioni fuori intervallo: {invalid}', flush=True)
        print('RISPOSTA:\n' + str(response), flush=True)
        print(f'Report aggiornato: {args.output}', flush=True)
    print('\nFINE: nessuna modifica agli indici.', flush=True)


if __name__ == '__main__':
    main()
