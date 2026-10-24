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

### V5-SOURCE-AWARE-DIFF-02

Attivita: differenziale VPS baseline vs --source-aware su domanda Ussia 4/A. Script: smoke_test_rag_v5_e2e.py. Commit correzione: aa2586e. Report: v5_source_baseline_v1.json e v5_source_aware_v1.json forniti dall'operatore; 5319 record prima/dopo, top8 identico, source_aware_source=null anche con flag attivo. Risultato: ESEGUITO, nessun delta retrieval; individuata regex con boundary doppiamente escaped nel runner. Decisione: corretta regex nel commit aa2586e; ripetere esclusivamente il caso diagnostico differenziale con nuovo codice, non benchmark shadow. Stato: ESEGUITO.

### V5-SOURCE-AWARE-DIFF-03

Attivita: verifica differenziale VPS del retrieval source-aware dopo correzione regex. Script: projects/tactical-engine/scripts/smoke_test_rag_v5_e2e.py con --retrieval-only e --source-aware. Commit implementazione/correzione: 9170f83, aa2586e. Report: v5_source_baseline_v1.json e v5_source_aware_fixed_v1.json; output F3/F8 fornito dall'operatore. Risultato: ESEGUITO; la baseline aveva 0/8 chunk di Transizioni.Ussia, la prova corretta ne recupera 2/8 (F3 pp. 15-16, F8 pp. 35-37), fonte riconosciuta come Transizioni.Ussia, indice Chroma invariato. F3 descrive la continuazione 4/B e la conclusione entro 5 secondi; F8 riguarda esercitazione 19, non 4/A. Decisione: cercare il riferimento esatto 4/A nell'indice; pertinenza specifica ancora DA FARE; nessun benchmark ripetuto, nessuna integrazione o certificazione attestata. Stato: ESEGUITO.

### V5-USSIA-4A-MAP-01

Attivita: mapping Ussia 4/A originale e chunk Chroma. Script: scripts/inspect_ussia_4a_chunk_mapping_v1.py. Commit: 6d2930d. Report: evaluation/ussia_4a_chunk_mapping_v1.json (output VPS fornito). Risultato: ESEGUITO; Docling pagina 14 contiene intestazione e svolgimento; chunk_index 10 ece84a07 contiene svolgimento e pagine [12,13,14], ma headings solo SVOLGIMENTO; chunk 45 contiene riferimento 4/A solo nell'indice; count 5319 invariato. Decisione: esaminare codice di costruzione chunk e progettare correzione circoscritta, senza ripetere test o reindicizzare ora. Stato: ESEGUITO.

### V5-USSIA-4A-CHUNK-CODE-01

Attivita: audit statico codice chunking V5, distinto dal mapping VPS gia eseguito. Script esaminato: scripts/build_rag_index_v5_multisource.py. Commit report: c67866b. Report: docs/v5-ussia-4a-chunking-code-audit-2026-10-23.md. Risultato: ESEGUITO; HybridChunker merge_peers=True, headings da chunk.meta.headings, page_numbers da prov, ID dipendente dal testo; chunk 4/A manca dell'intestazione specifica. Decisione: progettare correzione isolata senza modificare la collection corrente; niente replay di test completati. Stato: ESEGUITO.

### V5-EXERCISE-CHUNK-DESIGN-01

Attivita: progettazione documentale variante gerarchica opt-in per esercitazioni, distinta da mapping e audit gia eseguiti. Script: nessuno; implementazione DA FARE. Commit: 4fb3f8f. Report: docs/v5-exercise-aware-chunking-design.md. Risultato: ESEGUITO; definiti confini esercitazioni, titoli, provenienza, pagine e controllo sommario. Decisione: implementare estrattore separato e controlli deterministici offline; nessuna scrittura su collection V5 o ripetizione di benchmark. Stato: ESEGUITO.

### V5-EXERCISE-EXTRACT-IMPLEMENT-01

Attivita: implementare estrattore Docling gerarchico opt-in e isolato. Script: scripts/extract_exercise_units_v1.py. Commit: b599e3e. Report: read-back GitHub del file; esecuzione VPS DA FARE. Risultato: IMPLEMENTATO; estrazione offline con intestazione, pagine e riferimenti agli elementi, nessuna operazione Chroma o LLM. Decisione: eseguire controllo deterministico nuovo su esercitazioni 3/A, 4/A e 4/B, senza ripetere mapping e benchmark precedenti. Stato: IMPLEMENTATO.

### V5-EXERCISE-EXTRACT-OFFLINE-01

Attivita: analisi output offline estrattore v1. Script: scripts/extract_exercise_units_v1.py (b599e3e). Report: evaluation/ussia_exercise_units_v1.json fornito da VPS. Risultato: ESEGUITO; 33 unita, 4/A pagina 14 con titolo e svolgimento separata da 3/A e 4/B. Anomalie: refuso Esecitazione 10 incorporato nella 9; sezioni psicocinetica e portiere incorporate rispettivamente in 11/B e 21; identificativi 19/B e 20 ricorrenti. Decisione: correggere confini e disambiguazione in v2, senza reindicizzare. Stato: ESEGUITO.

### V5-EXERCISE-EXTRACT-V2-01

Attivita: correggere confini esercitazioni in variante offline isolata. Script: scripts/extract_exercise_units_v2.py. Commit: 23cc0db. Report: codice GitHub; nuovo output VPS DA FARE. Risultato: IMPLEMENTATO; riconoscimento refuso Esecitazione, interruzione su sezioni psicocinetica e portiere, ID hash derivati anche dal riferimento Docling. Decisione: verificare soltanto differenze V1 vs V2, senza ripetere mapping Chroma o benchmark. Stato: IMPLEMENTATO.

### V5-EXERCISE-EXTRACT-V2-OFFLINE-01

Attivita: verifica differenziale V2 rispetto alle anomalie V1, senza replay dei benchmark. Script: scripts/extract_exercise_units_v2.py (commit 23cc0db). Report: ussia_exercise_units_v2.json prodotto su VPS e fornito dall'operatore. Risultato: ESEGUITO; 34 unita contro 33 V1; esercitazione 10 separata dalla 9 (pagina 23), 11/B limitata a pagina 25, 21 limitata a pagina 40; 4/A ancora autonoma a pagina 14. Le etichette 19/B e 20 ricorrono in sezioni diverse con heading_ref e hash distinti. Decisione: correzioni mirate confermate; non dichiarare integrazione, certificazione o miglioramento retrieval. Valutare robustezza dei confini su altre fonti prima di indicizzazione candidata. Stato: ESEGUITO.

### V5-EXERCISE-HEADING-COVERAGE-01

