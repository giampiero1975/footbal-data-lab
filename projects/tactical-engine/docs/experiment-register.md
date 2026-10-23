# Registro autorevole esperimenti — Tactical Engine

Ultimo aggiornamento: 2026-10-23. GitHub è la fonte autorevole dello **stato**; i report runtime sulla VPS sono evidenze da collegare, non automaticamente versionate. Questo registro è obbligatorio per ogni nuova attività.

## Protocollo permanente

**Attività → script → commit → report (percorso + hash se disponibile) → risultato → decisione → stato.**

Prima di avviare qualunque test: cercare in questo registro, nel TODO, nei report e nella cronologia Git gli esperimenti equivalenti. Un rerun richiede una differenza documentata di codice, dataset, ambiente o obiettivo; non ripetere benchmark costosi per ricostruire informazioni già acquisite. Dopo ogni report: analizzarlo e aggiornare registro e TODO **nello stesso ciclo operativo**. Non segnare completato un test solo perché lo script esiste.

### Stati definitivi

- **DA FARE**: non implementato.
- **IMPLEMENTATO**: codice pubblicato, ma senza esito runtime verificato.
- **ESEGUITO**: report di esecuzione disponibile, ancora da valutare.
- **VALIDATO**: risultato esaminato rispetto a criteri dichiarati, con evidenze; limitato all'ambito del test.
- **INTEGRATO**: modifica presente nell'entry point effettivo e regressione verificata.
- **CERTIFICATO**: supera gold indipendente congelato e criteri di promozione.
- **BLOCCATO**: impedimento documentato, con prossimo passo.

Uno stato superiore **non** si deduce dal precedente. In particolare VALIDATO shadow ≠ INTEGRATO e citazioni sintatticamente valide ≠ fedeltà.

## Registro — recupero V5 per fonte/riferimento

| ID | Attività / script | Commit | Report / evidenza | Risultato e decisione | Stato |
|---|---|---|---|---|---|
| V5-SRC-01 | Audit metadata / `audit_v5_source_metadata.py` | `14c7674` | Report audit VPS riferito: 5319/5319 metadata validi | Accettato come prerequisito del filtro fonte; non certifica generazione | VALIDATO |
| V5-SRC-02 | Source retrieval / `rag_v5_source_shadow_v1.py` | `5d916af` | Diagnostica source-aware discussa; percorso/hash non consolidati | Source-filtering valutato in shadow | VALIDATO (shadow) |
| V5-SRC-03 | Source rerank / `rag_v5_source_rerank_shadow_v2.py` | `8db0760` | Report source rerank VPS; hash da acquisire | Migliora casi Foscarini, non risolve Ussia 4/A | VALIDATO (ambito mirato) |
| V5-REF-01 | Exact reference / `rag_v5_exact_reference_shadow_v1.py` | `21cdb18` | `rag_v5_exact_reference_shadow_v1.json`; hash da acquisire | Ussia 4/A recuperato, ma mMARCO lo colloca F5; non integrare ranking grezzo | VALIDATO (diagnostica) |
| V5-REF-02 | Generalizzazione / `rag_v5_reference_generalization_shadow_v1.py` | `547da5c`, fix `eaad637` | `rag_v5_reference_generalization_shadow_v1.json`; hash da acquisire | Parser e riferimenti su 4 nuovi casi, senza generazione | VALIDATO (retrieval) |
| V5-REF-03 | E2E fresh / `rag_v5_fresh_reference_e2e_shadow_v1.py` | `3d10d7f` | `rag_v5_fresh_reference_e2e_shadow_v1.json`; hash da acquisire | Quattro risposte; figura 9 F5, figura 20 con attribuzione imprecisa. Non promuovere | VALIDATO (diagnostica) |
| V5-REF-04 | Priority replay / `rag_v5_reference_priority_shadow_v1.py` | `b570abd` | `rag_v5_reference_priority_shadow_v1.json` fornito in chat 2026-10-23; SHA-256 allegato: `49c6c81d268bf05a1fc43c398daa6a266a6aea53134199186ea80d7e7ad1fb84` (file ricevuto in chat; non ancora archiviato in Git) | 4/B F1, 6/B F1+F2, fig.9 F1, fig.20 F1; stesso top8, nessuna lettura/scrittura Chroma. Risposta fig.20 cita F1, ma attribuisce esplicitamente l'incrocio ai numeri 4 e 3, mentre il testo dice solo che segue allo scambio 4/3: lieve inferenza non garantita; verificare in regressione. **Accettato solo come replay shadow e generazione mirata**, non come certificazione end-to-end | VALIDATO (shadow) |
| V5-REF-05 | Live source-aware retrieval con `--priority-exact` / `rag_v5_fresh_reference_e2e_shadow_v1.py` | `bbb9b7b` | `rag_v5_live_priority_integration_v1.json` (file chat, non Git), SHA-256 `0503e2dcc94be563a7176f0768b869360a6a2465411d4e454688f06fa21512fc` | 4/4 casi con passaggio esatto F1 (6/B anche F2), tutti i top8 invariati come insieme; Chroma 5319→5319; generazione disattivata. Accettata priorità live in shadow; non prova qualità risposta fig20 né integrazione nel candidato locked/produzione | VALIDATO |
| V5-CERT-01 | Gold indipendente V5 | `641f61e`, audit `db9abab` | `evaluation/rag_v5_independent_candidate_v2.json` | Candidato predisposto, revisione indipendente/freeze non attestati | IMPLEMENTATO |
| V5-CERT-02 | Certificazione V5 9/10 e confronto V4 | — | — | Non certificata; non ripetere holdout diagnostici | DA FARE |

