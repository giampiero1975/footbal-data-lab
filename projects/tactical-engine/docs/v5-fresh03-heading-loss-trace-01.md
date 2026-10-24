# V5-FRESH03-HEADING-LOSS-TRACE-01

Data: 2026-10-24. Stato: DIAGNOSI PARZIALE; causa tecnica precisa DA CONFERMARE su VPS.

## Attività

Confrontare la pagina 4 del manuale sorgente con i chunk già censiti, localizzare nel codice il passaggio che conserva o associa le intestazioni e predisporre una verifica read-only del confine estrazione → chunking → metadati.

## Script

- Script inventory già eseguito sulla VPS: `scripts/inspect_v5_fresh03_manual_v1.py`.
- Script mirato da eseguire una volta sulla VPS: `scripts/inspect_v5_fresh03_heading_loss_v1.py`.
- Ispezione statica del codice: `scripts/ingest_pdfs.py` e `scripts/build_rag_index_v5_multisource.py`.
- Nessun retrieval, embedding, reranking o generazione eseguito in questa attività.

## Commit

- Script diagnostico read-only: `391baf6023461f5184be6598196d1210b14046f3`.
- La raccolta `dribbling_tactics_v5_multisource` non è stata aperta o modificata dall'ambiente locale.

## Report

Questo documento registra il confronto locale del PDF originale e del JSON dell'inventario VPS già fornito, oltre al percorso nel codice. L'output del nuovo trace deve essere allegato/registrato dopo la singola esecuzione VPS.

## Risultato

La pagina 4 del PDF originale ha la sezione `9. Differenze tra moduli`; le righe `4-3-3`, `4-4-2`, `3-5-2` e `3-4-2-1` precedono ciascuna il rispettivo paragrafo. Il confronto con l'inventario esistente conferma quattro chunk senza intestazione, identificati dai prefissi `d7ced9a0`, `c4559848`, `c1ab686a` e `4a924438`. L'inventario VPS già registrava 62 chunk e conteggio Chroma 5319 prima/dopo.

Nel codice, `ingest_pdfs.py` esporta direttamente Markdown e struttura JSON da Docling. Il builder V5 passa il documento a `HybridChunker`, usa `chunker.contextualize(chunk)` per il testo indicizzato e registra `chunk.meta.headings` separatamente nei metadati. Non è presente una rimozione esplicita di queste quattro stringhe. Il punto osservabile di perdita è quindi la disponibilità/associazione della gerarchia Docling al `HybridChunker`; il codice e gli artefatti attualmente registrati non provano se l'origine sia la classificazione Docling degli elementi o la successiva relazione di sezione nel chunker.

Il nuovo trace legge, senza scrivere, gli elementi di pagina 4 del JSON Docling (testo, label, parent e riferimento), i chunk V5 di pagina 4 (testo e `headings`) e controlla che il conteggio della raccolta resti 5319. Nella copia di lavoro mancano Docling e Chroma: non è stato possibile eseguire localmente quel trace né produrre una nuova osservazione VPS.

## Decisione

La correzione di comportamento non è ancora tecnicamente giustificata: manca l'evidenza che distingue un heading non riconosciuto in estrazione da un heading riconosciuto ma non propagato nel chunk. Eseguire una sola volta il trace sulla VPS e scegliere la patch sul confine effettivamente dimostrato. Preservare la raccolta V5 congelata; ogni eventuale validazione della correzione dovrà usare un artefatto/indice shadow separato, senza ripetere il benchmark equivalente o rigenerare risposte.

## Stato

Diagnosi parziale ESEGUITA; causa radice DA CONFERMARE; correzione funzionale NON IMPLEMENTATA; nessuna validazione, integrazione o certificazione dichiarata. Il solo controllo nuovo eseguito localmente è la compilazione sintattica dello script diagnostico (`py_compile`); nessun test applicativo.

## Operazione VPS necessaria

Dal repository aggiornato, usare il venv già configurato e il JSON Docling già presente in `knowledge/processed`, poi eseguire:

```bash
python scripts/inspect_v5_fresh03_heading_loss_v1.py \
  --processed-json knowledge/processed/<percorso-relativo>/FOOTBALL_DATA_LAB_Transizioni_Offensive_e_Difensive_Manuale.json \
  --output evaluation/v5_fresh03_heading_loss_trace_v1.json
```

Il percorso effettivo va risolto dal file `.json` esistente relativo al PDF; il comando non reingestisce il PDF e non scrive nella raccolta. Dopo l'esecuzione, verificare nell'output `index_unchanged=true`, i quattro `module_body_matches` e le label/parent degli elementi corrispondenti alle intestazioni. Se il trace conferma i 5319 record, il risultato può essere aggiunto a questo report e usato per la patch mirata.