Attivita: inventario statico delle convenzioni delle intestazioni nei JSON Docling, distinto dai controlli Ussia e dai benchmark RAG. Script: scripts/audit_exercise_heading_coverage_v1.py. Commit: a240657. Report previsto: evaluation/exercise_heading_coverage_v1.json, non ancora prodotto. Risultato: IMPLEMENTATO; sola lettura di file locali, nessuna inferenza, embedding o modifica Chroma. Decisione: eseguire una volta l'inventario e selezionare solo successivamente un eventuale controllo differenziale su fonte non gia coperta. Stato: IMPLEMENTATO.

### V5-EXERCISE-HEADING-COVERAGE-OFFLINE-01

Attivita: inventario unico delle intestazioni Docling nel corpus formations-and-systems. Script: scripts/audit_exercise_heading_coverage_v1.py (a240657). Report: evaluation/exercise_heading_coverage_v1.json prodotto sulla VPS e fornito dall'operatore. Risultato: 141 documenti, 3 con intestazioni compatibili V2 (Ussia 34, DeRosa 8, Allegati_2832014181753 5); 38 documenti con 183 intestazioni di altri tipi. Il rilevamento di intestazioni non prova che siano esercitazioni autonome. Decisione: non eseguire extraction benchmark indiscriminati o reindicizzazione; definire criteri di riconoscimento e confini per famiglie documentali prima di test mirati non duplicati. Stato: ESEGUITO.

### V5-EXERCISE-HEADING-FAMILIES-DESIGN-01

Attivita: specifica documentale delle famiglie di intestazioni e dei confini di esercitazione, senza duplicare controlli precedenti. Script: nessuno (progettazione). Commit: 2ee613a. Report: docs/v5-exercise-heading-families-design.md. Risultato: ESEGUITO; distinte intestazioni numerate, alternative, descrittive, collettive e ambigue; section_boundary distinto da exercise_start, con provenance Docling e review_required. Decisione: definire casi mirati basati su evidenza insufficiente prima di nuova implementazione; nessuna variazione Chroma, runner, gold o benchmark. Stato: ESEGUITO.

### V5-EXERCISE-HEADING-ACCEPTANCE-PLAN-01

Attivita: definizione campione e criteri di accettazione per futura analisi differenziale delle intestazioni non coperte da V2. Script: nessuno (piano documentale). Commit: 541ccc3. Report: docs/v5-exercise-heading-acceptance-plan.md. Risultato: ESEGUITO; tre fonti con delta documentato (smarcamento_marcamento, la_punta_centrale_Gritti, Allegati_2832014181753) e otto criteri, senza test o modifiche alla pipeline. Decisione: prima di ogni ispezione nuova verificare che non esistano evidenze equivalenti; solo poi autorizzare una singola raccolta read-only del contesto. Stato: ESEGUITO.

### V5-EXERCISE-HEADING-CONTEXT-IMPLEMENT-01

Attivita: implementare ispezione mirata e read-only delle intestazioni Docling e dei riferimenti per tre fonti selezionate nel piano di accettazione. Script: scripts/inspect_exercise_heading_context_v1.py. Commit: 8dd613f. Report previsto: evaluation/exercise_heading_context_v1.json, non ancora prodotto. Risultato: IMPLEMENTATO; script circoscritto a smarcamento_marcamento, la_punta_centrale_Gritti e Allegati_2832014181753; heading, pagine, self_ref e due intestazioni precedenti/successive, classificazione review_required. Decisione: richiedere singola esecuzione offline su VPS, senza replay dei test Ussia, retrieval, embedding o scrittura Chroma. Stato: IMPLEMENTATO.

### V5-EXERCISE-HEADING-CONTEXT-OFFLINE-01

Attivita: lettura del report sulle intestazioni di tre fonti. Script: scripts/inspect_exercise_heading_context_v1.py. Commit script: 8dd613f. Report: exercise_heading_context_v1.json prodotto sulla VPS e fornito dall'operatore. Risultato: ESEGUITO; 22 candidati, di cui 8 smarcamento_marcamento, 6 la_punta_centrale_Gritti, 8 Allegati_2832014181753. Riferimenti Docling e pagine presenti. Tutte le voci rimangono review_required. Decisione: confini non validati; evitare reindicizzazione e replay di test precedenti. Stato: ESEGUITO.

### V5-EXERCISE-BOUNDARY-EVIDENCE-DECISION-01

Attivita: riconciliazione dei risultati disponibili sui confini. Script: nessuna nuova esecuzione. Commit: e114e95. Report: docs/v5-exercise-boundary-evidence-decision.md. Risultato: 22 intestazioni note, nessuna prova sufficiente sui confini; Stato: ESEGUITO. Decisione: limitare il successivo controllo ai contenuti associati, senza ripetere i test precedenti o modificare Chroma.

### V5-EXERCISE-BODY-INSPECTION-PLAN-01

Attivita: progettazione di controllo differenziale del contenuto Docling. Script: non implementato. Commit: beb05ba. Report: docs/v5-exercise-body-inspection-plan.md. Risultato: piano limitato a 22 riferimenti, tre fonti e brevi estratti con provenance. Decisione: solo successiva implementazione read-only, nessun test duplicato o Chroma. Stato: ESEGUITO.

### V5-EXERCISE-BODY-INSPECTION-IMPLEMENT-01

Attivita: implementare ispettore di contenuti Docling. Script: scripts/inspect_exercise_body_context_v1.py. Commit: a07ebf2. Report: da produrre. Risultato: IMPLEMENTATO per 22 riferimenti su tre fonti. Decisione: una sola esecuzione offline, senza reindicizzazione. Stato: IMPLEMENTATO.

### V5-EXERCISE-BODY-INSPECTION-OFFLINE-01

Attivita: analisi report di ispezione del corpo Docling. Script: scripts/inspect_exercise_body_context_v1.py. Commit script: a07ebf2. Report: exercise_body_context_v1.json fornito dall'operatore. Risultato: 22 su 22, 8 smarcamento, 6 Gritti, 8 Allegati; esercitazione 16 in Allegati con zero elementi intermedi. Decisione: conservare review_required e verificare anomalie prima di validare confini; nessuna modifica Chroma. Stato: ESEGUITO.

### V5-EXERCISE-BOUNDARY-ANOMALY-REVIEW-01

Attivita: revisione evidenze. Script: nessuno. Commit: f1118e8. Report: docs/v5-exercise-boundary-anomaly-review.md. Risultato: anomalie di duplicazione, figure e contenuto assente. Decisione: confini non validati; revisione ulteriore solo sui casi incerti. Stato: ESEGUITO.