## Obblighi di manutenzione

1. Registrare ogni nuovo report con percorso, checksum SHA-256, commit, dataset e parametri quando disponibili. Non inventare digest o versioni.
2. Chiudere le attività nel TODO **solo** se il relativo criterio è dimostrato. Conservare la cronologia qui.
3. Prima di proporre un comando VPS, verificare che non ripeta un esperimento già concluso.
4. Documentare regressioni e rollback prima di modificare un entry point funzionante; non alterare Chroma né baseline V4 senza autorizzazione.
5. Per report disponibili soltanto nella conversazione o sulla VPS, dichiarare esplicitamente la lacuna di archiviazione Git.

## Decisione integrazione controllata — 2026-10-23

- **Attività:** V5-REF-05; **script:** `rag_v5_fresh_reference_e2e_shadow_v1.py --priority-exact`; **commit:** `bbb9b7b`.
- **Report acquisito:** `rag_v5_live_priority_integration_v1.json`, SHA-256 `0503e2dcc94be563a7176f0768b869360a6a2465411d4e454688f06fa21512fc` (allegato in chat, non archiviato Git). **Risultato:** 4/B F1→F1; 6/B F1,F5→F1,F2; fig9 F5→F1; fig20 F1→F1; top8 stesso insieme di ID in 4/4; Chroma 5319→5319, `index_writes=false`, `generation_requested=false`. **Decisione:** VALIDATO limitatamente al riordino live source-aware opt-in. Conservare flag disattivato per default; candidato locked invariato. La qualità della risposta fig20 non è stata valutata da questo report. **Stato:** VALIDATO.
- **Differenza tecnica rispetto ai test già conclusi:** questo script applica la priorità *durante un retrieval live con embedding, filtro fonte e reranker*, non rigioca punteggi salvati. Il successivo test deve limitarsi a verificare questa integrazione, non ripetere la campagna di benchmark.
- **Rollback:** omettere `--priority-exact`; il comportamento precedente è conservato. Non sono previste scritture Chroma.


## V5-REF-06 — Trasferimento nel runner effettivo (2026-10-23)

- **Attività:** inserire priorità esatta nel runner richiamato dal candidato V5.
- **Script:** `scripts/smoke_test_rag_v5_e2e.py`; **commit:** `a0301b6489443ef7ac0a954af981ea09f7704676`.
- **Report:** non disponibile. **Risultato:** opzione `--priority-exact` aggiunta al runner, disattivata per default; lookup esatto limitato a domande con fonte Ussia/Foscarini esplicita; Chroma non scritto.
- **Decisione:** IMPLEMENTATO (runner e wrapper pubblicati). Il forwarding dal wrapper `run_rag_v5_locked_candidate_v2.py` è stato pubblicato nel commit `2a2ceb9409aaa2e35a1ecd7464029037277d575b`; non dichiarare INTEGRATO prima della regressione runtime. Verifica statica e regressione runtime mirata ancora mancanti. Il gold candidato resta immutato.
- **Rollback:** omettere il flag; nessuna migrazione dell'indice.

- **Sblocco 2026-10-23:** wrapper `scripts/run_rag_v5_locked_candidate_v2.py` aggiornato nel commit `2a2ceb9409aaa2e35a1ecd7464029037277d575b`: il flag opt-in è inoltrato al runner; senza flag comportamento precedente. **Stato:** IMPLEMENTATO. Verifica statica e regressione runtime ancora DA FARE; non ripetere benchmark shadow.

### V5-REF-06 preflight mirato

Commit `a8cfef6`: gestione distanze assenti per chunk lessicali e opzioni `--retrieval-only`, `--probe-question` nel runner effettivo. Nessun report runtime disponibile. Stato: IMPLEMENTATO. Prova successiva: una domanda diagnostica, niente gold e niente generazione; verificare F1, indice immutato e assenza errori.

### V5-REF-06 — Esito probe runner effettivo (2026-10-23)

