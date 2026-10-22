# RAG V5 — Chiusura campagna diagnostica (22 ottobre 2026)

## Ambito e decisione
**Campagna diagnostica V5: CHIUSA.** **Certificazione holdout indipendente: NON SUPERATA / NON ESEGUITA**; non dichiarare PASS 9/10 certificato, non promuovere automaticamente V5 in produzione. Giudizio esperto orientativo discusso in chat: **9/10 qualitativo**, non metrica gold.

## Evidenze e risultati già acquisiti
- Diagnostico prospettico: `rag_v5_prospective_diagnostic_v1.json`, 10 risposte generate, 0 identificativi citazione invalidi; collection `dribbling_tactics_v5_multisource` 5319 record prima e dopo; circa 1240,64 s totali. Report fornito in chat, non attestato come artefatto committato né come accesso diretto SSH.
- Pipeline dichiarata nel report: dense24 → reranker mMARCO CPU → collapse exact-alias → top8; modello `qwen3.5:9b`.
- Revisione qualitativa preliminare delle 10 risposte eseguita in chat: esiti coerenti per 03,05,10; attenzione a pertinenza/attribuzione 01,04,07,09; astensione prudente 06,08. La domanda 02 è stata contestata come formulazione di benchmark e **non va trattata come FAIL del RAG senza revisione del quesito**. Questa è una valutazione preliminare, non un'audizione claim-by-claim indipendente.
- Revisione atomica storica già conclusa in `docs/rag-v5-phase-passage-atomic-adjudication-20261022.md`: holdout_06 REVIEW, holdout_10 FAIL. **Casi development, non ripetere e non riutilizzare come gold indipendente.**
- Protocollo già presente: `docs/rag-v5-quality-9of10-validation-protocol-v1.md` e `docs/rag-v5-quality-prospective-grounding-gate-20261022.md`. Non ricreare rubriche o rifare gli stessi diagnostici.

## Check di chiusura
- [x] Report diagnostico letto e interpretato.
- [x] Sintassi citazioni e stabilità numerica indice verificate sul JSON.
- [x] Risposte e criticità qualitativamente esaminate; giudizio 9/10 **indicativo**, non certificato.
- [x] Test diagnostici e vecchi holdout congelati come evidenza storica; nessun rerun autorizzato senza cambiamenti.
- [x] Nessuna modifica a V4, Chroma o prompt richiesta per questa chiusura documentale.
- [ ] Gold indipendente: fonti/pagine puntuali, claim e revisore validati **prima** dell'esecuzione.
- [ ] Freeze manifest indipendente con hash, configurazione, codice, versione modello.
- [ ] Singola esecuzione nuova sul gold effettivamente indipendente e adjudication in cieco.
- [ ] Confronto V4/V5 controllato e decisione finale di promozione secondo protocollo.

## Distinzione vincolante
Il manifest `evaluation/rag_v5_prospective_holdout_candidate_v1.json` reca `candidate_source_aligned_not_frozen`, `freeze.status=blocked_pending_verified_source_pages`, `sha256=null`, `reviewer=null`. Le 10 domande **già eseguite e lette** non possono diventare retroattivamente holdout indipendente. Conservarle come regressione; eventuale gold nuovo va fissato prima di generare risposte.

## Prossima attività senza duplicazioni
Per la certificazione successiva usare solo evidenze nuove e non esaminate, verificare le pagine già mappate su Drive senza rifare analisi precedenti, fissare revisore e hash, poi un solo run read-only e confronto V4/V5. Non riaprire la campagna diagnostica V5 conclusa.