### V5-EXERCISE-BOUNDARY-GAP-PLAN-01

Attivita: analisi delle evidenze mancanti sui confini. Script: nessuna esecuzione. Commit: c2d83bd. Report: docs/v5-exercise-boundary-gap-plan.md. Risultato: quattro finestre Docling mirate con delta rispetto ai report precedenti. Decisione: solo successiva ispezione read-only, senza replay o modifica Chroma. Stato: ESEGUITO.

### V5-EXERCISE-BOUNDARY-WINDOWS-IMPLEMENT-01

Attivita: implementazione ispezione di quattro finestre Docling. Script: scripts/inspect_exercise_boundary_windows_v1.py. Commit: bb02c68. Report previsto: evaluation/exercise_boundary_windows_v1.json. Risultato: IMPLEMENTATO; estratti e provenance, nessuna esecuzione. Decisione: una sola esecuzione offline, senza modifiche agli indici. Stato: IMPLEMENTATO.

### V5-EXERCISE-BOUNDARY-WINDOWS-OFFLINE-01

Attivita: analisi delle quattro finestre Docling. Script: inspect_exercise_boundary_windows_v1.py (bb02c68). Commit report: 398860d. Report: docs/v5-exercise-boundary-windows-findings.md e JSON operatore. Risultato: individuati titoli in text/caption e confine erroneo su esercitazione 16. Decisione: progettare segmentazione sensibile ai titoli, senza modificare V2 o Chroma. Stato: ESEGUITO.

### V5-EXERCISE-SEMANTIC-BOUNDARY-DESIGN-01

Attivita: progettazione di regole candidate per confini semantici. Script: nessuno. Commit: b74c496. Report: docs/v5-exercise-semantic-boundary-design.md. Risultato: regole per text, caption, sottotitoli, titoli ripetuti e sezioni collettive. Decisione: eventuale prototipo offline read-only con revisione, nessuna modifica V2 o Chroma. Stato: ESEGUITO.

### V5-EXERCISE-SEMANTIC-BOUNDARY-PROTOTYPE-01

Attivita: prototipo offline per proposte di confini. Script: scripts/propose_semantic_exercise_boundaries_v1.py. Commit: 528d90b. Report: exercise_semantic_boundary_proposals_v1.json fornito dall'operatore. Risultato: 16 candidati da quattro finestre, tutti review_required. Decisione: analizzare gli esiti prima di validare confini; nessuna modifica Chroma o V2. Stato: ESEGUITO.

### V5-EXERCISE-SEMANTIC-CANDIDATE-REVIEW-01

Attivita: revisione dei 16 candidati semantici. Script: propose_semantic_exercise_boundaries_v1.py (528d90b), nessun replay. Commit report: b5eae2b. Report: docs/v5-exercise-semantic-candidate-review.md. Risultato: 8 inizi proposti, 4 sezioni, 1 sottotitolo e 3 duplicazioni ambigue. Decisione: mantenere review_required, non modificare V2 o Chroma. Stato: ESEGUITO.

### V5-SMARCAMENTO-RESIDUAL-BOUNDARY-DECISION-01

Attivita: valutazione residua di Smarcamento. Script: nessuna nuova esecuzione. Commit report: 7b7525d. Report: docs/v5-smarcamento-residual-boundary-decision.md. Risultato: 109 inizio candidato, 115 possibile ripresa, 122 indeterminato. Decisione: tutti review_required; nessuna deduplicazione e nessuna modifica V2 o Chroma. Stato: ESEGUITO.

### V5-SMARCAMENTO-ORIGINAL-LAYOUT-REVIEW-01

Attivita: esame pagina 6 PDF originale, pagina stampata 10. Script: nessuno. Commit report: c7a65b8. Report: docs/v5-smarcamento-original-layout-review.md. Risultato: i riferimenti 109, 115, 122 rappresentano un'unica esercitazione con due esempi illustrativi; il testo specifica sempre stesso esercizio. Decisione: identita VALIDATO sul documento originale, nessuna integrazione V2 o Chroma. Stato: VALIDATO.

### V5-EXERCISE-CANDIDATE-BUILDER-01

Attivita: preparazione di collection candidata isolata per esercitazioni Ussia. Script: scripts/build_rag_v5_exercise_candidate_v1.py. Commit: d8e7741. Report: nessun report runtime; solo implementazione GitHub. Risultato: builder opt-in con dry-run predefinito, estrattore V2, metadati di provenienza e collection separata. Decisione: prima verificare percorso JSON Ussia e comportamento offline; scrittura candidata solo dopo autorizzazione operativa e verifica rollback. Baseline V5 e runner invariati. Stato: IMPLEMENTATO.

### V5-EXERCISE-CANDIDATE-DRYRUN-01

Attivita: dry-run VPS del builder candidato isolato Ussia. Script: scripts/build_rag_v5_exercise_candidate_v1.py (commit d8e7741). Report: output shell operatore 2026-10-23, PLAN candidate=dribbling_tactics_v5_exercise_candidate_v1 source=Transizioni.Ussia.json units=34; DRY_RUN no Chroma access, no embeddings, no writes. Risultato: ESEGUITO con 34 unita, coerenti con precedente estrazione V2; non e una verifica della qualita semantica o del retrieval. Decisione: autorizzare solo creazione opt-in della collection candidata separata, con baseline intatta e successiva verifica conteggi; nessuna promozione automatica. Stato: ESEGUITO.

### V5-EXERCISE-CANDIDATE-CREATE-01

Attivita: creazione collection isolata sulla VPS dopo dry-run. Script: build_rag_v5_exercise_candidate_v1.py (d8e7741). Report: conferma dell'operatore dell'esecuzione della shell; output completo non allegato, valori rows e baseline non verificati indipendentemente. Risultato: ESEGUITO secondo conferma operatore; verifica dei conteggi runtime ancora DA FARE. Decisione: mantenere candidata isolata, non promuovere senza riscontro 34/5319. Stato: ESEGUITO.

### V5-EXERCISE-CANDIDATE-RETRIEVAL-IMPLEMENT-01

Attivita: predisporre retrieval opt-in candidato nel runner effettivo e wrapper. Script: smoke_test_rag_v5_e2e.py (0a7223d), run_rag_v5_locked_candidate_v2.py (bdd093b). Report: commit GitHub dei due script; nessun report VPS. Risultato: IMPLEMENTATO flag --exercise-candidate, merge di candidati Ussia prima del rerank, verifica 34 record, baseline 5319, controllo conteggi finali; default invariato. Decisione: verifica runtime mirata su flag nuovo prima di qualsiasi benchmark E2E, nessuna promozione. Stato: IMPLEMENTATO.