- Attività: regressione mirata del percorso opt-in nel runner effettivo, distinta dai test shadow già conclusi.
- Script: `scripts/smoke_test_rag_v5_e2e.py`, commit `a8cfef6a84d259a78606524f24a61659ca00cfb1`.
- Report: `rag_v5_effective_priority_probe_v1.json`, ricevuto in chat; SHA-256 `e52c802051873703c197e8b28123a580a3b56a2268a2309b11e4d5f764f6bbda`.
- Risultato: Foscarini figura 20 promossa a F1, un candidato esatto, 8 evidenze; Chroma 5319 prima e dopo; retrieval-only, nessuna risposta generata, nessun errore nel report.
- Decisione: VALIDATO per la sola probe del retrieval nel runner effettivo. Il forwarding wrapper è verificato staticamente, non esercitato in questa probe. Nessuna certificazione E2E o qualità della risposta; mantenere opt-in default off.
- Stato: VALIDATO (probe retrieval); integrazione end-to-end del candidato locked ancora DA FARE.

### V5-REF-07 — Verifica risposta nel runner effettivo (2026-10-23)

Attività: verificare la generazione di una sola risposta per Foscarini figura 20 nel runner effettivo con priorità opt-in, dopo probe retrieval VALIDATA V5-REF-06. Script: `scripts/smoke_test_rag_v5_e2e.py`, commit `00c3a7766f1703cc08a415737ad6a06345ddc92e`; la domanda singola è ora ammessa anche con generazione. Report atteso: `rag_v5_effective_priority_answer_fig20_v1.json`. Risultato e decisione in attesa del report VPS. Stato: IMPLEMENTATO. Differenza dal precedente shadow: percorso generativo effettivo dopo dense24, mMARCO, collapse alias e promozione exact; non è benchmark gold.

### V5-REF-07 follow-up

Il report di risposta figura 20 evidenzia attribuzione non supportata del ruolo del giocatore 7. Esito ESEGUITO, accuratezza non VALIDATA. Correzione mirata del prompt nel commit `f22ade7`: vincoli sui ruoli e sui soggetti, senza modificare retrieval. Stato IMPLEMENTATO; attesa verifica differenziale.

### V5-REF-07 verifica differenziale — esito

Script `scripts/smoke_test_rag_v5_e2e.py`, prompt commit `f22ade7`; report `rag_v5_effective_priority_answer_fig20_promptfix_v1.json`, SHA-256 `d2d071ca77ec43b9132fff19a553f191d0e19f17129466f1a715eafb1e81f05a`. Risultato: Foscarini F1, scambio 4/3, incrocio mediani, movimenti 7 e 6 corretti; il 7 non viene piu definito mediano. Citazioni F1/F2/F4 esistenti; F2 e F4 sono digressioni non richieste. Chroma 5319 prima e dopo; 101,8 s. Decisione: VALIDATO per la correzione puntuale dell'attribuzione dei ruoli, non CERTIFICATO come qualita generale o integrazione locked. Nessun nuovo test equivalente.

### V5-CERT-02 — Gate revisione indipendente

Attivita: protocollo per revisione e freeze del candidato v2. Artefatto: `docs/rag-v5-independent-review-gate-v1.md`, commit `0c79578`. Nessuna esecuzione o report. Risultato: checklist pronta; candidato invariato. Decisione: richiedere revisore indipendente e fingerprint runtime prima del freeze. Stato protocollo: IMPLEMENTATO; certificazione: BLOCCATO.

### V5-CERT-02 — Riconciliazione anti-duplicati

Audit autore delle dieci domande fresh_01–fresh_10 gia ESEGUITO il 2026-10-22, come attestato da `source_claim_audit` e `coverage_audit` nel manifest candidato v2. Non ripetere audit, retrieval o generazione. Revisione indipendente distinta: DA FARE, richiede un revisore diverso dall'autore; freeze BLOCCATO fino ad approvazione e fingerprint runtime. Nessuna nuova esecuzione.

### V5-GEM-01 — Revisore Gemini separato

Attivita: integrazione minima del revisore esterno per fresh_01, distinta dall'audit autore ESEGUITO. Script `scripts/review_rag_v5_gemini.py`, commit `ca8383b`; guida `docs/gemini-independent-review-v1.md`, commit `25ef94d`; esclusione credenziali e materiale privato `.gitignore`, commit `24e8ac6`. Report: non ancora generato. Risultato: implementato client REST blind, controllo hash manifest, bundle documentale obbligatorio, validazione citazioni, budget locale e nessun retry o fallback automatico. Decisione: preparare fonte originale Ussia pp21-23 e preflight fresh_01; non eseguire benchmark RAG. Stato: IMPLEMENTATO, prova runtime DA FARE; freeze BLOCCATO.

### V5-GEM-01 — Configurazione credenziali

Attivita: predisposto caricamento chiave da `.env` locale ignorato da Git, senza committare credenziali. Script commit `a80cf34`, template `.env.example` commit `2e0fdf4`, guida commit `5362336`. Report: nessuno; risultato: supporto configurazione IMPLEMENTATO, installazione chiave VPS DA FARE. Decisione: configurare solo sulla VPS e ruotare una chiave eventualmente esposta; nessun test Gemini eseguito. Freeze BLOCCATO.

### V5-GEM-01 — Preparazione fonti fresh_01

