# RAG V5 — revisione diagnostica candidate v2 (2026-10-23)

## Natura e limiti
Revisione **non indipendente** del report VPS `rag_v5_candidate_v2_runtime_report.json` caricato in conversazione, confrontato con `evaluation/rag_v5_independent_candidate_v2.json` e `docs/rag-v5-quality-9of10-validation-protocol-v1.md`. Il manifest è `source_verified_candidate_not_frozen`, revisori null. Nessuna certificazione 9/10, nessun tuning sul candidato, nessun nuovo run. Non modificati indice, V4, manifest o prompt.

## Esecuzione (dal report)
- 10/10 generazioni; `qwen3.5:9b`; `dense24 -> mMARCO CPU -> exact-alias chunk collapse -> top8`.
- Chroma `dribbling_tactics_v5_multisource`: 5319 -> 5319, `index_unchanged=true`.
- 0 ID citazioni formalmente invalidi, ma controllo **solo sintattico**.
- Latenza somma `elapsed_seconds`: 1099.08 s (~18m19s); media 109.91 s; minimo 63.77 s (05), massimo 139.25 s (06). Non confondere con sola durata generazione.

## Adjudication preliminare per domanda
Esiti **diagnostici**, non rubric indipendente: `OK-P` = requisiti principali soddisfatti apparentemente; `FAIL-P` = almeno un difetto materiale; `REVIEW` = verifica semantica ancora necessaria.

| ID | Esito | Riscontro | Diagnosi |
|---|---|---|---|
| fresh_01 | FAIL-P | Individua zone alta/centrale/bassa, ma nega l'affermazione qualitativa di Ussia sulla maggiore efficacia della zona alta, esplicitamente vietato dal manifest; per esercitazione 8 usa anche una fonte omonima di De Rosa. | Passaggi Ussia mancanti nel top8; confusione tra esercitazioni con stesso numero di autori diversi; risposta su contesto insufficiente. |
| fresh_02 | OK-P | Fonte Ussia F1 pagine 10-11: correre nello spazio di destinazione, impedire sei passaggi, riconquistare. | Buon recupero e ancoraggio diretto. |
| fresh_03 | FAIL-P | Coglie correttamente che un assetto statico non dimostra causalità, ma non richiama i quattro moduli richiesti dal gold (4-3-3, 4-4-2, 3-5-2, 3-4-2-1); fonte primaria manuale transizioni non presente. | Mancato recupero fonte primaria e incompletezza; argomentazione collaterale. |
| fresh_04 | FAIL-P | Risponde che il vincolo non è disponibile; manifest richiede **cinque secondi** come regola dell'esercitazione 4/A. Nel top8 compare soltanto l'indice Ussia pagina 48. | Retrieval/rerank seleziona indice al posto del passaggio della pagina 14; astensione prudente ma non soddisfa la domanda. |
| fresh_05 | OK-P | Cita manuale interno sul lato debole libero fuori/protetto dentro e obiettivi di 1v1, cross preparato, mezzo spazio. | Risposta ben supportata. |
| fresh_06 | REVIEW | Fonte Ussia F1 contiene partenza 11>0 e inserimento 1-2 avversari fino a 10>10; risposta include dettagli da fonti non necessarie. **Attenzione:** estratto F1 denomina il corner come figure 12/A-12/B mentre la domanda lo chiama esercitazione 11/A: verificare la corrispondenza nel gold, senza correggere silenziosamente. | Risposta sostanzialmente pertinente, ma source mapping della domanda e contaminazione da fonti esterne richiedono controllo. |
| fresh_07 | FAIL-P | Nessun estratto Foscarini nel top8; modello tratta zona B di Indiani (area di porta, palle inattive) come se fosse la zona B di Foscarini e interpreta 'laterali' come rimesse laterali. | Errore grave di disambiguazione autore, zona e concetto; retrieval failure con allucinazione di attribuzione. |
| fresh_08 | FAIL-P | Fonte Foscarini F1 corretta su centrocampo/playmaker, ma risposta incorpora `80% delle reti` dalla zona B di Indiani [F3] come se fosse pertinente alla zona B di Foscarini. | Contaminazione multisorgente e attribuzione scorretta malgrado presenza fonte corretta. |
| fresh_09 | REVIEW | Principali condizioni di consolidamento presenti e citate (difesa ripiegata, recuperatore pressato, sostegni assenti, risultato); mescola inoltre principi di ripiegamento difensivo e di pressing al consolidamento del possesso dopo recupero. | Possibile slittamento di fase in affermazioni accessorie; serve verifica puntuale rubric. |
| fresh_10 | REVIEW | Condizioni favorevoli e limite di universalità esposti; fonte Ussia diretta assente, citazione principale è manuale interno che descrive Ussia. | Risposta apparentemente pertinente ma confronto primario-secondario non pienamente tracciato. |

**Risultato prudenziale:** 2 OK-P, 5 FAIL-P, 3 REVIEW. **Non** interpretare come score ufficiale: senza revisore indipendente e gold congelato non esiste un PASS certificato.

## Cause e interventi proposti (non ancora applicati)
1. **Priorità P0 — entity/source grounding:** domande che nominano autore/documento/esercitazione devono conservare autore, titolo e identificatore come vincoli del retrieval; evitare che un'altra `zona B` o `esercitazione 8` venga spacciata per quella richiesta. Considerare filtri metadata Chroma **solo se il campo è effettivamente presente e verificato**, con fallback esplicito e tracciato. Non assumere che i metadati permettano già un filtro specifico.
2. **Priorità P0 — completezza delle evidenze:** su fresh_01/04/07 recuperare prima i passaggi obbligatori e le pagine note; non basta il top8 globale; l'indice di Ussia pagina 48 non sostituisce l'esercitazione 4/A.
3. **Priorità P0 — separazione dei contesti:** indicare chiaramente fonte e autore per ogni zona/figura; vietare fusioni semantiche tra autori quando condividono etichette generiche. Il modello ha fallito fresh_08 pur disponendo di Foscarini F1.
4. **Priorità P1 — valutazione:** eseguire adjudication indipendente sui claim, senza utilizzare questo candidato per tuning e senza proclamare 9/10. Per una modifica del retrieval, usare regression suite di sviluppo e poi **nuovo** holdout prospettico.
5. **Priorità P1 — prestazioni:** conservare la baseline di latenza 1099.08 s, evitando di confondere CPU rerank e durata generazione; confronti solo su condizioni equivalenti.

## Fonti ufficiali consultate (2026-10-23)
- Chroma Query/Get: https://docs.trychroma.com/docs/querying-collections/query-and-get — `query_embeddings`, `n_results`, `where` e `where_document` documentati; `get` non usa similarity ranking.
- Sentence Transformers CrossEncoder: https://www.sbert.net/docs/cross_encoder/usage/usage.html — rerank di candidati e costi per coppia.
- Ollama Chat: https://docs.ollama.com/api/chat — `/api/chat`, `stream`, `think`, `options`, contatori e durate.

## Stato
**VERIFICATO:** file JSON caricato, codice `smoke_test_rag_v5_e2e.py` e manifest letti; fonti ufficiali consultate; revisione preliminare completata. **DOCUMENTATO:** dipendenze runtime e protocolli nei docs del repository. **DA VERIFICARE:** gold indipendente, verifica pagina-esercitazione fresh_06, effettiva disponibilità metadati filtro su Chroma VPS, risultati di eventuali patch e confronto V4/V5. Nessuna esecuzione VPS richiesta in questa fase.