### V5-EXERCISE-CANDIDATE-PARTIAL-RECOVERY-01

Attivita: diagnosi errore primo retrieval opt-in e implementazione recupero parziale. Script: smoke_test_rag_v5_e2e.py (0a7223d), build_rag_v5_exercise_candidate_v1.py (0d98281). Commit: 0d98281. Report: traceback VPS fornito dall'operatore, Unexpected exercise candidate count 12; expected 34. Risultato: ESEGUITO controllo runtime, candidato parziale 12/34, retrieval interrotto prima della query; IMPLEMENTATO --resume-candidate con verifica preventiva di ID, documenti e metadata e completamento dei soli record mancanti, senza sovrascrittura. Decisione: riprendere soltanto la collection candidata e verificare 34/34, baseline 5319; nessun benchmark ripetuto. Stato: IMPLEMENTATO.

### V5-EXERCISE-CANDIDATE-RESUME-01

Attività: completamento collection candidata Ussia parziale. Script: `scripts/build_rag_v5_exercise_candidate_v1.py --resume-candidate` (commit `0d98281`). Commit: `0d98281` (script); report: output shell VPS fornito dall'operatore il 2026-10-23, `RESUME verified_existing=12 missing=22` e `CANDIDATE_COMPLETE rows=34 baseline_unchanged=5319`. Risultato: 22 record mancanti aggiunti; collection candidata 34 record, baseline 5319 invariata. Decisione: autorizzare un singolo probe retrieval-only del nuovo percorso opt-in; nessuna promozione, generazione o benchmark gold. Stato: ESEGUITO.

### V5-EXERCISE-CANDIDATE-PROBE-01

Attività: probe retrieval-only del candidato Ussia nel runner V5. Script: `smoke_test_rag_v5_e2e.py` (commit `0a7223d`); correzione successiva `cf61e33`. Report: `projects/tactical-engine/evaluation/v5_exercise_candidate_probe_v1.json` allegato dall'operatore; output `COMPLETE 1/1; V5 unchanged=True`. Risultato: ESEGUITO; baseline 5319 e candidata 34 invariati; `exercise_candidate_ids=[]`, F8 solo indice Ussia pagina 48, non contenuto 4/A; retrieval NON VALIDATO. Diagnosi codice: regex `r"\\\\bussia\\\\b"` erroneamente cerca backslash letterali invece del confine di parola. Decisione: correggere regex nel runner (`cf61e33`), eseguire soltanto verifica differenziale mirata, non benchmark gold e non promuovere. Stato: ESEGUITO.

### V5-EXERCISE-CANDIDATE-PROBE-FIXED-01

Attività: verifica differenziale del fix regex Ussia nel runner effettivo. Script: `smoke_test_rag_v5_e2e.py --exercise-candidate --retrieval-only --probe-question 'Descrivi l'esercitazione 4/A di Ussia.'` (fix commit `cf61e33`). Commit: `cf61e33`. Report: `v5_exercise_candidate_probe_fixed_v1.json` allegato in chat dall'operatore; output VPS `COMPLETE 1/1; V5 unchanged=True`. Risultato: F1 `Transizioni.Ussia`, pagina 14, contiene esercitazione 4/A con 8 contro 8, 2 portieri, 6 passaggi e 5 secondi per finalizzare; 24 ID candidati aggiunti al pool, collection 34 e baseline 5319 invariate. Decisione: VALIDATO esclusivamente retrieval mirato 4/A; nessuna valutazione della generazione, nessuna integrazione di default o certificazione 9/10. Stato: VALIDATO.

### V5-LOCKED-INTEGRATION-GATE-01

Attività: riconciliazione del percorso V5 con le evidenze già validate. Script: `run_rag_v5_locked_candidate_v2.py` (flag `--source-aware`, `--priority-exact`, `--exercise-candidate`), `smoke_test_rag_v5_e2e.py`; commit già presenti `bdd093b`, `cf61e33`. Report: audit codice e stato GitHub 2026-10-23, nessuna nuova esecuzione VPS. Risultato: wrapper supporta già la composizione opt-in delle tre modalità; recupero Ussia 4/A VALIDATO nel probe differenziale, non nelle dieci risposte locked; gold indipendente non ancora approvato. Decisione: non duplicare script o benchmark; autorizzare soltanto un'esecuzione diagnostica E2E della configurazione combinata dopo preflight e conservare report distinto, senza usare `--approved-gold` o dichiarare 9/10. Stato: DA FARE.

### V5-GOV-EXTERNAL-REVIEW-RETIRE-01

Attività: decisione vincolante del titolare del 2026-10-23 di eliminare revisore esterno indipendente e blind adjudication esterna come prerequisiti obbligatori. Script: `scripts/run_rag_v5_locked_candidate_v2.py` (commit `c56e7f2`, rimosso gate `--approved-gold`, nessun cambio a manifest/indice). Commit: `c56e7f2`, TODO `bcc8a76`. Report: istruzione esplicita del titolare e audit GitHub dei requisiti. Risultato: requisito organizzativo ritirato; nessuna revisione esterna effettuata o simulata, nessun nuovo benchmark. Decisione: adottare valutazione interna documentata claim-per-claim su rubriche e fonti, conservare manifest SHA e traccia runtime, misurare 9/10 senza certificazione esterna fittizia. Le precedenti note che indicano revisore esterno come BLOCCATO/DA FARE sono storiche e superate per tale sola condizione; restano gli altri gate tecnici non completati. Stato: ESEGUITO.


### V5-LOCKED-INTEGRATION-GATE-01 — esecuzione 2026-10-23

Attività: verifica dell'esecuzione E2E combinata. Script: `scripts/run_rag_v5_locked_candidate_v2.py` e `scripts/smoke_test_rag_v5_e2e.py`. Commit: implementazione `bdd093b`, correzione `cf61e33`, governance `c56e7f2`; nessuna nuova modifica agli script. Report: `rag_v5_combined_candidate_v1.json`, allegato dall'operatore, dieci risposte `fresh_01`-`fresh_10`. Risultato: tutte le dieci risposte generate; source-aware, priority-exact ed exercise-candidate attivi; citazioni presenti, nessun ID citazione invalido; baseline 5319 prima/dopo, candidato 34 prima/dopo, `index_unchanged=true`. La verifica delle citazioni è soltanto sintattica: correttezza delle risposte e punteggio 9/10 ancora non accertati mediante rubriche interne. Decisione: non ripetere l'esecuzione; svolgere valutazione interna documentata domanda per domanda; non promuovere la configurazione di default e non dichiarare certificazione. Stato: ESEGUITO.


### V5-LOCKED-CANDIDATE-INTERNAL-ASSESSMENT-01