Attivita: verificata accessibilita del PDF originale Ussia su Drive e presenza delle pagine interne 21–23; implementato script di estrazione PDF read-only `scripts/prepare_gemini_fresh01_sources.py`, commit `aaa4b28`. Report: nessuno. Risultato: preparazione bundle IMPLEMENTATO, esecuzione e preflight DA FARE. Decisione: richiedere PDF originale locale sulla VPS, estrarre tre pagine con riferimenti verificati, poi preflight senza chiamata Gemini; benchmark e freeze invariati.

### V5-GEM-01 — Bundle Ussia fresh_01 eseguito

Attivita: estrazione originale Ussia pp. 21, 22, 23 dalla VPS. Script: `prepare_gemini_fresh01_sources.py` (`aaa4b28`, import PyMuPDF aggiornato `34ba249`). Commit: precedenti. Report: output VPS `SOURCE_BUNDLE_PREPARED` e SHA256 PDF `6aa542e55dc88527c4d47c0e7696bb8872c71ee262120509e7dbc0fd2e683772`; bundle privato `evaluation/fresh_01_sources.json`. Risultato: ESEGUITO per estrazione, nessun Gemini chiamato. Decisione: preflight read-only `fresh_01` DA FARE; freeze BLOCCATO. Stato: ESEGUITO.

### V5-GEM-01 — Preflight fresh_01

Attivita: preflight locale con fonti Ussia pp.21–23. Script: `review_rag_v5_gemini.py --dry-run` gia implementato. Report: output VPS `preflight=PASS`, manifest SHA256 `f0d36bc5b35ddcfd42bfef234db2380db6a684a9b81fb9cd19ab75bea81755c0`, bundle SHA256 `a1dfdeaf59c25dac15cc9ae4e33033f3d62ea5d657d8ab41e660aab13e240a27`, modello `gemini-3-flash-preview`, blind=true, Ollama outputs sent=false. Risultato: VALIDATO solo preflight, zero chiamate API. Decisione: consentire una singola chiamata Gemini Free Tier fresh_01; freeze BLOCCATO.

### V5-GEM-01 — Prima chiamata Gemini fresh_01

Attivita: revisione blind Gemini 3 Flash con fonte originale Ussia pp21–23. Script: `review_rag_v5_gemini.py` commit `ca8383b` con caricamento env `a80cf34`. Report: `gemini_fresh_01_review_v1.json` allegato, stato BLOCCATO, error_type ValueError, reason `UNVERIFIABLE_QUOTE`, manifest SHA256 `f0d36bc5b35ddcfd42bfef234db2380db6a684a9b81fb9cd19ab75bea81755c0`, bundle SHA256 `a1dfdeaf59c25dac15cc9ae4e33033f3d62ea5d657d8ab41e660aab13e240a27`; ledger VPS 2026-10-23: 1 richiesta registrata. Risultato: risposta Gemini non conservata nel report per errore validazione citazione esatta, giudizio tattico non verificabile. Decisione: non ripetere richiesta; prima diagnosi offline e correzione persistenza diagnostica, senza abbassare gate citazioni. Stato: BLOCCATO. Freeze BLOCCATO.

### V5-GEM-01 — Correzione diagnostica dopo UNVERIFIABLE_QUOTE

Attivita: rendere ispezionabile la risposta Gemini anche se la validazione fallisce. Script: `review_rag_v5_gemini.py`, commit `16b5a08` salva `raw_review` e hash prima del gate; commit `9cc3a53` aggiunge pagina, claim e citazione non corrispondente al motivo BLOCCATO. Report runtime: DA FARE; nessuna nuova richiesta eseguita. Risultato: IMPLEMENTATO; validazione citazioni rigorosa invariata. Decisione: prima verificare modifica, poi eventuale nuova chiamata motivata dalla differenza tecnica, con nome report nuovo e limite quota esplicito; freeze BLOCCATO.

### V5-GEM-01 — Test diagnostico offline

Attivita: regressione senza rete per rifiuto citazioni non presenti e persistenza diagnostica. Script: `scripts/test_gemini_quote_diagnostics_offline.py`; commit `3aefe66`. Report runtime: DA FARE sulla VPS, nessuna richiesta API prevista. Risultato: IMPLEMENTATO; esecuzione e validazione DA FARE. Decisione: eseguire solo test locale, non nuova chiamata Gemini; freeze BLOCCATO.

### V5-GEM-01 — Esito regressione offline

Attivita: controllo locale diagnostica citazioni. Script: `test_gemini_quote_diagnostics_offline.py`, commit `3aefe66`. Report: conferma utente di esito positivo sulla VPS dopo comando previsto `OFFLINE_DIAGNOSTICS_PASS API_REQUESTS=0`; nessun file report persistente del test. Risultato: VALIDATO per il solo test sintetico offline, non per la persistenza end-to-end della risposta API. Decisione: eventuale nuovo tentativo Gemini `fresh_01` consentito solo con output v2, correzione tecnica `16b5a08`/`9cc3a53`, budget giornaliero rispettato; conservare report v1 e freeze BLOCCATO.

### V5-GEM-01 — Seconda risposta Gemini e audit offline

Attivita: richiesta differenziale fresh_01 v2 autorizzata dall'utente con limite locale 2. Script: `review_rag_v5_gemini.py` corretto, commit `16b5a08` e `9cc3a53`. Report: `gemini_fresh_01_review_v2.json` ricevuto; ledger 2026-10-23=2; risposta grezza conservata, Gemini decision PASS, validatore BLOCCATO per citazione abbreviata `Esercitazione 8... pressione alta`. Risultato: ESEGUITO, non VALIDATO. Decisione: nessuna terza chiamata; audit delle 9 evidenze contro bundle originale con script offline `audit_gemini_fresh01_v2_offline.py` commit `6a6a4c2`, che accetta soltanto frammenti letterali ordinati separati da ellissi esplicite e spazi normalizzati. Stato: BLOCCATO in attesa del report audit; freeze BLOCCATO.

### V5-GEM-01 audit fresh_01 2026-10-23

VALIDATO: Gemini PASS, 9/9 evidenze controllate offline, zero API aggiuntive. Report gemini_fresh_01_audit_v2.json. Gli altri nove casi richiedono revisione; freeze BLOCCATO.

### V5-GEM-02 — Riconciliazione casi residui

Attivita: verificati TODO, registro, manifest e protocollo di revisione. Fonti originali Ussia, Foscarini e due manuali interni accessibili su Drive. Report: fresh_01 audit VALIDATO; nessun report indipendente verificato per fresh_02-fresh_10. Risultato: DA FARE per nove revisioni indipendenti. Decisione: preparare bundle paginati senza eseguire RAG; poi revisione cieca Gemini, senza ripetere fresh_01. Stato: DA FARE; freeze BLOCCATO.

### V5-GEM-02 — Preparazione bundle residui

Attivita: preparazione offline di nove bundle privati fresh_02-fresh_10, con riferimenti ai quattro PDF originali. Script: `scripts/prepare_gemini_remaining_sources_v1.py`; commit `7ad9ee6`. Report: non ancora eseguito su VPS. Risultato: IMPLEMENTATO, non VALIDATO. Decisione: verificare pagine stampate dei manuali e Foscarini rispetto agli indici PDF prima di qualunque revisione; nessuna chiamata API, nessuna generazione RAG. Stato: IMPLEMENTATO; freeze BLOCCATO.

### V5-GEM-02 — Diagnosi numerazione Foscarini

Attivita: esecuzione bundle su VPS interrotta `PAGE_NOT_VERIFIED: foscarini 22`; PDF Foscarini ha 11 pagine fisiche. Script: correzione differenziale `fba8b96`, richiede indice PDF esplicito per pagina stampata 22, senza assumere equivalenza. Commit: `fba8b96`. Report: output utente con elenco PDF 1-11. Risultato: ESEGUITO, preparazione BLOCCATO fino a verifica della corrispondenza. Decisione: ispezionare pagina stampata e confermare indice prima di rieseguire; zero chiamate Gemini. Stato: BLOCCATO.

### V5-GEM-02 — Mapping Foscarini verificato

Attivita: verifica paginazione fonte originale Foscarini. Script: diagnostica locale PyMuPDF su prime tre pagine. Commit: script `fba8b96`. Report: PDF pagina 1 termina con numero stampato 21; PDF pagina 2 termina con numero stampato 22. Risultato: VALIDATO mapping pagina stampata 22 = indice PDF 2. Decisione: usare `--foscarini-page-22-pdf-index 2` nel generatore; verificare separatamente la paginazione degli altri manuali. Stato: VALIDATO per il solo mapping Foscarini; freeze BLOCCATO.

### V5-GEM-02 — Bundle privati generati

Attivita: generazione offline fresh_02-fresh_10. Script: `prepare_gemini_remaining_sources_v1.py` commit `fba8b96`. Report: output VPS dell'utente con nove righe PREPARED e API_REQUESTS=0. Risultato: ESEGUITO, non ancora VALIDATO sul contenuto. Decisione: esaminare nove JSON privati, controllare numerazione e copertura delle fonti prima della revisione cieca; non ripetere estrazione. Stato: ESEGUITO; freeze BLOCCATO.

### V5-GEM-02 — Audit preliminare bundle caricati

Attivita: ispezione di sette bundle caricati fresh_02-fresh_08 e confronto con manifest. Script: generatore `fba8b96`; commit TODO `233e7b6`. Report: pagine Ussia 11/14/24, Foscarini 22=PDF2, manuali interni 3-5 con numerazione coerente. Risultato: ESEGUITO controllo preliminare 7/9; non revisione indipendente. Decisione: acquisire fresh_09 e fresh_10, poi completare audit di copertura claim; non effettuare nuove API. Stato: ESEGUITO; freeze BLOCCATO.

### V5-GEM-02 — Correzione mirata fresh_09