Attività: valutazione interna claim-per-claim delle dieci risposte del report combinato locked, senza nuovo test. Script: runner già eseguito `scripts/run_rag_v5_locked_candidate_v2.py` e `scripts/smoke_test_rag_v5_e2e.py`; nessuna nuova implementazione. Commit: report di audit `506c4ba`. Report: `docs/v5-locked-candidate-internal-assessment-01.md` (rubriche mandatory/forbidden del manifest, evidenze F1-F8 e risposte del file `rag_v5_combined_candidate_v1.json`). Risultato: PASS fresh_02, fresh_04, fresh_05, fresh_06, fresh_08; FAIL fresh_01 (limite statistico omesso), fresh_03 (moduli e causalità omessi), fresh_07 (contaminazione della zona B Foscarini/Indiani), fresh_09 (trade-off e controllo imperfetto omessi), fresh_10 (claim specifico Ussia non coperto). Totale 5/10, soglia 9/10 NON raggiunta. Decisione: non ripetere il test, non promuovere configurazione di default; approfondire in modo documentato coerenza fonte/tassonomia, completezza dei mandatory claim e pertinenza delle evidenze prima di progettare un eventuale test tecnicamente differente. Stato: ESEGUITO (audit concluso; benchmark non VALIDATO, non INTEGRATO, non CERTIFICATO).


### V5-TACTICAL-CORPUS-RECONCILIATION-01

Attività: inventario PDF tattica Drive/VPS/Chroma. Script: comandi di sola lettura già eseguiti e ricerca Drive. Commit: `6f08d5a`. Report: `docs/v5-tactical-corpus-reconciliation-2026-10-24.md`. Risultato: 141 PDF VPS, 141 fonti Chroma, 5319 chunk, 11 PDF calcistici non trasferiti; discrepanza Drive 153/154 ancora da chiarire. Decisione: mantenere la baseline invariata e valutare i candidati prima di una collection isolata. Stato: ESEGUITO.


### V5-CORPUS-SCOPE-DECISION-01

Attività: rettifica perimetro su decisione del titolare. Script: nessuno; modifica documentale. Commit: aggiornamento TODO `329613b`. Report: riconciliazione già archiviata, senza nuovi test. Risultato: corpus operativo limitato ai 141 PDF VPS e ai 5319 chunk Chroma; fonti aggiuntive Drive escluse dall'analisi corrente. Decisione: non analizzare né acquisire PDF Drive; procedere con diagnosi dei cinque FAIL sul corpus invariato. Stato: ESEGUITO.


### V5-LOCKED-CANDIDATE-FAILURE-ANALYSIS-01

Attività: diagnosi read-only dei cinque FAIL `fresh_01/03/07/09/10`. Script: ispezione di `scripts/smoke_test_rag_v5_e2e.py`, nessuna esecuzione nuova. Commit: report `60bc141`, TODO `32cdb95`. Report: `docs/v5-locked-candidate-failure-analysis-01.md`. Risultato: copertura retrieval insufficiente per fresh_03/fresh_10, contaminazione fonti per fresh_07, completezza e astensione per fresh_01/fresh_09. Decisione: diagnostica mirata pre/post rerank prima di qualunque patch; baseline 141 PDF e 5319 chunk invariata, nessun documento Drive aggiuntivo nel perimetro corrente. Stato: ESEGUITO.


### V5-RERANK-TRACE-01

Attività: isolare assenza nel pool o perdita nel rerank di estratti per fresh_03 e fresh_10. Script: `scripts/diagnose_v5_rerank_failures_v1.py`. Commit: `e7f9e4b`, correzione normalizzazione `c4ee2b5`. Report: `docs/v5-rerank-trace-01.md` (commit `adf47ee`), dati VPS `diagnostica_v5_rerank_failures_v1.json`. Risultato: collection 5319/34 invariata; fresh_03 manuale Transizioni assente dai 24 candidati dense; fresh_10 Ussia pagina 17 presente nel pool filtrato ma al rango 9, fuori dalla top8. Decisione: preservare corpus e Chroma, progettare correzioni motivate di recupero e selezione senza ripetere il benchmark equivalente. TODO aggiornato `26154a0`. Stato: ESEGUITO.


### V5-SOURCE-COVERAGE-SHADOW-01

Attività: prototipo opt-in della selezione di evidenze per fresh_03/fresh_10 senza modificare il runner V5. Script: `scripts/v5_source_coverage_shadow_v1.py`. Commit: `c400bf0`; TODO `8af0a1b`. Report: non disponibile, esecuzione VPS DA FARE. Risultato: codice IMPLEMENTATO, nessun benchmark o retrieval ripetuto; sul trace esistente fresh_03 richiede recupero aggiuntivo della fonte prima della selezione, fresh_10 contiene Ussia pagina 17 in posizione 9. Decisione: valutare lo shadow offline sui dati di trace senza modificare Chroma; solo dopo progettare un recupero mirato distinto e giustificato. Stato: IMPLEMENTATO.


### V5-TARGETED-COVERAGE-IMPLEMENTATION-01

Attività: introdurre differenza tecnica opt-in per fresh_03 e fresh_10 senza duplicare i test storici. Script: `scripts/v5_targeted_coverage_v1.py` e flag `--targeted-coverage` in `scripts/smoke_test_rag_v5_e2e.py`, inoltrato da `scripts/run_rag_v5_locked_candidate_v2.py`. Commit: helper `e75d3ca`, runner `71994e9`, wrapper `d70856f`, diagnostica scoped `b4d1ebf`, report implementazione `413bf4d`, TODO `6c2ec8e`. Report: `docs/v5-targeted-coverage-implementation-01.md`; runtime DA FARE. Risultato: modifica GitHub implementata; nessuna esecuzione VPS, nessuna evidenza di miglioramento delle risposte. Decisione: sola verifica retrieval-only con variante opt-in, fonte manuale fresh_03 e pagina 17 Ussia fresh_10, baseline 5319/34 invariata; mantenere default e corpus invariati. Stato: IMPLEMENTATO.


### V5-RUNTIME-IMPORT-FAILURE-01

Attività: diagnosi `ModuleNotFoundError: chromadb` dopo `V5_RUNTIME /usr/bin/python3` nella prova scoped fresh_03/fresh_10. Script: `scripts/run_rag_v5_locked_candidate_v2.py`. Commit: fix `779f4c3`, report `1a70278`. Report: `docs/v5-runtime-import-failure-01.md` e log console VPS. Risultato: esecuzione interrotta prima del retrieval, nessun JSON di prova prodotto; precedente check con `find_spec` sostituito da import reali delle tre dipendenze. Decisione: riusare venv esistenti, nessuna installazione o modifica Chroma, riprovare solo la prova precedentemente bloccata. Stato: IMPLEMENTATO.