Attivita: audit completato sui nove bundle caricati. Script: mapping fresh_09 da pagina 4 a pagina 3, commit `71fe98c`; manifest aggiornato commit `1f64bb7`. Report: il bundle fresh_09 precedente citava pagina 4, mentre sezione 4 Consolidare invece di accelerare e relativi pro/contro si trovano a pagina 3, gia estratta in fresh_10. Risultato: IMPLEMENTATO correzione su GitHub, non ancora ESEGUITO il riallineamento del file privato VPS. Decisione: aggiornare solo fresh_09_sources.json con testo gia verificato, senza nuovi test o API. Stato: IMPLEMENTATO; freeze BLOCCATO.

### V5-GEM-02 — Verifica finale fresh_09

Attivita: conferma JSON pagina 3 e verifica documentazione OpenAI sulle azioni GitHub. Script: fix `71fe98c`; manifest `1f64bb7`. Commit TODO `bd1fba6`. Report: fresh_09 aggiornato su VPS, backup presente, API_REQUESTS=0, file caricato coerente con sezione 4. Risultato: VALIDATO allineamento documentale. Decisione: non ripetere estrazioni; revisione indipendente ancora DA FARE. I blocchi intermittenti delle scritture sono compatibili con controlli di sicurezza delle app ChatGPT, senza causa specifica accertata. Stato: VALIDATO per fresh_09; freeze BLOCCATO.

### V5-GEM-03 — Revisore residuo

Attivita: preparazione revisione indipendente fresh_02-fresh_10. Script: `review_rag_v5_gemini_remaining_v1.py`, commit `954cfd4`, derivato dal revisore esistente con blocco esplicito fresh_01 e hash del manifest aggiornato. Report: pubblicazione GitHub riuscita; nessuna chiamata API e nessun dry-run ancora eseguito. Risultato: IMPLEMENTATO. Decisione: verificare hash manifest VPS e dry-run offline prima di qualsiasi richiesta Gemini; conservare fresh_01 invariato. Stato: IMPLEMENTATO; freeze globale BLOCCATO.

### V5-GEM-03 — Preflight verificato

Attivita: controllo offline fresh_02. Script: reviewer `954cfd4`. Report: manifest SHA256 c160a8a2128e05eda50842230c5f4aad2bf9a8085f4240c8ee893ed2e3a3fa71; dry-run PASS, bundle SHA256 7e64a3c213b9cd4a35c1e3b6fcec1670ac198eed621c2afaae661b380ab5c425, blind true. Risultato: VALIDATO preflight, zero API. Decisione: autorizzare singola revisione fresh_02 e verificare report prima di proseguire. Stato: VALIDATO; freeze BLOCCATO.

### V5-GEM-03 — Budget locale esaurito

Attivita: diagnosi blocco fresh_02. Script: reviewer `954cfd4`; ledger locale. Report: 2026-10-23 UTC conteggio 2, presenti soltanto report fresh_01 v1 e v2; fresh_02 fermato prima della richiesta API da LOCAL_DAILY_BUDGET_EXHAUSTED con limite 1. Risultato: ESEGUITO controllo ledger; origine e consegna dei due tentativi non ancora accertate. Decisione: ispezionare metadata dei report senza ripetere richieste, non azzerare ledger. Stato: BLOCCATO per fresh_02; freeze globale BLOCCATO.

### V5-GEM-03 — Riconciliazione richieste Gemini

Attivita: ispezione report fresh_01 v1 e v2 sulla VPS. Script: lettura metadati JSON senza API. Report: entrambi BLOCCATO per UNVERIFIABLE_QUOTE; v2 contiene usage_metadata con 4894 token, prova di risposta Gemini ricevuta; v1 senza usage_metadata nel riepilogo. Ledger 2026-10-23 UTC: 2 tentativi contabilizzati. Risultato: ESEGUITO riconciliazione parziale; nessuna richiesta fresh_02 inviata. Decisione: non ripetere fresh_01, non alterare ledger, attendere nuova giornata UTC per fresh_02. Stato: BLOCCATO per budget giornaliero; freeze globale BLOCCATO.

### V5-GEM-04 — fresh_02 HTTP 503

Attivita: prima richiesta indipendente fresh_02 con limite locale 5. Script: `review_rag_v5_gemini_remaining_v1.py` (`954cfd4`). Commit: script esistente. Report: `gemini_fresh_02_review_v1.json` ricevuto, manifest SHA256 c160a8a2128e05eda50842230c5f4aad2bf9a8085f4240c8ee893ed2e3a3fa71, bundle SHA256 7e64a3c213b9cd4a35c1e3b6fcec1670ac198eed621c2afaae661b380ab5c425; status BLOCCATO, HTTPError 503 Service Unavailable; ledger 2026-10-23 UTC=3. Risultato: ESEGUITO tentativo, nessuna revisione ricevuta. Decisione: conservare report v1 e ledger, non ripetere immediatamente; eventuale nuova richiesta solo come retry differenziale motivato da indisponibilita API, con report v2 e controllo quota. Stato: BLOCCATO; freeze globale BLOCCATO.

### V5-GEM-05 — Requisiti resilienza revisore