### V5-RUNTIME-SYMLINK-FIX-01

Attività: riconciliazione log VPS con symlink del venv e import chromadb riuscito. Script: `scripts/run_rag_v5_locked_candidate_v2.py`. Commit: `6faa907`; report `docs/v5-runtime-symlink-fix-01.md` (`d37c1c8`). Report: output operatore con symlink `.venv/bin/python3 -> /usr/bin/python3` e import chromadb da site-packages virtualenv. Risultato: causa individuata nel confronto `Path.resolve()` che elimina la distinzione tra interprete venv e sistema; sostituito con `Path.absolute()`. Decisione: nessuna installazione; ritentare soltanto il retrieval scoped mai partito. Stato: IMPLEMENTATO.


### V5-TARGETED-COVERAGE-RETRIEVAL-01

Attività: verifica VPS della differenza tecnica opt-in fresh_03/fresh_10 con manifest locked SHA256 c160a8a2128e05eda50842230c5f4aad2bf9a8085f4240c8ee893ed2e3a3fa71. Script: `scripts/run_rag_v5_locked_candidate_v2.py`, `scripts/smoke_test_rag_v5_e2e.py`, `scripts/v5_targeted_coverage_v1.py`. Commit: codice `e75d3ca`, `71994e9`, `b4d1ebf`, runtime `6faa907`; report `62e71fc`; TODO `75f33c2`. Report: `docs/v5-targeted-coverage-retrieval-01.md`, output VPS `evaluation/v5_targeted_coverage_retrieval_v1.json` fornito dall'operatore. Risultato: COMPLETE 2/2, index_unchanged true, 5319/34; fresh_03 manuale F8 p5 (pertinenza insufficiente da verificare), fresh_10 manuale F5 p3 e Ussia F8 p17; nessuna generazione e nessuna citazione attesa. Decisione: retrieval diagnostico ESEGUITO, nessuna validazione del benchmark, nessuna integrazione o certificazione; intervenire sulla pertinenza fresh_03 prima di generare. Stato: ESEGUITO.


### V5-TARGETED-ANSWER-CORRECTNESS-01

Attività: valutare correttezza fresh_03/fresh_10. Script: v5_targeted_coverage_v1.py. Commit: e0018bf. Report: docs/v5-targeted-answer-correctness-01.md (2a5707e). Risultato: modifica implementata; generazione VPS non ancora eseguita. Decisione: controllo scoped claim-level, senza modificare Chroma o benchmark. Stato: IMPLEMENTATO.


### V5-TARGETED-ANSWER-SYNTAX-FIX-01

Attività: correggere SyntaxError import helper prima della generazione scoped. Script: `scripts/v5_targeted_coverage_v1.py`. Commit: `0c89b47`. Report: `docs/v5-targeted-answer-syntax-fix-01.md` (`c0f6c63`), log VPS operatore. Risultato: ramo if/else corretto, parsing locale del ramo SYNTAX_OK, generazione VPS non eseguita. Decisione: riprendere la generazione interrotta dopo git pull, nessuna nuova baseline. Stato: IMPLEMENTATO.


### V5-TARGETED-ANSWERS-REVIEW-01

Attività: verifica claim-level delle risposte fresh_03/fresh_10 dopo generazione scoped. Script: wrapper locked, smoke V5 e helper targeted coverage. Commit: fix `0c89b47`, report `dbdb7ca`. Report: `docs/v5-targeted-answers-review-01.md`, JSON VPS `evaluation/v5_targeted_answers_v1.json` fornito dall'operatore. Risultato: fresh_03 incompleta e non validata; fresh_10 soddisfa mandatory claims ma revisione finale sospesa per digressione fuorigioco e possibile confusione pressing/riaggressione. Tempi 132.23s e 138.54s; Chroma 5319/34 invariati. Decisione: non ripetere test equivalenti, non integrare, benchmark locked 5/10 invariato. Stato: ESEGUITO.


### V5-FRESH03-MANUAL-INVENTORY-01

Attività: censimento diretto dei chunk Chroma del manuale fresh_03; differenza dai test precedenti: lettura di tutte le evidenze della source senza retrieval vettoriale o generazione. Script: `scripts/inspect_v5_fresh03_manual_v1.py`. Commit: `dc28977`; report `docs/v5-fresh03-manual-inventory-01.md` (`4e3eb53`). Risultato: VPS ESEGUITA, 62 chunk della fonte, Chroma 5319 invariato; zero etichette letterali dei quattro moduli, pagina 4 contiene descrizioni senza nomi. Report aggiornato `54af77a`. Decisione: riconciliare intestazioni del documento sorgente con la segmentazione prima di cambiare retrieval; nessuna reindicizzazione o benchmark duplicato. Stato: ESEGUITO.


### V5-FRESH03-HEADING-LOSS-TRACE-01

Attività: confrontare la pagina 4 del PDF originale con i quattro chunk e isolare il confine in cui si perde l'associazione heading-paragrafo, senza ripetere retrieval o generazione. Script: confronto del PDF e dell'inventario VPS esistente; ispezione statica `scripts/ingest_pdfs.py` e `scripts/build_rag_index_v5_multisource.py`; nuovo trace read-only `scripts/inspect_v5_fresh03_heading_loss_v1.py`. Commit script `1019592`. Report: `docs/v5-fresh03-heading-loss-trace-01.md`; trace VPS DA FARE. Risultato: il PDF conferma la sezione `9. Differenze tra moduli` e i quattro heading immediatamente prima dei rispettivi paragrafi; l'inventario precedente mostra i quattro chunk privi di intestazione. `ingest_pdfs.py` esporta la gerarchia Docling senza trasformazioni; il builder si affida a `HybridChunker.contextualize` e salva `chunk.meta.headings`. Gli artefatti registrati non distinguono se Docling abbia mancato la classificazione o il chunker abbia mancato l'associazione. Compilazione sintattica locale dello script OK; dipendenze Docling/Chroma non disponibili localmente; nessun accesso o scrittura alla collection in questa sessione. Decisione: nessuna patch comportamentale finché il trace read-only sulla VPS non mostri quale passaggio è responsabile; eseguire solo quel trace sul JSON Docling esistente, quindi applicare la patch mirata e valutarla su shadow separato. Stato: DIAGNOSI PARZIALE ESEGUITA; causa DA CONFERMARE; fix NON IMPLEMENTATO; nessuna validazione/integrazione/certificazione.

### V5-FRESH03-HEADING-AWARE-RETRIEVAL-01

Attività: recupero heading dei quattro moduli per fresh_03. Script: `v5_targeted_coverage_v1.py`, `smoke_test_rag_v5_e2e.py`, wrapper locked in modalità retrieval-only. Commit: `cfffe6a`, `68ca18d`, `95d4917`, `a9334bb`. Report: `docs/v5-fresh03-heading-aware-retrieval-v2-result.md` (`a5811c5`), evidenza VPS `evaluation/v5_fresh03_heading_aware_retrieval_v2.json` fornita dall'operatore. Risultato: F1–F4 contengono rispettivamente 4-3-3, 4-4-2, 3-5-2, 3-4-2-1, pagina 4, 5319 record invariati, nessuna generazione. Decisione: retrieval VALIDATO; correggere duplicazione heading prima della generazione; nessuna integrazione o certificazione, benchmark 5/10 invariato. Stato: VALIDATO.

### V5-FRESH03-HEADING-AWARE-ANSWER-01

Attività: generazione fresh_03 dopo heading dedup. Script: wrapper locked con --targeted-coverage --only-ids fresh_03. Commit: 1e3dfbe. Report: docs/v5-fresh03-heading-aware-answer-v1-review.md (1c16f88), JSON VPS fornito dall'operatore. Risultato: quattro evidenze corrette e zero citazioni invalide; risposta non nomina i quattro moduli e non delimita la causalità del cambio di modulo. Decisione: risposta non VALIDATA, benchmark 5/10 invariato. Stato: ESEGUITO.

### V5-FRESH03-GENERATION-GUIDANCE-01

Attività: generazione mirata fresh_03 con istruzioni circoscritte. Script: smoke_test_rag_v5_e2e.py e wrapper locked. Commit: c08ba43, 44a2b78. Report: docs/v5-fresh03-generation-guidance-v1-review.md (064f120), JSON VPS fornito dall'operatore. Risultato: 4 moduli citati F1–F4, assenza di prova causale esplicitata, zero citazioni invalide, Chroma 5319 invariato. Decisione: generazione mirata VALIDATA; benchmark locked ancora 5/10; non INTEGRATO né CERTIFICATO. Stato: VALIDATO.

### V5-HEADING-ROUTING-INTEGRATION-01

Attività: generalizzare il recupero delle intestazioni e la guida causale, separando il comportamento dal caso locked fresh_03. Script: scripts/v5_heading_routing_v1.py, scripts/smoke_test_rag_v5_e2e.py, scripts/run_rag_v5_locked_candidate_v2.py. Commit: 0476123, 52499ca, d69d4b7, 8392e6c. Report: docs/v5-heading-routing-integration-01.md (9f2bf7c). Risultato: implementazione opt-in, nessun test VPS eseguito in questa sessione. Decisione: verificare con un unico differenziale --heading-routing senza --targeted-coverage, non ripetere il test shadow validato. Stato: IMPLEMENTATO; benchmark 5/10 invariato, non INTEGRATO né CERTIFICATO.

### V5-HEADING-ROUTING-INTEGRATION-01 — differenziale VPS v1

Attività: verificare il routing generico senza `--targeted-coverage`. Script: `run_rag_v5_locked_candidate_v2.py --heading-routing --only-ids fresh_03`. Commit implementazione: `0476123`, `52499ca`, `d69d4b7`, `8392e6c`. Report: `docs/v5-heading-routing-differential-v1-review.md` (`83ef6b4`); evidenza VPS `evaluation/v5_heading_routing_generic_fresh03_v1.json` fornita dall'operatore. Risultato: test ESEGUITO, nessuna delle quattro intestazioni del manuale nella top8; risposta incompleta; zero citazioni invalide e Chroma invariato a 5319 record. Decisione: non VALIDATO; modificare selezione e promozione delle evidenze prima di eseguire un test tecnicamente diverso. Benchmark ufficiale 5/10 invariato; non INTEGRATO né CERTIFICATO. Stato: ESEGUITO.

### V5-HEADING-ROUTING-INTEGRATION-02 — differenziale VPS v2

Attività: verifica della riserva generica di heading senza targeted coverage. Script: `run_rag_v5_locked_candidate_v2.py --execute --heading-routing --only-ids fresh_03`; implementazione `v5_heading_routing_v1.py`, `v5_heading_reservation_v2.py`, `smoke_test_rag_v5_e2e.py`. Commit: `2e42ac4`, `f86df6c`, `8260c62`. Report: `docs/v5-heading-routing-differential-v2-review.md` (`76ae393`); evidenza VPS `evaluation/v5_heading_routing_generic_fresh03_v2.json` fornita dall'operatore. Risultato: riservati quattro heading ma selezionato il manuale Attacco della Profondità, non Transizioni Offensive e Difensive; manca 4-4-2. Citazioni invalide zero, Chroma 5319 invariato. Decisione: correggere ranking della fonte prima di una nuova prova tecnicamente distinta; benchmark locked 5/10 invariato. Stato: ESEGUITO, non VALIDATO, INTEGRATO o CERTIFICATO.

### V5-HEADING-ROUTING-INTEGRATION-03

Attività: selezione semantica del manuale dopo differenziale v2 non VALIDATO. Script: `v5_source_semantic_rank_v3.py`, `v5_heading_reservation_v2.py`, `smoke_test_rag_v5_e2e.py`. Commit: `cb8cdb1`, `af903d1`, `df514a3`, `4c8bb24`, `362e6cd`. Report: `docs/v5-heading-routing-semantic-v3.md` (`769f4de`). Risultato: implementato cross-encoder per valutare pertinenza di titolo ed estratti dei manuali prima della riserva top8; nessun differenziale v3 ancora eseguito. Decisione: autorizzare un test VPS tecnicamente distinto dal v2; controllare scelta del manuale, citazioni e Chroma. Stato: IMPLEMENTATO; benchmark locked 5/10 invariato, non VALIDATO, INTEGRATO o CERTIFICATO.

### V5-HEADING-ROUTING-INTEGRATION-03 — differenziale VPS V3