Attivita: definizione REQ-GEM-01 e REQ-GEM-02 su richiesta utente dopo HTTP 503. Script: revisore attuale `954cfd4`, adeguamento DA FARE. Commit: protocollo `222fdac`. Report: nessuna nuova chiamata API, evidenza HTTP 503 gia archiviata in V5-GEM-04. Risultato: requisiti documentati. Decisione: implementare revisore non bloccante con controllo preliminare leggero, log esplicito di skip e contabilizzazione delle eventuali richieste di prova; non equiparare skip ad approvazione indipendente. Stato: DA FARE per implementazione; freeze globale BLOCCATO.

### V5-GEM-06 — Evidenza AI Studio e quota

Attivita: esame schermate Google AI Studio e documentazione pubblica API. Script: nessuna chiamata API. Commit: requisiti REQ-GEM-01/02 gia documentati. Report: screenshot utente Free Tier Gemini 3 Flash RPM 1/5, TPM 1.55K/250K, RPD 3/20, un errore 503; ledger locale UTC=3. Risultato: VALIDATO confronto tra screenshot e report 503, non prova di disponibilita attuale. Decisione: Gemini controllo formale opzionale; preflight legge ledger, non assume endpoint ufficiale per quota residua, non consuma chiamata generateContent di prova; riallineare reset quota a Pacific time e limiti configurabili, senza approvazione implicita del gate. Stato: DA FARE implementazione; freeze BLOCCATO.

### V5-GEM-07 — Preflight quota locale

Attivita: pubblicazione controllo quota Gemini read-only. Script: `scripts/gemini_optional_preflight_v1.py`. Commit: `1456abf`. Report: non ancora eseguito su VPS; nessuna API chiamata. Risultato: IMPLEMENTATO script con giorno Pacific e conteggio locale conservativo; quota Google live non verificata. Decisione: pull VPS ed esecuzione offline, poi integrare skip non bloccante nel revisore. Stato: IMPLEMENTATO; freeze globale BLOCCATO.

### V5-GEM-08 — Preflight VPS e REQ-GEM-01

Attivita: verifica preflight locale e implementazione revisore opzionale. Script: `gemini_optional_preflight_v1.py` (`1456abf`), `review_rag_v5_gemini_remaining_v1.py` (`57c5692`, `30fdeeef`). Report: VPS giorno Pacific 2026-10-23, used=3, limit=20, remaining=17, google_remaining=null, api_requests=0. Risultato: VALIDATO preflight locale; IMPLEMENTATO `--optional` per HTTPError/URLError, chiave assente e budget esaurito, senza PASS implicito. Decisione: eseguire test offline differenziale dello skip prima di validare REQ-GEM-01; nessuna API aggiuntiva. Stato: IMPLEMENTATO per REQ-GEM-01; freeze BLOCCATO.

### V5-GEM-09 — Skip opzionale validato

Attivita: verifica VPS senza API di REQ-GEM-01 su fresh_03. Script: reviewer commit `30fdeeef` con --optional e limite locale 1. Report: `gemini_fresh_03_optional_offline_v1.json`, manifest c160a8a2128e05eda50842230c5f4aad2bf9a8085f4240c8ee893ed2e3a3fa71, bundle a4b70b2b4e8b8e6f5cb78efdd01f2cdd1035e683eec256da904ae7940f90a4ad, skipped=true, reason=LOCAL_DAILY_BUDGET_EXHAUSTED, exit=0. Risultato: VALIDATO skip per budget senza nuova chiamata API; non prova runtime HTTP 503. Decisione: non ripetere questo test; integrare quota Pacific nel revisore e conservare gate indipendente. Stato: VALIDATO limitatamente allo skip per budget; freeze BLOCCATO.

### V5-GEM-10 — Pacific counter

Attivita: allineamento revisore alla giornata Pacific. Script: review_rag_v5_gemini_remaining_v1.py. Commit: ad08e57. Report: preflight VPS 2026-10-23, 3/20 richieste locali, 17 residue, zero API. Risultato: IMPLEMENTATO; controllo lettura ESEGUITO, rollover DA FARE. Decisione: test offline differenziale del cambio giornata. Stato: IMPLEMENTATO.

### V5-GEM-11 — Differential rollover offline

Attivita: preparazione verifica distinta dal test skip gia VALIDATO. Script: test_gemini_pacific_rollover_offline_v1.py. Commit: dfc4f37. Report: DA FARE esecuzione VPS, zero API previste. Risultato: IMPLEMENTATO test su codice reviewer, migrazione UTC, rollover estivo e invernale. Decisione: eseguire una sola volta e registrare esito. Stato: IMPLEMENTATO.

### V5-GEM-12 — Rollover Pacific VPS

Attivita: test differenziale offline del contatore Pacific. Script: test_gemini_pacific_rollover_offline_v1.py (dfc4f37). Report: VPS status VALIDATO, 5/5 passed (legacy_same_day, before_pt_midnight, after_pt_midnight, winter_before_midnight, winter_after_midnight), api_requests=0, real_ledger_modified=false. Risultato: VALIDATO rollover e compatibilita UTC nei casi simulati. Decisione: non ripetere test equivalente; HTTP 503 runtime resta da verificare separatamente; freeze RAG V5 BLOCCATO. Stato: VALIDATO.