Attività: verificare il ranking semantico V3 con un unico differenziale VPS `fresh_03`, tecnicamente distinto da V2. Script: `run_rag_v5_locked_candidate_v2.py --execute --heading-routing --only-ids fresh_03`, `smoke_test_rag_v5_e2e.py`, `v5_heading_reservation_v2.py`, `v5_source_semantic_rank_v3.py`. Commit implementazione: `cb8cdb1`, `af903d1`, `df514a3`, `4c8bb24`, `362e6cd`; ramo al test `eef7e3c`. Report: `docs/v5-heading-routing-differential-v3-review.md`; evidenza VPS `evaluation/v5_heading_routing_generic_fresh03_v3.json`, SHA-256 `b5ebc372a7a1155b88fd217054b1030114c3d1e88593b66b7f1db2deb9cd4e6a`. Risultato: `COMPLETE 1/1`, 136.03 s, fonte scelta `Manuale_Diagonali_Difensive` anziché `Transizioni Offensive e Difensive`; heading riservati `4-2-3-1`, `4-3-3`, `4-4-2`, copertura incompleta dei quattro moduli richiesti. Limite causale esplicitato, citazioni invalide 0, Chroma 5319 invariato. Decisione: non integrare V3 e non ripetere il test; una V4 richiede una differenza tecnica documentata che combini pertinenza e copertura senza hardcoding del benchmark. Benchmark locked 5/10 invariato. Stato: ESEGUITO; non VALIDATO, INTEGRATO o CERTIFICATO.

### V5-SOURCE-RANKING-TRACE-04

Attività: rendere ispezionabili i punteggi V3 perché il differenziale precedente registra la fonte errata ma non i punteggi o la copertura dei candidati; non ripetere generazione o benchmark. Script: `v5_source_semantic_rank_v3.py`, `v5_heading_reservation_v2.py`, `smoke_test_rag_v5_e2e.py`, `run_rag_v5_locked_candidate_v2.py`, `tests/test_v5_source_semantic_rank_v3.py`. Commit: `1355110`. Report: `docs/v5-source-ranking-trace-04.md`. Risultato: flag opt-in `--source-ranking-trace`, consentito solo con `--heading-routing --retrieval-only`; output fonte, score, formazioni e numero estratti. Test offline 2/2, compilazione sintattica e diff check superati; VPS DA FARE. Decisione: consentire una sola diagnostica retrieval-only `fresh_03`, senza generazione, mutazioni Chroma o aggiornamento benchmark. Stato: IMPLEMENTATO; non ESEGUITO, VALIDATO, INTEGRATO o CERTIFICATO.

### V5-SOURCE-RANKING-TRACE-04 — diagnostica VPS

Attività: eseguire una sola diagnostica retrieval-only `fresh_03` per registrare la graduatoria completa dei manuali senza generazione. Script: `run_rag_v5_locked_candidate_v2.py --execute --heading-routing --source-ranking-trace --retrieval-only --only-ids fresh_03`, implementazione `1355110`. Report: `docs/v5-source-ranking-trace-04.md`; evidenza VPS `evaluation/v5_source_ranking_trace_fresh03_v1.json`, SHA-256 `c29689e627798bf88c4f4b64b7e72ba0aa5e51d52fa1ae798c76cb611b9639a9`. Risultato: `COMPLETE 1/1`, 6.73 s, Chroma 5319 invariato; `Manuale_Diagonali_Difensive` primo a `-4.685579` con tre heading, `Transizioni Offensive e Difensive` seconda a `-5.848974` con i quattro heading richiesti. Decisione: dimostrato che il solo score semantico privilegia somiglianza lessicale senza copertura; non ripetere il trace o generare. Progettare V4 solo con combinazione generica documentata di pertinenza e copertura, senza ID benchmark o lista hardcoded. Benchmark locked 5/10 invariato. Stato: ESEGUITO; non VALIDATO, INTEGRATO o CERTIFICATO.

### V5-SOURCE-HYBRID-RANK-V4

Attività: correggere la selezione V3 combinando pertinenza e copertura in modo generico. Script: `v5_source_hybrid_rank_v4.py`, `v5_heading_reservation_v2.py`, `smoke_test_rag_v5_e2e.py`, `tests/test_v5_source_hybrid_rank_v4.py`. Commit: `30b04d4`. Report: `docs/v5-source-hybrid-rank-v4.md`. Risultato: fonti entro margine semantico 1.5 competono per numero di formazioni, poi score e nome; fonti oltre margine restano escluse. Nessun ID benchmark, nome fonte o lista moduli hardcoded. Test offline V3/V4 5/5, compilazione e diff check superati; VPS DA FARE. Decisione: consentire una sola verifica retrieval-only fresh_03 con trace; generazione solo dopo fonte, heading e indice corretti. Benchmark locked 5/10 invariato. Stato: IMPLEMENTATO; non ESEGUITO, VALIDATO, INTEGRATO o CERTIFICATO.

### V5-SOURCE-HYBRID-RANK-V4 — retrieval VPS

Attività: verificare la selezione ibrida V4 senza generazione. Script: wrapper locked con `--heading-routing --source-ranking-trace --retrieval-only --only-ids fresh_03`, implementazione `30b04d4`. Report: `docs/v5-source-hybrid-rank-v4.md`; evidenza VPS `evaluation/v5_source_hybrid_rank_fresh03_v1.json`, SHA-256 `51f01a0280434501b6eb2f1d6fedc6adcd92198f88a7c6c26c19c7c145367ab2`. Risultato: `COMPLETE 1/1`, 7.21 s, fonte selezionata `Transizioni Offensive e Difensive`, heading riservati `3-4-2-1`, `3-5-2`, `4-3-3`, `4-4-2`, Chroma 5319 invariato. Decisione: retrieval V4 VALIDATO per fresh_03; autorizzare una sola generazione differenziale senza targeted coverage, poi valutazione claim-level. Benchmark locked 5/10 invariato. Stato: VALIDATO limitatamente al retrieval; non INTEGRATO o CERTIFICATO.

### V5-SOURCE-HYBRID-RANK-V4 — generazione VPS

Attività: eseguire l'unica generazione differenziale autorizzata dopo il retrieval V4 validato. Script: wrapper locked con `--execute --heading-routing --only-ids fresh_03`, implementazione `30b04d4`. Report: `docs/v5-source-hybrid-rank-v4.md`; evidenza VPS `evaluation/v5_source_hybrid_generation_fresh03_v1.json`, SHA-256 `d446a18cf18ed9b7ec4fd7b6e8f751188b82fc222adda12927982e6196bf4a6e`. Risultato: `COMPLETE 1/1`, 138.78 s; risposta esplicita `3-4-2-1`, `3-5-2`, `4-3-3`, `4-4-2` con F1–F4, distingue condizioni operative e prova causale, richiede evidenze comparative, citazioni invalide 0, Chroma 5319 invariato. Decisione: fresh_03 V4 VALIDATO; non ripetere retrieval o generazione. Prima dell'integrazione di default eseguire una regressione completa tecnicamente distinta e rivalutare il benchmark complessivo. Benchmark ufficiale 5/10 invariato fino a tale valutazione. Stato: VALIDATO; non INTEGRATO o CERTIFICATO.