### V5-CERT-HASH-01 — Manifest candidate v2

Attivita: verifica SHA-256 manifest gold candidato su GitHub e VPS. Script: sha256sum (VPS), lettura GitHub. Commit: 553f050 (correzione protocollo). Report: output VPS SHA-256 c160a8a2128e05eda50842230c5f4aad2bf9a8085f4240c8ee893ed2e3a3fa71, coincidente con GitHub e reviewer. Risultato: VALIDATO hash del candidato, nessuna modifica al manifest. Decisione: non ripetere controllo equivalente; revisione indipendente e fingerprint runtime ancora DA FARE, freeze BLOCCATO. Stato: VALIDATO.

### V5-CERT-REVIEW-PREFLIGHT-01

Attivita: verifica preliminare delle rubriche sulle fonti Drive. Script: nessuno. Report: confronto 10 casi con quattro documenti. Risultato: ESEGUITO, due precisazioni su fresh_01 e fresh_10. Decisione: revisione indipendente ancora DA FARE; freeze BLOCCATO. Stato: ESEGUITO.

### V5-REVIEW-INTERNAL-02

Attivita: approvazione della verifica interna delle dieci rubriche. Script: confronto diretto con fonti Drive, gia eseguito. Commit: 2090c10 (correzione hash wrapper). Report: V5-CERT-REVIEW-PREFLIGHT-01. Risultato: VALIDATO limitatamente alla coerenza documentale interna. Decisione: nessuna approvazione indipendente implicita; freeze BLOCCATO. Stato: VALIDATO.

### V5-RUNTIME-FP-01

Attivita: ricognizione configurazione runner VPS. Script: grep e sha256sum in sola lettura. Commit: 2090c10. Report: manifest SHA c160a8a2; modello qwen3.5:9b, embedding qwen3-embedding:0.6b, reranker mmarco-mMiniLMv2-L12-H384-v1, collection dribbling_tactics_v5_multisource, Chroma /opt/football-data-lab/knowledge/rag/chroma, priority-exact default off. Risultato: ESEGUITO fingerprint statico parziale; prompt e commit VPS da confermare, modelli e collection live da verificare. Decisione: acquisire fingerprint read-only senza generazione. Stato: ESEGUITO.

### V5-RUNTIME-FP-02

Attivita: verifica risorse VPS senza generazione. Script: ollama list, Chroma count, sha256sum. Report: modelli richiesti presenti; collection 5319; SHA smoke 8eaf7f77a648b605355cab3f7b2c0b93a23d835a2a0a068466cbf95ae582ac6c; SHA wrapper 4d9f0cb3e98d036949c746fec07e42d205d311abd9f2798cf2158e0b0b230fc3. Risultato: VALIDATO risorse e hash file, non il commit VPS. Decisione: evitare verifiche duplicate; freeze BLOCCATO. Stato: VALIDATO.

### V5-E2E-RECONCILE-01

Attivita: confronto offline di dieci risposte E2E esistenti con rubriche gold. Script: nessuno. Report: rag_v5_candidate_v2_runtime_report.json. Risultato: 4/10 con criterio mandatory completo; casi conformi fresh_02, fresh_05, fresh_06, fresh_08. Decisione: obiettivo 9/10 non dimostrato; non ripetere benchmark, intervenire sui difetti documentati. Stato: ESEGUITO.

### V5-E2E-DIAG-02

Attivita: diagnosi differenziale delle evidenze del report E2E gia prodotto. Script: nessuno; analisi offline di risposte e top8. Commit: 374c2cd. Report: docs/rag-v5-e2e-failure-analysis-2026-10-23.md. Risultato: ESEGUITO; gap di retrieval documentati per fresh_03, fresh_04, fresh_07 e fresh_10, difetti di completezza in fresh_01 e fresh_09. Decisione: non ripetere test shadow equivalenti; sviluppare delta source-aware nel runner effettivo, valutare su nuovo holdout senza contaminare il gold. Stato: ESEGUITO.

### V5-SOURCE-AWARE-IMPLEMENT-01

Attivita: integrazione source-aware opt-in nel runner V5 e wrapper locked. Script: smoke_test_rag_v5_e2e.py, run_rag_v5_locked_candidate_v2.py. Commit: 9170f83, 03a5e0f. Report: verifica read-back GitHub dei due file, opzione --source-aware presente e condizionata in entrambi. Risultato: IMPLEMENTATO filtro Chroma per autore esplicitamente nominato (Ussia/Foscarini), merge candidati senza scritture all'indice, rerank preesistente e default invariato. Decisione: eseguire test differenziale nuovo su opzione e verificare runtime VPS prima di qualsiasi benchmark; gold candidato non modificato. Stato: IMPLEMENTATO.
