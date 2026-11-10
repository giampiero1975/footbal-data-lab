# Registro autorevole esperimenti — Tactical Engine

Ultimo aggiornamento: 2026-10-27. GitHub è la fonte autorevole dello **stato**; i report runtime sulla VPS sono evidenze da collegare, non automaticamente versionate. Questo registro è obbligatorio per ogni nuova attività.

### 2026-11-10 — Rivalutazione indipendente incrementale dopo R1

Attività: `RD-RAG-V5-REMEDIATION-A-POST-R1-INDEPENDENT-REASSESSMENT-01`.
Script: comandi locali read-only Git/AST/JSON e lettura manuale dei rami;
nessun import applicativo, helper di dominio o test eseguito. Commit:
documentale che pubblica contestualmente report, fatti, TODO e registro.
Report: `docs/rag-v5-remediation-a-post-r1-independent-reassessment-01.md`;
evidenze: `docs/remediation-a-post-r1-independent-reassessment-facts-01.json`.
HEAD iniziale locale/GitHub 5794e2c, tree pulito; tecnico R1 5bfa489. Nessuna
rivalutazione già registrata. Risultato: sola frase normativa cambiata rispetto
a c00af6d; caller numeric return same prima dei literal, limite versionato
esplicito. Validator/schema invariati, nessuna normalizzazione. Ricerca
incrementale su stati, entità/assi, raffinamento spaziale nel caller, quantifier
non numeric, conditions, polarity e derivazione label: nessuna nuova
contraddizione normativa bloccante. Preservati limite numeric e formulazione
label meno precisa già non bloccante. Conferma statica handoff 6.967 byte,
user storico 7.311 (+373), schema 16.869 da evidenza precedente invariata.
Nessuna stima token, compilazione grammar o accesso backend. Decisione unica
**A**: idoneo alla verifica separata del backend, non una generazione né una
compatibilità reale dichiarata. Stato: rivalutazione **ESEGUITO**, **VALIDATO**
come analisi documentale incrementale; patch **IMPLEMENTATO**, backend
**DA FARE**. Sedici e cinque PASS storici conservati, zero test ripetuti o
codice/test modificati. Accuratezza generativa, Gate, integrazione e
certificazione **BLOCCATO**. Zero VPS, modelli, runtime-05, staging, wrapper,
merge/deploy; precedenti report invariati. STOP dopo pubblicazione.

### 2026-11-10 — Correzione R1 numeric/literal

Attività: `RD-RAG-V5-REMEDIATION-A-R1-NUMERIC-LITERAL-01`. Script applicativo:
sola frase in `v5_tactical_semantic_support_s2_spatial_v2_extraction.py:358`;
nuovi controlli `tests/test_v5_spatial_extraction_numeric_literal_r1.py`.
Commit tecnico `5bfa4897e93d5d8edef0bc79371aa36b1b1409ae`; documentale successivo
pubblica insieme report, risultati, TODO e registro. Report:
`docs/rag-v5-remediation-a-r1-numeric-literal-closeout-01.md`; evidenze:
`docs/remediation-a-r1-numeric-literal-results-01.json`. HEAD iniziale
locale/GitHub c00af6d, tree pulito; R1 riconfermato prima della modifica.
Differenza motivata nella docstring prima dei controlli: ramo caller fra
numeric/literal non coperto dai sedici precedenti. Risultato: 5/5 PASS in
0,017 s, una sola esecuzione della nuova suite; numeric 2/3 e 2/2 same senza
dispatch, numeric/many in entrambe le direzioni different con helper reale,
sei sottocasi unknown/ambiguous prioritari, testo normativo coerente.
Nessuna suite storica 37/13/16 ripetuta o PASS invalidato retroattivamente.
Intero sorgente identico fuori dalla sostituzione; validatore, schema/shape,
locator/precontrollo, legacy, Gold/dataset, provenance/promozione, parametri e
wrapper invariati. Handoff 6.967 byte (+373), user storico 7.311 byte;
nessuna stima token o prova decoder. Decisione: idonea a nuova revisione del
contratto, non eseguita; R1 superato offline, limite numeric preservato.
Stato: correzione **IMPLEMENTATO**, verifiche **ESEGUITO** e **VALIDATO**
offline; accuratezza generativa, Gate, integrazione e certificazione **BLOCCATO**.
Zero VPS, modelli, inferenze, backend, runtime-05, staging/wrapper nuovi,
merge/deploy o modifiche servizi/panel. STOP dopo pubblicazione.

### 2026-11-10 — Revisione indipendente remediation A

Attività: `RD-RAG-V5-DUAL-BLOCKER-REMEDIATION-A-INDEPENDENT-REVIEW-01`.
Script: `docs/remediation-a-independent-static-audit-01.py`, sola lettura
Git/AST/literal/JSON, senza import applicativi o funzioni di dominio. Commit:
documentale che pubblica report, script/fatti, TODO e registro insieme.
Report: `docs/rag-v5-dual-blocker-remediation-a-independent-review-01.md`;
fatti: `docs/remediation-a-independent-review-facts-01.json`. HEAD iniziale
locale/GitHub c864040, tree pulito; tecnico 0ea62c0, baseline finale 13814c2.
Risultato: R1 bloccante accertato staticamente: istruzione numeric con literal
diversi impone different, ma `_expected_comparison` restituisce same per
value numeric uguali prima del dispatch al helper. Sedici PASS letti, non
rieseguiti; parità slot non copre quel confronto fra lati. Fail-closed,
locator, validatore finale, provenance e legacy preservati. Unknown legittimo
resta rappresentabile; schema più permissivo dei gate su vincoli residui.
Nuovo user per il caso storico 6.938 byte contro 2.663, istruzioni 6.594
contro 2.319; schema 16.869 byte dalla misura precedente. Nessuna stima token:
budget e compatibilità decoder reale non verificabili offline. Decisione unica
**B**, correggere prima di ulteriori verifiche, senza implementazione o nuova
generazione. Stato: revisione **ESEGUITO**, analisi documentale **VALIDATO**;
patch **IMPLEMENTATO**, idoneità al passo backend **BLOCCATO**, correzione
**DA FARE** previa autorizzazione. Accuratezza generativa, Gate, integrazione
e certificazione **BLOCCATO**. Zero test applicativi/suite, VPS, modelli,
wrapper, staging, runtime-05, merge/deploy/promozioni. STOP alla pubblicazione.

### 2026-11-10 — Remediation offline A dopo runtime-04

Attività: `RD-RAG-V5-DUAL-BLOCKER-REMEDIATION-A-OFFLINE-01`. Script:
`shadow_nli_spatial_relations_v2_inference.py`,
`v5_tactical_semantic_support_s2_spatial_v2_extraction.py`; nuova suite
`tests/test_v5_spatial_extraction_status_contract_v1.py`. Commit tecnico:
`0ea62c0ef1f0adfcd928c2893f069de060275381`. Report:
`docs/rag-v5-dual-blocker-remediation-a-offline-01.md`; risultati
`docs/runtime04-remediation-a-offline-results-01.json`. Baseline documentale
iniziale locale/GitHub `8fca97f`, tree pulito; applicativa precedente `13814c2`.
Risultato: handoff normativo completo per stati, sentinelle, confronto e
grounding separato; matrici lette dalle costanti finali. Schema correlato con
anyOf completi e shape check deterministico delle regole residue; nessun
repair o forzatura label/comparison. Run iniziale nuovo 13/13; dopo correzione
di duplicazioni locali e completamento della copertura, 15/15 PASS; nuovo
controllo aggiuntivo di parità finale 1/1 su 1.050 combinazioni. Sedici controlli
distinti coperti, nessuna suite storica 37/37 o wrapper 13 ripetuta. Raw
runtime-04 immutato, rejection anticipata senza promozione; legacy identico
al frozen, locator/validatore/dataset/panel/ops invariati. Limiti: checker del
solo subset, nessun compilatore grammar/backend remoto o tokenizer reale;
vincoli non esprimibili mantenuti fail-closed nel deterministico. Decisione:
revisione indipendente raccomandata prima di ogni prova generativa; nessun
runtime, wrapper/staging nuovo, modello o accesso VPS, merge/deploy. Stato:
patch **IMPLEMENTATO**, verifiche **ESEGUITO**, proprietà coperte **VALIDATO**
offline; accuratezza delle contraddizioni, Gate, integrazione e certificazione
**BLOCCATO**. Report/TODO/registro pubblicati contestualmente, STOP.

### 2026-11-10 — Forense offline unknown/same runtime-04

Attività: `RD-RAG-V5-DUAL-BLOCKER-RUNTIME04-UNKNOWN-SAME-FORENSIC-01`. Script:
sola lettura Git/stdlib locale, hash, JSON e AST di costanti; nessun import o
funzione applicativa, test, modello o accesso VPS. Commit: documentale che
pubblica report, fatti derivati, TODO e registro insieme. Report:
`docs/rag-v5-dual-blocker-runtime04-unknown-same-forensic-01.md`; fatti
`docs/runtime04-unknown-same-forensic-facts-01.json`. Baseline documentale
locale/GitHub `86bfcfc`, working tree pulito; applicativa `13814c2` invariata.
Risultato: 27 originali conformi ai blob pubblicati; raw parsato coincide con
extraction. Messaggio effettivo conforme al prompt baseline, file prompt con
solo LF finale introdotto dalla persistenza. Sedici slot unknown, due item
condizioni ambiguous e otto comparison same; lettura statica di
`_expected_comparison` prescrive unknown in tutte le dimensioni. Origine già
nel raw; schema senza default, ma status/value/fragments indipendenti e
prompt privo di precedenza esplicita. Lacuna handoff accertata, contributo
causale al comportamento del modello non isolato. Entrambi i valori abundant
non rappresentano l'opposizione spaziale; nessuna causa cognitiva inventata.
Precontrollo corretto, locator e validatore finale non raggiunti. Decisione:
due sole alternative non implementate; raccomandata A (handoff normativo e
schema correlato), B distinta (nuovo trasporto relations-only con derivazione
sistemica limitata). Nessuna forzatura di comparison o Gold, nessun runtime
o analisi runtime-03 ripetuta. Stato: revisione **ESEGUITO**, catena e diagnosi
documentale **VALIDATO** nel perimetro probatorio; alternative **DA FARE**
previa decisione, accuratezza generativa, nuovi runtime, Gate, integrazione
e certificazione **BLOCCATO**. STOP dopo pubblicazione.

### 2026-11-10 — Singola esecuzione runtime-04

Attività: `RD-RAG-V5-DUAL-BLOCKER-RUNTIME04-EXECUTION-01`. Script: launcher
runtime-04 approvato, SHA `abf6db3060b68cbc1e5d9e1c28ea13e2cb3dbce09f2ae2b5c00f8ec1e7f55f17`,
invocato una sola volta senza modifiche. Baseline applicativa
`13814c20d80bca4d9cb4cb08a288b6e7b31dac0d`; iniziale documentale locale/GitHub
`c699639`, tree pulito. Commit: documentale con report, originali, metadati,
TODO e registro pubblicati insieme. Report:
`docs/rag-v5-dual-blocker-runtime04-execution-01.md`; evidenze originali e
inventari `evaluation/runtime04_execution_01/`.
Risultato: preflight immediato positivo, nessun tentativo preesistente, lock
sondato/rilasciato e acquisito poi dal wrapper. Una chiamata, una generazione
completa, 132,537836 s, done stop, processo generativo exit 0, launcher/wrapper
exit 80. Stato completed_fail_closed, boundary
`E_EXTRACTION_SEMANTIC_INCONSISTENT`, dettaglio
`E_EXTRACTION_COMPARISON_INCONSISTENT` su comparison. Output propone supported
con status unknown/comparison same; label autorevole e semantic match nulli,
Gold contradicted. Precontrollo arresta prima del locator: records vuoti,
witness/validation assenti, nessuna promozione. Finalizzazione completa,
inventari 23+1+1 conformi, 27 file originali preservati e pubblicati; staging
pulito e hash wrapper 03/04 invariati. Decisione: tentativo consumato, zero
retry/repair/fallback; nessun altro caso o runtime. Proposta sola revisione
offline mirata della nuova incoerenza prima di ulteriori modifiche/prove,
non eseguita. Stato: tentativo **ESEGUITO**, completamento tecnico,
finalizzazione e fail-closed del caso **VALIDATO**; accuratezza generativa,
contraddizioni, ulteriore runtime, Gate, integrazione e certificazione
**BLOCCATO**. Nessuna modifica applicativa, servizi, Chroma, panel, merge o
deploy; nessuna promozione o certificazione generale.

### 2026-11-10 — Trasferimento wrapper runtime-04 e preflight non generativo

Attività: `RD-RAG-V5-DUAL-BLOCKER-RUNTIME04-TRANSFER-NONGENERATIVE-PREFLIGHT-01`.
Script: due connessioni SSH con stdlib Python inline, trasferimento binario
esclusivo/rilettura e diagnostica separata `/usr/bin/python3 -B -I`; nessun
launcher, corpo remoto o blocco applicativo del wrapper eseguito. Commit:
documentale che pubblica report, JSON di evidenza, TODO e registro insieme.
Report: `docs/rag-v5-dual-blocker-runtime04-transfer-nongenerative-preflight-01.md`;
evidenza `evaluation/runtime04_transfer_nongenerative_preflight_evidence_01.json`.
Baseline documentale iniziale locale/GitHub `59e8917`, tree pulito;
applicativa `13814c20d80bca4d9cb4cb08a288b6e7b31dac0d` invariata.
Risultato: wrapper remoto 47.755 byte, SHA locale/remoto
`abf6db3060b68cbc1e5d9e1c28ea13e2cb3dbce09f2ae2b5c00f8ec1e7f55f17`,
confronto integrale byte-per-byte positivo, file regolare `football:football`
modo `0600`; originale runtime-03 invariato, nessuna sovrascrittura. Snapshot
non generativo: staging detached esatto e pulito, common dir interna, evidenze
blob/fsck precedenti riusate; artefatti assenti, lock regolare `0600` senza
entry procfs corrispondenti e mai acquisito, nessun runtime visibile rilevato.
Python 3.12.3 e strumenti presenti, dipendenze stdlib verificate senza import
applicativi o installazioni. Sole GET tags/ps/version: Ollama 0.40.5, digest
qwen3.5:9b atteso, `models=[]`. Zero richieste generative/esecuzioni wrapper;
nessuna suite 37/13 o validazione completa staging ripetuta. Decisione: STOP
dopo report, nessuna modifica a codice/servizi/indici/panel e nessuna promozione.
Stato: trasferimento **ESEGUITO**, identità e preflight non generativo
**VALIDATO** nel solo snapshot osservato; lock/concorrenza non garantiti per
il futuro. Runtime-04, accuratezza delle contraddizioni, Gate, integrazione e
certificazione **BLOCCATO** fino alle autorizzazioni e prove pertinenti.

### 2026-11-10 — Staging indipendente runtime-04

Attività: `RD-RAG-V5-DUAL-BLOCKER-RUNTIME04-STAGING-PREPARATION-01`. Script:
comandi Git e stdlib Python inline, tre sessioni SSH per preflight, upload del
solo bundle e clone/verifica; nessun modulo applicativo eseguito. Commit:
documentale con report `docs/rag-v5-dual-blocker-runtime04-staging-preparation-01.md`,
evidenza `evaluation/runtime04_staging_preparation_evidence_01.json`, TODO e
questo registro. Baseline documentale iniziale locale/GitHub `83abcde`,
working tree pulito; applicativa congelata
`13814c20d80bca4d9cb4cb08a288b6e7b31dac0d`.
Risultato: destinazioni libere e parent reale; bundle completo con unico ref
di branch alla baseline, 2.728.883 byte, SHA-256 locale/remoto
`05c4f8726c1a1f701ec46af63a32f066caac416d6b69f3578dc69ddf9bd0ae29`.
Anomalia di ref nonbranch del primo bundle rilevata e risolta solo localmente
prima dell'upload con artefatto distinto, senza cambiare baseline. Clone
indipendente `staging/spatial-v2-dual-blocker-13814c2`, detached esatto, status
vuoto, common dir interna, nessun alternate/symlink critico/hardlink Git;
fsck full strict e verifica bundle exit 0, quattro blob applicativi e hash
checkout conformi al wrapper locale. Nove snapshot Git prima/dopo coincidenti
(operativo + otto staging storici), artefatti runtime-04 ancora assenti.
Decisione: STOP dopo staging; nessun upload o esecuzione wrapper, inferenza,
download corpus/dipendenze, suite 37/13, Chroma, servizio, panel, merge o deploy.
Stato: bundle/trasporto **VALIDATO**, staging **IMPLEMENTATO**, controlli
**ESEGUITO**, staging isolato **VALIDATO**; trasferimento wrapper/preflight
**DA FARE** con autorizzazione successiva; accuratezza delle contraddizioni,
runtime, Gate, integrazione e certificazione **BLOCCATO**.

### 2026-11-10 — Preparazione locale wrapper runtime-04

Attività: `RD-RAG-V5-DUAL-BLOCKER-RUNTIME04-LOCAL-PREPARATION-01`. Script:
`operations/runtime-wrappers/prepare_runtime04_wrapper.py`, nuova copia
`spatial-v2-extraction-locator-q3-04-runtime-04.sh` e controlli
`test_runtime04_wrapper_delta.py`; originale e diff completo versionati.
Commit tecnico: `56fba214c6a2d438bf1e1c4383dc920654cfc5c7`. Report:
`docs/rag-v5-dual-blocker-runtime04-local-preparation-01.md`, pubblicato
insieme agli aggiornamenti TODO/registro nella stessa sessione. Baseline
documentale iniziale `cf6b63d`, locale/GitHub allineati e tree pulito;
baseline applicativa obbligatoria `13814c20d80bca4d9cb4cb08a288b6e7b31dac0d`.
Risultato: originale recuperato read-only, 45.964 byte e SHA storico invariati;
nuovo wrapper 47.755 byte, SHA-256
`abf6db3060b68cbc1e5d9e1c28ea13e2cb3dbce09f2ae2b5c00f8ec1e7f55f17`.
Delta limitato a identità/percorsi/blob e ramo semantico dedicato con details
versionati, provenance senza localizzazione, assenza witness/validation e
non promozione; nessuna auto-correzione. Nuovi controlli specifici del wrapper:
13 distinti, 12 PASS iniziali e un confronto statico corretto per l'attempt ID
autorizzato, rieseguito da solo 1/1 PASS. Bash -n launcher/corpo, cinque blocchi
Python compilati, verificatore estratto provato offline e alterazioni respinte;
originale preservato, diff e blob Git verificati. Nessuna suite 37/37 ripetuta.
Decisione: STOP dopo pubblicazione; nessuna esecuzione wrapper, inferenza,
upload o staging remoto; codice applicativo/locator/validatore invariati.
Stato: wrapper **IMPLEMENTATO**, controlli **ESEGUITO**, preparazione locale
**VALIDATO**; staging/preflight **DA FARE** previa autorizzazione; runtime,
accuratezza delle contraddizioni, Gate, integrazione e certificazione
**BLOCCATO**. Backup chiave resta separato.

### 2026-11-10 — Verifica read-only wrapper e artefatti runtime-03

Attività: `RD-RAG-V5-DUAL-BLOCKER-RUNTIME03-READONLY-READINESS-01`. Script:
tre connessioni SSH batch, stdlib Python inline e Git `--no-optional-locks`,
senza import applicativi, esecuzione wrapper o scritture VPS. Commit:
documentale che aggiunge il report e aggiorna insieme TODO/registro, ricercabile
nella storia di `docs/rag-v5-dual-blocker-runtime03-readonly-readiness-01.md`.
Baseline documentale iniziale locale/GitHub `b180f97`, tree locale pulito;
baseline applicativa futura `13814c20d80bca4d9cb4cb08a288b6e7b31dac0d`.
Risultato: wrapper storico 45.964 byte e SHA-256
`ba0160e0381bbe5242196a555ab5e85ae0109c0b383bc9a79825c14b4fd44d57`
conformi; inventari verificati 23+1+1, fail-closed storico e finalizzazione
riconfermati. Parametri reali: 2.048 token, ctx 4.096, think false, HTTP 360 s,
supervisore 450 s/kill-after 15 s. Staging storico pulito a `db3ad66`, nuovi
target proposti assenti; operativo a `1a80fe0`, senza delta tracked ma con 17
percorsi untracked preservati. Rilievo statico nuovo: il verificatore storico
non distingue `E_EXTRACTION_SEMANTIC_INCONSISTENT` dalla localizzazione fallita
e respingerebbe il nuovo boundary come errore di verifica contenuto; occorre
adattare la copia futura, senza modificare locator o validatore finale.
Decisione: nessuna suite 37/37 o forense ripetuta; proposta preparazione locale
wrapper con ramo diagnostico dedicato, da autorizzare separatamente; nessun
trasferimento, staging o runtime. Stato: ricognizione **ESEGUITO**, identità e
integrità storiche **VALIDATO**; wrapper post-patch e staging **DA FARE**;
backup cifrato **DA FARE** separato e non bloccante; accuratezza generativa,
contraddizioni, runtime, Gate, integrazione e certificazione **BLOCCATO**.

### 2026-11-10 — Accesso SSH v3 dal nuovo PC

Attività: `RD-FOOTBALL-VPS-SSH-V3-NEW-PC-ACCESS-01`. Script: OpenSSH locale,
blocco Python stdlib di append eseguito dal titolare nella sessione VPS con
password, unico test SSH Codex read-only. Commit: documentale che aggiunge
`docs/football-vps-ssh-v3-new-pc-access-01.md` e aggiorna contestualmente TODO e
questo registro, rintracciabile dalla storia del report. Baseline iniziale
locale/GitHub `103fd8fb1de3d7712462ccb2e00e1cc63b1b4ae1`, working tree pulito.
Risultato: fingerprint pubblica v3
`SHA256:fpb/vDKCpmsoJD04J7KU3hCvlQqNL389hBp61Umj8iM`; host Ed25519
verificato contro known_hosts. Uso della privata senza passphrase accettato
esplicitamente dal titolare dopo i controlli di cifratura; nessun segreto
registrato. Policy script non firmati preservata; installazione manuale
password con append senza duplicati e vecchi byte invariati. Alias nuovo
`football-vps` con sola v3 e controllo host rigoroso. Singolo test Codex exit 0,
autenticazione publickey, utente football, conteggio v3 1 e hash remoto
`07c6bb9c1259c24dce3ed6b7db25d3e9eace1e14fbe2fd1912cefbfaa509a78a`
coincidente con l'esito manuale. Decisione: STOP connessioni e attività VPS;
nessuna revoca, modifica servizi/codice, staging o inferenza. Stato:
installazione/alias **ESEGUITO**, accesso SSH **VALIDATO**; backup cifrato
indipendente **DA FARE**; problema generativo RAG V5, contraddizioni, Gate,
integrazione e certificazione **BLOCCATO**. Il precedente blocco di accesso
nuovo PC è superato esclusivamente per la nuova identità v3.

### 2026-11-10 — Nuovo PC e preparazione runtime Dual Blocker

Attività: `RD-RAG-V5-DUAL-BLOCKER-NEW-PC-PREPARATION-01`. Script: soli comandi
locali Git, inventario nomi file SSH e confronto statico AST/hash con stdlib;
nessuno script applicativo o wrapper eseguito. Commit: documentale che aggiunge
il report e aggiorna contestualmente TODO e questo registro, rintracciabile
con `git log -1 -- docs/rag-v5-dual-blocker-new-pc-runtime-preparation-01.md`
dalla directory Tactical Engine. Report:
`docs/rag-v5-dual-blocker-new-pc-runtime-preparation-01.md`.
Risultato: repository `C:\laragon\www\footbal-data-lab`, branch corretto,
HEAD locale/remoto `13814c20d80bca4d9cb4cb08a288b6e7b31dac0d` dopo fetch,
0/0, working tree iniziale pulito e un solo worktree. Patch `56a7b72`, test
storici 37/37 e revisione indipendente riconciliati; locator e validatore
invariati, precontrollo attivo prima del locator. Preparato piano per singolo
`q3_04` con nuova baseline, riuso controllato del wrapper runtime-03 e
inventari; wrapper originale non versionato, adattamento non materializzato.
SSH installato e directory `.ssh` presente, ma mancano config/alias e chiave
v2 documentata; nessuna chiave alternativa provata, zero connessioni VPS.
Decisione: nessun test equivalente, inferenza, trasferimento, modifica VPS,
panel o codice; prima accesso autorizzato e verifica wrapper, poi autorizzazioni
separate per staging/trasferimenti e singolo runtime. Stato: preparazione
documentale **ESEGUITO**; accesso VPS **BLOCCATO**, staging e wrapper adattato
**DA FARE**; accuratezza generativa, contraddizioni, runtime, Gate, integrazione
e certificazione **BLOCCATO**. La baseline applicativa resta distinta dal
commit di pubblicazione documentale.

### 2026-11-09 — Revisione indipendente patch dual blocker RAG V5

Attività: `RD-TSC-V2-D3-S2-RAG-V5-DUAL-BLOCKER-INDEPENDENT-REVIEW-01`.
Esaminati staticamente commit tecnico, handoff, schema extraction, ordine del
precontrollo, regole Spatial V2, locator invariato e 37 risultati già registrati;
nessuna suite rieseguita. Vincolo side-bound e blocco deterministico delle
incoerenze **VALIDATO** offline, senza difetti bloccanti. Restano non bloccanti
la diagnostica comparison aggregata e l'assenza nel repository del raw
runtime-03 come fixture byte-identica. Accuratezza generativa **BLOCCATO**;
futura prova controllata **DA FARE** previa autorizzazione, una generazione per
invocazione e zero retry/repair/fallback. Revisione **ESEGUITO**. Report
`docs/tactical-semantic-support-s2-rag-v5-dual-blocker-independent-review-01.md`.

### 2026-11-09 — Remediation offline dual blocker RAG V5

Attività: `RD-TSC-V2-D3-S2-RAG-V5-DUAL-BLOCKER-OFFLINE-REMEDIATION-01`.
Rafforzati esclusivamente handoff e schema extraction con separazione
claim/evidence, definizioni degli slot, matrice asse-valori e regole normative
già versionate. Il nuovo precontrollo fail-closed verifica asse/valore e riusa
le regole comparison del validatore Spatial V2 prima del locator; locator e
validatore finale sono invariati. Test differenziali e regressioni direttamente
interessate 37/37 PASS (16 extraction/locator, 21 Spatial V2). Commit tecnico
`56a7b72135595e99a98ff2fb5b1bcc3d6a0c9ebf`. Patch **IMPLEMENTATO**,
verifiche **ESEGUITO**, proprietà deterministiche **VALIDATO** offline.
Efficacia generativa, runtime, Gate, integrazione e certificazione **BLOCCATO**.
Report `docs/tactical-semantic-support-s2-rag-v5-dual-blocker-offline-remediation-01.md`.

### 2026-11-09 — Revisione causale dual blocker RAG V5

Attività: `RD-TSC-V2-D3-S2-RAG-V5-DUAL-BLOCKER-CAUSAL-REVIEW-01`.
Analizzati staticamente artefatti originali runtime-03, codice e forensi
pregresse. Localizzazione: la raw response contiene già un frammento evidence
in `claim_relation.reference`; nessun difetto del parser/locator, che blocca
side-bound. Semantica: falso `supported` indipendente e storico; l'extraction
usa `space_availability/between` e comparison `same` incoerenti con valori,
entity/condition ID e quantificatori. L'handoff non trasmette integralmente
definizioni dei campi, matrice asse→valori e derivazione; il precontrollo
extraction non applica ancora le regole già presenti nel validatore finale.
Cause dirette **VALIDATO**, causa cognitiva interna non determinabile.
Raccomandata patch offline minima di handoff e precontrollo deterministico,
senza auto-correzioni. Revisione **ESEGUITO**; implementazione/test sono ora
tracciati nella voce precedente;
runtime, Gate, integrazione, panel e certificazione **BLOCCATO**. Report
`docs/tactical-semantic-support-s2-rag-v5-dual-blocker-causal-review-01.md`.

### 2026-11-09 — Runtime-03 Extraction Locator eseguito una volta

Attività: `RD-TSC-V2-D3-S2-SPATIAL-V2-EXTRACTION-LOCATOR-RUNTIME-03`.
Preflight corretto PASS; wrapper remoto conforme invocato esattamente una volta.
Una chiamata di trasporto e una generazione completa in 142,34 s, senza retry,
repair o fallback. Extraction JSON valida per parsing/shape; il locator ha
localizzato 10/11 frammenti, mentre
`claim_relation.reference.selected_fragments[0]` è assente dal lato claim.
Risultato `not_evaluable`, reason code
`E_EXTRACTION_LOCALIZATION_NOT_UNIQUE`, exit wrapper 80, nessun witness o
validation e `promotion_authorized=false`. La label proposta `supported` non è
stata promossa né confrontata autorevolmente col Gold `contradicted`.
Inventari SHA-256/finalizzazione PASS e staging invariato. Tentativo
**ESEGUITO**; completamento tecnico e fail-closed **VALIDATO** nel singolo caso;
localizzazione, semantica, Gate, integrazione e certificazione **BLOCCATO**.
Report
`docs/tactical-semantic-support-s2-spatial-v2-extraction-locator-runtime-03-run-01.md`.

### 2026-11-09 — Diagnosi dipendenza Python runtime-03

Attività: `RD-TSC-V2-D3-S2-SPATIAL-V2-EXTRACTION-LOCATOR-RUNTIME-03`, diagnosi
read-only. `/usr/bin/python3` è Python 3.12.3, non virtualenv, con `pydantic`
assente e `requests 2.31.0`; la virtualenv operativa esistente contiene
`pydantic 2.14.1` e `requests 2.34.2`. Il wrapper usa però il percorso assoluto
di sistema in tutti i processi figli. Analisi statica e import read-only
dimostrano che i tre moduli Extraction Locator effettivi dipendono soltanto da
stdlib e moduli locali e sono importabili con `/usr/bin/python3`. Il blocco
precedente deriva dal requisito esterno improprio di importare `pydantic`, non
da una dipendenza del runner corrente. Diagnosi **ESEGUITO/VALIDATO**;
correzione della sola procedura preflight **DA FARE** previa autorizzazione,
senza installazioni o modifiche. Runtime-03, Gate, integrazione e certificazione
restano **BLOCCATO**. Report
`docs/tactical-semantic-support-s2-spatial-v2-extraction-locator-runtime-03-python-dependency-diagnosis-01.md`.

### 2026-11-09 — Runtime-03 bloccato nel preflight Python

Attività: `RD-TSC-V2-D3-S2-SPATIAL-V2-EXTRACTION-LOCATOR-RUNTIME-03`, esecuzione
singola condizionata. Wrapper conforme trasferito in percorso isolato esterno a
checkout/staging e verificato remotamente: file regolare `football:football`,
modo 0600, 45.964 byte, SHA-256 `ba0160e0...44d57`. Staging presente a
`db3ad66`, status pulito e directory artefatti runtime-03 assente. Il preflight
immediato si è arrestato al primo controllo negativo: `/usr/bin/python3` non
importa `pydantic` (`ModuleNotFoundError`). Nessun retry, installazione o
adattamento: 0 invocazioni wrapper, 0 trasporti, 0 generazioni. Identità e
trasferimento **VALIDATO**; preflight, runtime-03, Gate, integrazione e
certificazione **BLOCCATO**. Report
`docs/tactical-semantic-support-s2-spatial-v2-extraction-locator-runtime-03-execution-01.md`.

### 2026-11-09 — Materializzazione conforme wrapper runtime-03

Attività: `RD-TSC-V2-D3-S2-SPATIAL-V2-EXTRACTION-LOCATOR-RUNTIME-03`, sola
materializzazione controllata. Verificato il sorgente `runtime-02` di 45.964
byte/SHA-256 `5bcc1826...fcfcaf`; sostituite direttamente sui byte originali le
sole tre occorrenze complete dell'identificativo. Il nuovo artefatto distinto
`runtime-03-approved.sh` misura 45.964 byte, ha SHA-256
`ba0160e0...44d57`, contiene 3 ID `runtime-03` e 0 ID `runtime-02` ed è
identico byte-per-byte alla trasformazione autorizzata, senza LF aggiuntivo.
Il file divergente precedente, 45.965 byte/SHA-256
`ddd74491...c923930`, resta conservato. Materializzazione **ESEGUITO** e
identità **VALIDATO**; 0 wrapper eseguiti, 0 trasporti, 0 generazioni e nessun
trasferimento VPS. Runtime-03, Gate, integrazione e certificazione restano
**BLOCCATO**. Report
`docs/tactical-semantic-support-s2-spatial-v2-extraction-locator-runtime-03-materialization-01.md`.

### 2026-11-09 — Runtime-03 arrestato prima dell'esecuzione

Attività: `RD-TSC-V2-D3-S2-SPATIAL-V2-EXTRACTION-LOCATOR-RUNTIME-03`.
Preflight remoto read-only PASS su staging `db3ad66`, blob, dataset, modello,
lock, dipendenze, artefatti assenti e concorrenza osservabile. Il wrapper
materializzato contiene i tre ID `runtime-03`, ma misura 45.965 byte e ha
SHA-256 `ddd74491...c923930`, contro i 45.964 byte e
`ba0160e0...fd44d57` autorizzati: confronto byte-level identifica un LF `0A`
aggiuntivo in coda. Arresto obbligatorio senza correzione, trasferimento o
esecuzione; 0 chiamate di trasporto e 0 generazioni. Preflight **ESEGUITO**,
prerequisiti osservati **VALIDATO** nel solo snapshot; materializzazione,
runtime, Gate, integrazione e certificazione **BLOCCATO**. Report
`docs/tactical-semantic-support-s2-spatial-v2-extraction-locator-runtime-03.md`.

### 2026-11-09 — Staging Extraction Locator Spatial V2

Attività:
`RD-TSC-V2-D3-S2-SPATIAL-V2-EXTRACTION-LOCATOR-STAGING-PREPARATION-01`.
Creato bundle Git autosufficiente 2.345.406 byte, SHA-256
`d595c23a...a60f08`, con storia completa e nessun prerequisito esterno,
verificato localmente e sulla VPS. Clone indipendente
`staging/spatial-v2-extraction-locator-db3ad66`, detached a `db3ad66`, status
pulito, common dir interno, alternates assenti e `git fsck --full` PASS. Blob
inference/extraction/validator/dataset e SHA-256 Linux dataset conformi.
Checkout operativo e staging precedenti invariati. Bundle e isolamento
**VALIDATO**, clone **IMPLEMENTATO**, verifiche **ESEGUITO**; runtime Extraction
Locator, Gate, integrazione e certificazione **BLOCCATO**. Nessun test
applicativo, Ollama, Qwen o inferenza. Report
`docs/tactical-semantic-support-s2-spatial-v2-extraction-locator-staging-preparation-01.md`.

### 2026-11-08 — Runtime-02 Extraction Locator bloccato per staging assente

Attività: `RD-TSC-V2-D3-S2-SPATIAL-V2-EXTRACTION-LOCATOR-RUNTIME-02`.
Wrapper integrale verificato con SHA-256 `5bcc1826...` ed eseguito una sola
volta. Il controllo lock corretto ha superato il precedente punto di arresto;
il preflight è terminato con `E_PATH_MISSING`, exit wrapper 68, perché lo
staging richiesto `spatial-v2-extraction-locator-db3ad66` è assente. Il parent
staging esiste; nessuna correzione o creazione è stata effettuata. Stato finale
e inventari SHA-256 PASS, `transport_calls=0`, zero generazioni, nessun witness.
Tentativo **ESEGUITO**; integrità wrapper, finalizzazione e fail-closed del
singolo arresto **VALIDATO**; preflight completo, runtime, Gate, integrazione e
certificazione **BLOCCATO**. Nessun retry o terzo tentativo. Report
`docs/tactical-semantic-support-s2-spatial-v2-extraction-locator-runtime-02.md`.

### 2026-11-08 — Runtime Extraction Locator Spatial V2 arrestato nel preflight

Attività: `RD-TSC-V2-D3-S2-SPATIAL-V2-EXTRACTION-LOCATOR-RUNTIME-01`.
Eseguito una sola volta il wrapper approvato per
`spatial-v2-extraction-locator-q3-04-runtime-01`. Il preflight ha creato e
acquisito il lock, verificato poi come file regolare vuoto, ma il confronto
testuale `regular file` ha respinto la descrizione GNU `regular empty file`:
`E_LOCK_FD_NOT_REGULAR`, exit wrapper 62. Arresto precedente a staging,
modello e inferenza; `transport_calls=0`, nessuna generazione e nessun witness.
Finalizzazione completa e inventari SHA-256 verificati. Tentativo **ESEGUITO**;
fail-closed osservato **VALIDATO** nel singolo arresto; preflight completo,
runtime, Gate, integrazione e certificazione **BLOCCATO**. Nessun retry o
secondo tentativo eseguito. Report
`docs/tactical-semantic-support-s2-spatial-v2-extraction-locator-runtime-01.md`.

### 2026-11-07 — Revisione statica extraction locator Spatial V2

Attività: `RD-TSC-V2-D3-S2-SPATIAL-V2-EXTRACTION-LOCATOR-REVIEW-01`. Revisione
statica di schema, trasformazione, match, semantica, fail-closed, provenienza e
legacy sulla baseline `9bd8ee4`, senza ripetere i 12+21 test. Campi semantici
conservati; locator letterale side-bound con conteggio overlap e unico match;
validatore finale blob-invariato. Digest e ricalcolo offrono integrità rispetto
agli input, non autenticità crittografica. Nessun difetto concreto. Limiti
minori: overlap non coperto direttamente e nessun positivo dedicato a ogni
slot esplicito/multi-frammento; codice relativo verificato staticamente.
Revisione **ESEGUITO**, proprietà esaminate **VALIDATO**; singolo runtime
diagnostico opt-in **DA FARE** previa autorizzazione; Gate, integrazione e
certificazione **BLOCCATO**. Report
`docs/tactical-semantic-support-s2-spatial-v2-extraction-locator-review-01.md`.

### 2026-11-07 — Extraction contract e locator Spatial V2 offline

Attività: `RD-TSC-V2-D3-S2-SPATIAL-V2-EXTRACTION-LOCATOR-01`. Implementati
contratto versionato senza source/offset, localizzatore letterale side-bound e
percorso judge strettamente opt-in. Solo un match unico viene materializzato;
zero/multipli, lato opposto, input malformato e provenienza alterata sono
fail-closed. Il locator non modifica status/value, comparison o label e delega
al `validate_spatial_v2()` invariato; `promotion_authorized=false`. Default,
prompt/schema legacy, modello, timeout, token e politica senza retry/repair/
fallback restano invariati. Test nuovi 12/12 PASS; regressione Spatial V2
direttamente interessata 21/21 PASS; zero rete/inferenze. Contratto e locator
**IMPLEMENTATO**, test **ESEGUITO**, proprietà offline **VALIDATO**; efficacia
Qwen, runtime, Gate, integrazione e certificazione **BLOCCATO**. Report
`docs/tactical-semantic-support-s2-spatial-v2-extraction-locator-01.md`.

### 2026-11-07 — Revisione architetturale witness Spatial V2

Attività: `RD-TSC-V2-D3-S2-SPATIAL-V2-WITNESS-ARCHITECTURE-01`. Revisione
statica dei due runtime conclusi, codice Spatial V2, D3/S1/S2, bridge e spalla.
Nel runtime storico 16/16 frammenti e nel post-remediation 13/14 sono esatti e
univoci nel lato imposto; l'ultimo appartiene soltanto al lato opposto. Tutti i
30 offset sono invalidi. Nessun resolver produttivo equivalente è presente;
D3 verifica già `exact_text`, mentre `validate_spatial_v2()` applica il
contratto finale senza mutazioni. La spalla Groq è separata, disattivata e non
calcola offset. Raccomandato un contratto opt-in distinto: Qwen seleziona
frammenti senza offset/source, un locator puro accetta solo match letterali
univoci e il validatore V2 invariato decide fail-closed; status/value e semantica
non vengono corretti. Analisi **ESEGUITO**; evidenze e raccomandazione
**VALIDATO** progettualmente; implementazione/test **DA FARE** previa
autorizzazione; Gate, integrazione e certificazione **BLOCCATO**. Report
`docs/tactical-semantic-support-s2-spatial-v2-witness-architecture-01.md`.

### 2026-11-07 — Runtime post-remediation prompt Spatial V2 q3_04

Attività: `RD-TSC-V2-D3-S2-SPATIAL-V2-Q3-04-PROMPT-RUNTIME-01`. Unica
richiesta autorizzata sullo staging Git indipendente detached a `41d50fa`, con
timeout HTTP 360 s ed esterno 450 s, modello `qwen3.5:9b`, 2.048 token massimi
e zero retry/repair/fallback. Risposta completa in 247,24 s: 462 token prompt,
1.803 token generati in 222,43 s, circa 8,11 token/s. La remediation è rispettata
per i quantificatori (2/2 conformi contro 0/2), ma tutti i 14 anchor restano
invalidi; la polarità `explicit/affirmed` mantiene inoltre
`E_STATUS_VALUE_INCONSISTENT`. Il risultato resta `not_evaluable`, label
derivata nulla e `promotion_authorized=false`. Artefatti 24/24 verificati;
checkout operativo e staging invariati. Tentativo **ESEGUITO**; completamento,
fail-closed e correzione dei quantificatori **VALIDATO** nel singolo caso;
validità complessiva, semantica, promozione, Gate, integrazione e certificazione
**BLOCCATO**. Report
`docs/tactical-semantic-support-s2-spatial-v2-q3-04-prompt-runtime-01.md`.

### 2026-11-07 — Remediation prompt Spatial V2 q3_04

Attività: `RD-TSC-V2-D3-S2-SPATIAL-V2-Q3-04-PROMPT-REMEDIATION-01`.
Modificato esclusivamente `INSTRUCTION` del judge Spatial V2 per trasmettere
offset Unicode code-point zero-based e semiaperti, uguaglianza exact-span,
divieto di stime/normalizzazioni e combinazioni normative complete dei
quantificatori. Un solo test mock nuovo PASS verifica prompt effettivo,
claim/evidence, modello, schema, `num_predict=2048`, timeout 180, singola
chiamata, zero retry/repair/fallback e fail-closed del witness con anchor e
status/value invalidi. Schema, validatore, timeout 360 e semantica invariati;
nessuna rete o inferenza. Correzione **IMPLEMENTATO**, test **ESEGUITO**,
handoff interessato **VALIDATO** offline; nuova generazione **DA FARE**,
efficacia Qwen, semantica, promozione, Gate, integrazione e certificazione
**BLOCCATO**. Report
`docs/tactical-semantic-support-s2-spatial-v2-q3-04-prompt-remediation-01.md`.

### 2026-11-07 — Root cause witness Spatial V2 q3_04

Attività: `RD-TSC-V2-D3-S2-SPATIAL-V2-Q3-04-WITNESS-ROOT-CAUSE-01`.
Revisione statica dei 22 artefatti verificati e del codice eseguito a
`69ec127`: 16/16 anchor hanno span testuale esistente, ma offset errati; nessun
errore NFC, Unicode, punteggiatura, trasformazione input o validatore. Il
quantificatore `status=explicit`, `value=absent`, `anchors=[]` è vietato: per
assenza grammaticale la matrice prescrive `implicit/none/[]`, mentre
`absent/absent/[]` è la sentinella distinta. Specifica completa e validatore
sono allineati, ma prompt runtime e schema inviato al modello non rendono
espliciti tutti i vincoli incrociati. Analisi **ESEGUITO**, cause **VALIDATO**;
unica remediation raccomandata, non implementata, è completare il solo handoff
normativo nel prompt con offset code-point semiaperti ed esempi status/value.
Correzione **DA FARE**; semantica, promozione, Gate, integrazione e
certificazione **BLOCCATO**. Report
`docs/tactical-semantic-support-s2-spatial-v2-q3-04-witness-root-cause-01.md`.

### 2026-11-07 — Singolo runtime Spatial V2 q3_04 con timeout 360 s

Attività: `RD-TSC-V2-D3-S2-SPATIAL-V2-Q3-04-RUNTIME-360-01`. Staging Git
indipendente detached a `69ec127`; modello `qwen3.5:9b`, prompt/schema canonici,
`num_predict=2048`, timeout HTTP 360 s ed esterno 450 s. Un'unica richiesta,
zero retry/repair/fallback, completata in 236,00 s con `done_reason=stop`, 188
token prompt e 1.771 token generati a circa 8,04 token/s. Il modello ha proposto
`supported`, ma il validatore ha restituito `not_evaluable` con
`E_ANCHOR_INVALID` e `E_STATUS_VALUE_INCONSISTENT`: label derivata nulla e
`promotion_authorized=false`. Artefatti 22/22 conformi; checkout operativo e
staging invariati. Tentativo **ESEGUITO**, completamento tecnico e fail-closed
**VALIDATO** nel singolo caso; struttura, semantica, promozione, Gate,
integrazione e certificazione **BLOCCATO**. Report
`docs/tactical-semantic-support-s2-spatial-v2-q3-04-runtime-360-01.md`.

### 2026-11-07 — Timeout diagnostico opt-in 360 s Spatial V2

Attività: `RD-TSC-V2-D3-S2-SPATIAL-V2-Q3-04-TIMEOUT-OPTIN-360-01`.
Nel judge Spatial V2 è stato introdotto il solo selettore keyword esplicito
`q3_04_timeout_360=True`: il default resta 180 s e l'opt-in propaga 360 s al
trasporto HTTP. Modello `qwen3.5:9b`, prompt, schema, `num_predict=2048`, una
chiamata, zero retry/repair/fallback e fail-closed sono invariati. Test mock
differenziali 2/2 PASS: confronto 180/360 con payload identico e timeout opt-in
classificato `not_evaluable`/`E_JUDGE_TIMEOUT`, senza promozione. Nessuna rete o
inferenza. Variante **IMPLEMENTATO**, test **ESEGUITO**, correttezza tecnica
interessata **VALIDATO** offline; runtime 360 s **DA FARE** previa distinta
autorizzazione, semantica, Gate, integrazione e certificazione **BLOCCATO**.
Report
`docs/tactical-semantic-support-s2-spatial-v2-q3-04-timeout-optin-360-01.md`.

### 2026-11-07 — Helper sudo diagnostico controllato

Attività: `RD-FOOTBALL-VPS-SUDO-DIAGNOSTIC-IMPLEMENTATION-01`. Installati
atomicamente helper root-owned senza argomenti e regola sudoers `NOPASSWD`
vincolata al solo comando esatto per la finestra storica Ollama/kernel. Hash,
owner, mode, Bash e `visudo` conformi; manifest delle configurazioni sudo
preesistenti invariato. Test positivo: exit 0, 43.542 byte, 367 righe, due
sezioni e stderr vuoto anche con ambiente/pager manipolati. Argomenti extra e
altro comando sudo exit 1; regola esatta presente, `NOPASSWD: ALL` assente.
Rami timeout/troncamento/incompletezza verificati staticamente, non forzati sui
log reali. Helper/regola **IMPLEMENTATO**, test **ESEGUITO**, minimo privilegio,
integrità, fail-closed e accesso senza password **VALIDATO** nel solo perimetro
fisso. Nessun accesso amministrativo generale o certificazione VPS. Report
`docs/football-vps-sudo-diagnostic-implementation-01.md`.

### 2026-11-07 — Rotazione controllata chiave SSH v2

Attività: `RD-FOOTBALL-VPS-SSH-KEY-ROTATION-PHASE-01`. La nuova identità
Ed25519 v2 creata dal titolare ha superato file type, ACL, reparse point,
fingerprint e verifica interattiva della passphrase. Agent inizialmente vuoto,
poi `Running/Automatic` con la sola fingerprint attesa. Chiave pubblica aggiunta
atomicamente ad `authorized_keys` con backup protetto e vecchie entry preservate.
Singola connessione differenziale: exit 0, fingerprint v2 offerta dall'agent,
accettata dal server, autenticazione `publickey`, password/fallback disabilitati.
Alias aggiornato alla v2 con backup locale; vecchio accesso preservato. Fase SSH
**VALIDATO**; installazione/alias **ESEGUITO**; revoca vecchia identità **DA
FARE** separatamente. Lo stato `helper e sudoers BLOCCATO` apparteneva a questo
momento storico ed è stato successivamente superato da
`RD-FOOTBALL-VPS-SUDO-DIAGNOSTIC-IMPLEMENTATION-01`: helper e regola
**IMPLEMENTATO**, verifiche **ESEGUITO**, accesso senza password al solo helper
**VALIDATO**. Diagnostica generale resta **BLOCCATO**; nessun privilegio
amministrativo generale è concesso. Report
`docs/football-vps-ssh-key-rotation-phase-01.md`.

### 2026-11-07 — Fase 1 verifica chiave SSH e agent

Attività: `RD-FOOTBALL-VPS-SSH-AGENT-PHASE-01`. Metadati, ACL, reparse point,
alias e tipo pubblico Ed25519 conformi. Nella ripresa autorizzata l'agent vuoto
è stato temporaneamente abilitato e ha caricato la sola fingerprint attesa, ma
il caricamento non ha dimostrato una passphrase protettiva. Arresto prima della
SSH differenziale; rollback riuscito con rimozione della sola chiave e servizio
nuovamente `Stopped/Disabled`. Nessuna modifica VPS o credenziale acquisita.
Metadati/ACL/tipo **VALIDATO** nel solo perimetro, compatibilità tecnica agent
**ESEGUITO** nel tentativo rollbackato; cifratura, attivazione persistente e
autenticazione via agent **BLOCCATO**. Report
`docs/football-vps-ssh-agent-phase-01.md`.

### 2026-11-07 — Remediation piano SSH/sudo

Attività: `RD-FOOTBALL-VPS-SSH-SUDO-SECURE-ACCESS-REMEDIATION-01`. Recepiti C1–C5:
sudoers vincolato all'helper senza argomenti, contratto root-owned fisso per i
log storici, verifica separata di tipo/cifratura/ACL della chiave, distinzione
agent/disco/publickey/password e controlli completi su ACL, symlink, antenate e
dipendenze. Progettata matrice di 20 test, non eseguiti. Remediation documentale
**ESEGUITO**; verifica chiave, agent, helper e sudoers **DA FARE**; accesso
amministrativo persistente **BLOCCATO**. Nessuna configurazione Windows/VPS
modificata. Report `docs/football-vps-ssh-sudo-secure-access-plan.md`.

### 2026-11-07 — Piano accesso SSH persistente e sudo sicuro

Attività: `RD-FOOTBALL-VPS-SSH-SUDO-SECURE-ACCESS-PLAN-01`. Verificati in sola
lettura OpenSSH, alias `football-vps`, identità dedicata, accesso VPS,
`authorized_keys` e sudo senza acquisire segreti. Windows `ssh-agent` è
fermo/disabilitato; Credential Manager non è un backend diretto per OpenSSH o
sudo. Raccomandati chiave Ed25519 cifrata nell'agent e helper diagnostico
root-owned, autorizzato da sudoers soltanto col comando esatto. Piano
**ESEGUITO**, accesso SSH osservato **VALIDATO**; agent, helper e sudoers
**DA FARE**, accesso amministrativo persistente **BLOCCATO** fino ad
approvazione distinta. Report `docs/football-vps-ssh-sudo-secure-access-plan.md`.

### 2026-11-07 — Recupero amministrativo log Spatial V2

Attività: `RD-TSC-V2-D3-S2-Q3-04-ADMIN-LOG-EXPORT-01`.
Autorizzazione esplicita successiva del titolare: export read-only Ollama/kernel
acquisiti nella finestra 12:19:00–12:25:30 CET e verificati SHA-256. Log: modello
caricato in 8,80 s, prompt 184 token in 6,13 s, generazione regolare a ~8,13
token/s fino a 1.325 token; al timeout client di 180 s POST 500 e cancellazione
task a 1.529 token totali. Nessun OOM o stallo. Export **ESEGUITO**, integrità,
causa operativa e fail-closed **VALIDATO**; semantica, accuratezza, Gate,
integrazione e certificazione **BLOCCATO**. Report
`docs/tactical-semantic-support-s2-spatial-v2-q3-04-admin-log-export-01.md`.

### 2026-11-07 — Tentativo review privilegiata log Spatial V2

Attività: `RD-TSC-V2-D3-S2-SPATIAL-V2-Q3-04-PRIVILEGED-LOG-REVIEW-01`.
Fuso `Europe/Rome` e finestra tassativa 12:19:00–12:25:30 CET confermati. Query
ordinarie senza entry visibili; `sudo -n journalctl` non disponibile (exit 1,
password richiesta). Nessuna password o escalation alternativa usata. La unità
Ollama invia stdout al journal e non dichiara file log dedicati. Nessuna nuova
evidenza server/kernel acquisita e matrice causale invariata. Review log
**BLOCCATO**; fail-closed **VALIDATO**; semantica, accuratezza, Gate,
integrazione e certificazione **BLOCCATO**. Report
`docs/tactical-semantic-support-s2-spatial-v2-q3-04-privileged-log-review-01.md`.

### 2026-11-07 — Forensic timeout Spatial V2 q3_04

Attività: `RD-TSC-V2-D3-S2-SPATIAL-V2-Q3-04-TIMEOUT-FORENSIC-01`.
Verifica read-only: SHA-256 inventario conforme e 12/12 artefatti verificati;
timeline 12:20:38–12:23:38 ricostruita. Timeout client a 180,124 s dimostrato,
una chiamata, zero retry/repair/fallback e non-promozione corretta. Modello
assente prima e caricato durante: caricamento e lentezza generativa compatibili,
non dimostrati come causa. Log completi Ollama non visibili all'utente SSH;
telemetria interna assente. Revisione **ESEGUITO**, integrità e fail-closed
**VALIDATO**; semantica, accuratezza, Gate, integrazione e certificazione
**BLOCCATO**. Report
`docs/tactical-semantic-support-s2-spatial-v2-q3-04-timeout-forensic-01.md`.

### 2026-11-07 — Singola diagnosi runtime Spatial V2 q3_04

Attività: `RD-TSC-V2-D3-S2-SPATIAL-V2-Q3-04-RUNTIME-RUN-01`.
Preflight conforme sullo staging detached `009f76e`; avviata esattamente una
richiesta `qwen3.5:9b`, zero retry/repair/fallback. Dopo 180,124 s il judge ha
restituito `not_evaluable` con `E_JUDGE_TIMEOUT`, nessuna promozione, witness o
label. Prompt, payload, risultato e metadati sono preservati esternamente con
inventario SHA-256; nessuna risposta HTTP grezza è stata ricevuta. Tentativo
**ESEGUITO**, fail-closed **VALIDATO** nel singolo caso; diagnosi semantica,
accuratezza, Gate, integrazione e certificazione **BLOCCATO**; revisione
indipendente **DA FARE**. Report
`docs/tactical-semantic-support-s2-spatial-v2-q3-04-runtime-run-01.md`.

### 2026-11-07 — Staging isolato Spatial V2 q3_04

Attività: `RD-TSC-V2-D3-S2-SPATIAL-V2-STAGING-PREPARATION-01`.
Clone Git autonomo creato via GitHub HTTPS nel parent VPS autorizzato, detached
HEAD esatto `009f76e`, working tree pulito e `git fsck` PASS. Moduli Spatial V2,
schema, test e dataset canonico presenti; blob e materializzazione Linux del
dataset coincidono. Import non generativo PASS con Python 3.12.3; Ollama espone
`qwen3.5:9b`, nessun modello caricato o Gate concorrente nello snapshot. Zero
inferenze. Staging **IMPLEMENTATO**, verifiche **ESEGUITO**, isolamento e
integrità **VALIDATO**; diagnosi runtime, efficacia, Gate, integrazione e
certificazione **BLOCCATO**. Report
`docs/tactical-semantic-support-s2-spatial-v2-staging-preparation-01.md`.

### 2026-11-07 — Preflight diagnosi runtime Spatial V2 q3_04

Attività: `RD-TSC-V2-D3-S2-SPATIAL-V2-Q3-04-RUNTIME-DIAGNOSTIC-01`.
Baseline `009f76e`. Dataset/claim/evidence canonici verificati tramite SHA-256.
Il PC non espone Ollama; la VPS espone `qwen3.5:9b` e nello snapshot non mostra
modelli caricati o Gate concorrenti, ma i quattro staging presenti appartengono
a baseline storiche e nessuno contiene `009f76e`. Nessun trasferimento, clone o
riuso del checkout operativo era autorizzato. Decisione: arresto pre-inferenza,
zero chiamate/generazioni, nessun artefatto runtime. Report
`docs/tactical-semantic-support-s2-spatial-v2-q3-04-runtime-diagnostic-01.md`.
Stato: preflight **ESEGUITO**; diagnosi q3_04, efficacia, Gate, integrazione e
certificazione **BLOCCATO**. Prossimo passo eventuale: distinta autorizzazione
per staging isolato alla baseline, senza inferenza automatica.

### 2026-11-07 — Closeout revisione indipendente Spatial V2 R1/R2

Attività: `RD-TSC-V2-D3-S2-SPATIAL-V2-OFFLINE-REMEDIATION-REVIEW-01`.
Baseline `3c935b0`. La revisione indipendente statica ha confermato nel percorso
esaminato la restrizione normativa di `incompatible`, la precedenza delle
sentinelle e gli envelope fail-closed del judge con una chiamata e zero
retry/repair/fallback. Esaminati codice, test e report su GitHub; i 18 test non
sono stati rieseguiti dal revisore e non si registra una seconda esecuzione.
Nessuno script tecnico creato o eseguito in questo closeout. Report
`docs/tactical-semantic-support-s2-spatial-v2-offline-remediation-review-01.md`.
Decisione: remediation R1/R2 e proprietà nel percorso esaminato **VALIDATO**;
validazione complessiva, accuratezza, q3_04 runtime, Gate, integrazione e
certificazione **BLOCCATO**. Closeout documentale concluso.

### 2026-11-07 — Remediation offline Spatial V2 R1/R2

Attività: `RD-TSC-V2-D3-S2-SPATIAL-V2-OFFLINE-REMEDIATION-01`. Baseline
`128f014`. R1 restringe `incompatible` alle sole coppie di
`INCOMPATIBLE_VALUES`, con sentinelle e assi diversi conservativi. R2 converte
gli errori operativi previsti del judge in envelope `not_evaluable` con codici
distinti, una sola chiamata e nessun retry/repair/fallback; errori di
programmazione restano eccezioni. Primo run aggiornato 16/18 PASS: la correzione
R1 sovrascriveva due sentinelle; dopo rettifica, finale 18/18 PASS, exit 0.
Nessuna inferenza o rete. Report
`docs/tactical-semantic-support-s2-spatial-v2-offline-remediation-01.md`.
Decisione: remediation **IMPLEMENTATO**, test **ESEGUITO**, revisione
indipendente **DA FARE**; validazione complessiva, efficacia, Gate, integrazione
e certificazione **BLOCCATO**.

### 2026-11-07 — Implementazione offline isolata Spatial V2

Attività: `RD-TSC-V2-D3-S2-SPATIAL-V2-OFFLINE-IMPLEMENTATION-01`. Baseline
`4e8eabb`. Implementati in moduli nuovi schema/vocabolario
`nli_spatial_relations_v2` 2.0.0, validatore deterministico puro e judge opt-in
inerte, con una chiamata, zero retry/repair/fallback e
`promotion_authorized=false`. Il primo run nuovo ha prodotto 6 PASS/10 FAIL per
un errore nell'ordine del comparison conditions; corretto, il run finale è
16/16 PASS. Nessuna inferenza, rete, Gate o suite storica. Legacy interessato
invariato. La revisione indipendente R1–R5 è registrata **VALIDATO** solo nel
perimetro documentale. Report
`docs/tactical-semantic-support-s2-spatial-v2-offline-implementation-01.md`.
Decisione: PASS tecnico offline; sottoporre codice/test/report a revisione
indipendente. Stato: implementazione **IMPLEMENTATO**, test **ESEGUITO**,
proprietà coperte **VALIDATO** offline; efficacia, Gate, integrazione e
certificazione **BLOCCATO**.

### 2026-11-07 — Remediation specifica Spatial V2 R1–R5

Attività: `RD-TSC-V2-D3-S2-SPATIAL-V2-SPEC-REMEDIATION-01`. Baseline
`31007f2`. Corrette esclusivamente le ambiguità documentali: associazioni
axis/value normative nello schema (incluso `area_extent/stable`), precedenza
totale fra invalidità e insufficienza, scelta A per `compatible` come asserzione
shadow non verificata, matrice completa status/value/anchor e semantica chiusa
dei quantificatori. Verificata la rappresentabilità di `q3_04`, non la sua
risoluzione. Nessun test, inferenza o runtime eseguito; architettura invariata.
Report `docs/tactical-semantic-support-s2-spatial-v2-spec-remediation-01.md`.
Decisione: sottoporre la specifica corretta a revisione indipendente prima di
ogni implementazione. Stato: remediation **ESEGUITO**; review e implementazione
**DA FARE**; efficacia, Gate, integrazione e certificazione **BLOCCATO**;
provenance Spatial V1 **VALIDATO**.

### 2026-11-07 — Specifica tecnica offline Spatial V2

Attività: `RD-TSC-V2-D3-S2-SPATIAL-V2-SPEC-01`. Sulla baseline `16c6daf` è
stato specificato il contratto opt-in `nli_spatial_relations_v2` 2.0.0:
relation witness strutturato, schema Draft 2020-12, vocabolario relazionale,
ancore testuali exact-span con offset code point, comparabilità, derivazione
deterministica delle tre label e codici fail-closed. Il validatore futuro potrà
dimostrare forma, ancoraggio e coerenza interna, non la correttezza semantica
delle categorie scelte dallo stesso modello. Una sola generazione, zero
retry/repair/fallback, shadow e `promotion_authorized=false`; V1, NLI V2, S1,
S2, retrieval, API e panel invariati. Nessuno script di test o runtime è stato
eseguito. Report
`docs/tactical-semantic-support-s2-spatial-v2-spec-01.md`. Decisione: sottoporre
la specifica a revisione indipendente prima di qualsiasi implementazione.
Stato: specifica **ESEGUITO**; implementazione **DA FARE**; efficacia, Gate,
integrazione e certificazione **BLOCCATO**; provenance Spatial V1 **VALIDATO**.

### 2026-10-27 — Fix pannello: rimozione `--tactical-plan` dal profilo default

Attività: diagnosticare e risolvere il blocco totale del pannello pubblico sulla VPS.
Script: `scripts/run_rag_v5_query.py`; commit: `7c018f9` su `codex/rag-coverciano-remediation`.
Risultato: il branch aveva introdotto `--tactical-plan` nel profilo default del runner
del pannello, attivando il quality gate di `audit_answer` (`v5_tactical_query_plan_v1.py`)
su tutte le domande. Il gate richiedeva `complete=True` (zero `missing_facets`,
`missing_operational <= 1`, zero `missing_details`, zero `semantic_issues`); le risposte
RAG generiche fallivano su `unsupported_rigid_player_numbers` e altri criteri Coverciano.
Tutti i job restituivano `INCOMPLETE: tactical_quality_gate_failed`. Rimossa la riga
`--tactical-plan` dalla lista argv del profilo default; gate e audit preservati per gli
script Coverciano. Deploy: git pull VPS + restart `football-rag-api`; pannello ripristinato.
Decisione: `--tactical-plan` rimane fuori dal profilo default del pannello finché non
validato su domande generiche. Stato: **VALIDATO e INTEGRATO**.

### 2026-10-27 — Chiusura differenziale V10.1/V10.2

Attività: rerun esclusivo dei casi 5, 6, 8 e 10 dopo gli errori V10. Risultato:
5/6/8 PASS; caso 10 rigenerato una seconda volta con geometria coerente e senza
numeri inventati. Il FAIL residuo dipendeva solo dall'audit, che riconosceva
`comando/segnale` ma non `comandi/segnali`; re-audit dopo correzione PASS.
Nessuna nuova inferenza per gli altri casi. Decisione: set logico finale 10/10
VALIDATO tecnicamente; aprire il cancello esterno con almeno dieci domande
inedite Gemini, risposta RAG invariata, spalla disabilitata e soglia media
>=28/30. Stato: V10.1/V10.2 **ESEGUITA e VALIDATA tecnicamente**; voto esterno
**DA FARE**.

### 2026-10-27 — Terzo giro V10 e correzione mirata V10.1

Attività: terzo rerun RAG-only 10/10 con gate di contaminazione rafforzato;
report `docs/rag-coverciano-remediation-v10-runtime-01.md`, risultati
`evaluation/coverciano-remediation-v10/`. Risultato: indice 6.410 invariato,
zero troncamenti/citazioni invalide, media 224,95 s, gate PASS 8/10. Casi 5 e 6
respinti; audit umano ha inoltre respinto i falsi PASS 8 (numeri inventati) e 10
(ruoli incoerenti). Decisione: V10 non VALIDATA; V10.1 ripete esclusivamente i
quattro casi interessati dopo sanificazione sottrattiva e nuovi gate. Stato:
V10 **ESEGUITA, NON VALIDATA**; V10.1 **IMPLEMENTATA**, validazione/runtime
**DA FARE**.

### 2026-10-27 — Preparazione terzo giro V10

Attività: audit manuale-applicativo dei dieci testi V9 prima di ripetere il test.
Evidenze: contaminazione da cross nel caso 2; numeri non richiesti nei casi 4 e
8; scivolamento descritto come arretramento e compiti quinto/mediano confusi nel
caso 5; etichetta interna nel caso 6; ruolo del limite area invertito nel caso
8; trasformazione con tre sostituzioni generiche nel caso 10. Script:
`v5_tactical_query_plan_v1.py`, `smoke_test_rag_v5_e2e.py`; test planner.
Decisione: introdurre questi gate e istruzioni correttive come differenza
tecnica V10, quindi rieseguire lo stesso set senza spalla. Stato:
**IMPLEMENTATO**; validazione offline e runtime **DA FARE**.

### 2026-10-27 — Runtime V9 e chiusura tecnica del set congelato

Attività: terzo rerun differenziale RAG-only delle dieci domande congelate;
report `docs/rag-coverciano-remediation-v9-runtime-01.md`, risultati
`evaluation/coverciano-remediation-v9/`. Risultato: 10/10 file, indice 6.410
invariato, zero citazioni invalide, zero troncamenti, media 215,72 s; gate 9/10.
Il solo FAIL era un falso positivo: una clausola associava correttamente palla
scoperta ad arretramento e descriveva una risalita solo successiva. V9.1 rende
l'audit sensibile alla sequenza; re-audit degli output conservati 10/10, senza
nuova inferenza. Confronto con i rilievi Gemini congelati: omissioni note ora
coperte, ma nessun nuovo voto esterno richiesto. Decisione: chiudere la
remediation tecnica del set; non dichiarare il target medio >=26/30 finché non
viene valutato esternamente il testo RAG invariato. Stato: V9 **ESEGUITA e
VALIDATA tecnicamente**; voto esterno **DA VALIDARE**.

### 2026-10-27 — Runtime V8 e correzione differenziale V9

Attività: rieseguire i dieci casi congelati con gate relazionale fail-closed,
contesto 8.192 e spalla disabilitata. Report
`docs/rag-coverciano-remediation-v8-runtime-01.md`; risultati
`evaluation/coverciano-remediation-v8/`. Risultato: 10/10, indice 6.410
invariato, zero citazioni invalide, zero troncamenti, media 254,05 s; gate PASS
3/10. Errori reali nei casi 7-10 e falsi negativi di audit nei casi 3, 4 e 6.
Decisione: V8 non VALIDATA; implementare V9 con attivazione contestuale dei
requisiti, match relazionale, divieto numeri non richiesti e repair in linguaggio
tattico naturale, quindi ripetere lo stesso set. Stato: V8 **ESEGUITA, NON
VALIDATA**; V9 **IMPLEMENTATA**, validazione offline e runtime **DA FARE**.

### 2026-10-27 — Remediation V8 gate relazionale e selezione repair

Attività: correggere le tre cause residue dimostrate dal runtime V7 senza
spalla e senza modificare la pipeline locked. Script:
`v5_tactical_query_plan_v1.py`, `smoke_test_rag_v5_e2e.py`,
`run_rag_v5_query.py`; test planner/API/catalogo. Implementazione: rilevamento
di associazioni tattiche contraddittorie e contaminazioni di fase, divieto di
esporre etichette interne o numeri rigidi non richiesti, confronto deterministico
fra prima risposta e repair, selezione del candidato con minori omissioni,
telemetria `quality_gate_*` e rifiuto fail-closed del wrapper se il candidato
finale non supera il gate. Risultato offline: 43/43 test, compilazione e diff
check PASS. Decisione: distribuire sul ramo dedicato e ripetere da zero le dieci
domande con contesto 8.192 per evitare troncamenti; continuare l'affinamento
dopo il confronto. Stato: **IMPLEMENTATO e VALIDATO offline**; runtime **DA
FARE**.

### 2026-10-27 — Runtime Coverciano remediation V7

Attività: secondo rerun differenziale 10/10 con ancoraggi documentali esatti,
audit scenario-specifico e singolo repair automatico; spalla disabilitata e
nessuna chiamata Gemini. Script: `v5_tactical_query_plan_v1.py`,
`smoke_test_rag_v5_e2e.py`; report
`docs/rag-coverciano-remediation-v7-runtime-01.md`; risultati
`evaluation/coverciano-remediation-v7/`. Risultato: indice 6.410 invariato,
zero citazioni invalide, media 227,45 s (-22,6% su V6), repair 6/10, due
troncamenti e solo tre risposte realmente complete; il caso 9 supera
erroneamente il gate pur contenendo una contraddizione palla coperta/scoperta.
Decisione: target 26/30 non dimostrato; non validare. Rafforzare audit
relazionale e fail-closed post-repair prima di altri benchmark. Stato:
**ESEGUITO, NON VALIDATO**.

### 2026-10-27 — Runtime V6 e correzione gate semantico V7

Attività: eseguire il rerun differenziale dei dieci casi Coverciano congelati e
confrontarlo con i rilievi Gemini storici, senza spalla né nuove chiamate
esterne. Script: `v5_tactical_query_plan_v1.py`,
`smoke_test_rag_v5_e2e.py`; report
`docs/rag-coverciano-remediation-v6-runtime-01.md`; risultati
`evaluation/coverciano-remediation-v6/`. Risultato V6: 10/10, indice 6.410
invariato, zero citazioni invalide, tempo medio 293,95 s; quattro audit
incompleti, due troncamenti e errori semantici residui nei casi 5, 6, 9 e 10.
Decisione: V6 non VALIDATA e target 26/30 non dimostrato. Correzione V7:
scenari generici, query prioritarie, vincoli decisionali, audit relazionale e
singola rigenerazione su omissione/troncamento. Stato: V6 **ESEGUITA, NON
VALIDATA**. Primo gate retrieval-only 4/4: ha rilevato che passaggi esatti gia
presenti nel corpus non entravano nel contesto; aggiunta espansione bounded per
frasi esatte con massimo tre riserve sottoposte al reranker. Suite aggiornata
39/39. V7 **IMPLEMENTATA e VALIDATA offline**; nuovo gate retrieval e runtime
**DA FARE**.

### 2026-10-26 — Remediation autonoma RAG sui dieci casi Coverciano

Attività: analizzare la baseline 199/300 e correggere il RAG senza riattivare
OpenRouter né ripetere chiamate Gemini. Script:
`scripts/v5_tactical_query_plan_v1.py`, integrazione opt-in applicativa in
`smoke_test_rag_v5_e2e.py` e default del solo wrapper
`run_rag_v5_query.py`; test `test_v5_tactical_query_plan_v1.py`. Report:
`docs/rag-coverciano-remediation-01.md`. Risultato: parser e piano dei
sottoproblemi, retrieval multi-query, penalità fase opposta, riserva multi-facet,
contratto applicativo e audit post-risposta implementati; test planner/router
11/11, API 19/19, catalogo 7/7, compilazione e diff check PASS. Decisione:
preservare il default locked, distribuire sul ramo dedicato e svolgere un solo
rerun differenziale dei dieci casi congelati; 26/30 resta soglia minima e non è
ancora dimostrata. Stato: **IMPLEMENTATO e VALIDATO offline**; runtime **DA
FARE**, benchmark non VALIDATO.

### 2026-10-26 — Reset benchmark Coverciano RAG-only 100

Attivita: sostituire il benchmark inficiato dalla riscrittura OpenRouter con un
nuovo percorso che valuta esclusivamente il RAG autonomo. Script: API e pannello
in modalità spalla disabilitata; protocollo
`docs/coverciano-rag-only-100-protocol-01.md`. Risultato iniziale: requisito
congelato; casi precedenti esclusi dalla nuova media; OpenRouter conservato nel
codice ma flag runtime impostato a zero. Decisione: Gemini Cloud genera e valuta,
il pannello esegue soltanto RAG; target medio >=26/30; continuare fino al caso
100 e poi arrestarsi con report completo. Stato: requisiti **IMPLEMENTATI**;
test/deploy **DA FARE**; benchmark **DA FARE**.

### 2026-10-26 — Migrazione revisore applicativo a OpenRouter

Attività: sostituire nel percorso applicativo i collegamenti diretti Gemini e
Groq con un unico trasporto OpenRouter, preservando integralmente storico e
pipeline RAG certificata. Script: `scripts/openrouter_tactical_copilot_v1.py`,
API e pannello; report `docs/openrouter-reviewer-migration-01.md`. Risultato:
adapter a due passaggi con fallback ordinato, structured output e validazione
fail-closed; configurazione, worker e UI non invocano più i provider diretti.
Suite API/adapter 22/22, compilazione Python e sintassi JavaScript PASS; zero
chiamate esterne. Decisione: mantenere gli artefatti storici per audit e
installare la nuova chiave solo nel file privato VPS. Stato: **IMPLEMENTATO**;
deploy e singola verifica pubblica **DA FARE**.

### 2026-10-26 — Prima prova pubblica OpenRouter e cardinalità PASS1

Attività: eseguire dal pannello il caso storico 4-3-3 contro 5-4-1 per
confrontabilità. Job `7cb0da28`; report
`docs/openrouter-reviewer-migration-01.md`. Risultato: RAG 128,2 s, totale
187 s, 555 token e quattro evidenze; OpenRouter raggiunto con modello riportato
`openai/gpt-oss-120b`, output bloccato da `PASS1_CASE_COUNT_MISMATCH` dopo
circa 34 s. Decisione: imporre nello schema per-request esattamente un elemento
per caso in `reviews` e `revised_answers`, senza allentare i gate semantici.
Suite 23/23, compilazione PASS, nessuna API nella correzione. Stato: prova
**ESEGUITA**, correzione **IMPLEMENTATA e VALIDATA offline**, runtime **DA FARE**.

### 2026-10-26 — OpenRouter GPT-4o completo, costo e giudizio esterno

Attività: sostituire il primario lento `gpt-oss-120b` con `openai/gpt-4o` dopo
il timeout differenziale del job `111f3235`, quindi completare dal pannello lo
stesso caso e sottoporre la risposta finale alla conversazione Gemini
esaminatrice. Job `efb84ad8`; report
`docs/openrouter-reviewer-migration-01.md`. Risultato: RAG 127,6 s, OpenRouter
21,6 s, totale 171 s; structured output e due passaggi verificati. Uso: 3.087
token input, 1.256 output, 4.343 totali; costo $0,0202775. Revisore 5/10;
Gemini esterno 18/30 con errori di ruoli, geometria, preventiva e uso dei cambi.
Decisione: mantenere GPT-4o primario per l'interattività, non validare la
qualità e tracciare nel pannello costo/token/modello per ogni caso. Stato:
flusso **ESEGUITO**, trasporto **VALIDATO**, qualità tattica **DA FARE**;
telemetria costo **IMPLEMENTATA**.

### 2026-10-26 — Remediation tattica successiva al 18/30

Attività: correggere le cause strutturali della risposta finale incompleta senza
allentare la verifica documentale. Script: contratto condiviso copilot, adapter
OpenRouter, API e pannello; report `docs/openrouter-reviewer-migration-01.md`.
Risultato: PASS2 riceve ora domanda e bozza integrali; prompt vincolato a ruoli,
lati e uso dei cambi; introdotto `GIUDIZIO_TECNICO` esclusivamente per finding
con `needs_document_check=false`, senza evidence labels e con downgrade
fail-closed in caso di abuso. Aggiunta telemetria di costo/token al pannello.
Suite 40/40 e compilazione PASS, zero API. Decisione: nuova prova differenziale
dal pannello e iterazione fino a voto esterno >=28/30. Stato: **IMPLEMENTATO e
VALIDATO offline**, runtime **DA FARE**.

### 2026-10-26 — Benchmark live Coverciano caso 001 e gate PASS2

Attività: avviare il protocollo Gemini-esaminatore → pannello RAG/Groq →
Gemini-valutatore sul caso già valutato in precedenza. Job `7c9d0148`; report
`docs/coverciano-100-live-benchmark-01.md`. Risultato: RAG 159,82 s/510 token,
totale 193 s, sei evidenze; Groq concluso ma respinto con
`GROQ_PASS2_UNKNOWN_OR_DUPLICATE_FINDING`. Gemini Cloud ha valutato la bozza
18/30 e rilevato l'errata attribuzione del terzino ammonito. Implementato schema
PASS2 dinamico con enum sugli ID reali; tutti i gate locali restano fail-closed.
Test copilot 12/12 e suite Groq 22/22, zero API. Decisione: preservare il caso
come fallimento di pipeline, non eseguire casi equivalenti finché la correzione
non è distribuita, poi riprendere dalla domanda 2 già acquisita. Stato: caso
**ESEGUITO**, correzione **IMPLEMENTATA e VALIDATA offline**, runtime **DA FARE**.

### 2026-10-26 — Benchmark live Coverciano caso 002 e coerenza evidenze PASS2

Attività: smoke runtime della correzione ID con la domanda 2 prodotta da Gemini.
Job `768b7980`; report `docs/coverciano-100-live-benchmark-01.md`. Risultato:
RAG 173,42 s, totale 206 s, quattro evidenze; il precedente errore ID è risolto,
ma PASS2 è bloccato da `UNSUPPORTED_WITH_EVIDENCE`. Decisione: rimuovere
meccanicamente le etichette dai finding non supportati e degradare a
`ULTERIORE_RETRIEVAL` i finding dichiarati supportati senza alcuna etichetta
valida. Nessuna promozione o modifica tattica. Il tentativo successivo con enum
dinamici è stato respinto dal provider con HTTP 400 schema ed è escluso dal
benchmark; su richiesta del titolare ogni ulteriore prova reale avverrà soltanto
dal pannello. Ripristinato lo schema statico e aggiunta riconciliazione
posizionale solo con cardinalità univoca, oltre alla normalizzazione fail-closed
delle etichette. Test copilot 16/16 e suite Groq 26/26. Stato: caso
**ESEGUITO**; correzione **IMPLEMENTATA e VALIDATA offline**; deploy e runtime
da pannello **DA FARE**.

### 2026-10-26 — Verifica pannello schema PASS2 versionato

Attività: validare dal solo pannello la correzione sul caso 002. Job
`a368e4de`; report `docs/coverciano-100-live-benchmark-01.md`. Risultato: RAG
171,63 s, totale 205 s, Groq respinto con `GROQ_HTTP_400_SCHEMA`; nessun voto
Gemini. Decisione: non riutilizzare il nome provider-side impiegato dal tentativo
dinamico; assegnare al contratto statico il nome immutabile
`groq_tactical_copilot_pass2_static_v2`. Stato: verifica **ESEGUITA**, correzione
**IMPLEMENTATA**, validazione offline e runtime **DA FARE**.

### 2026-10-26 — Normalizzazione token pannello pubblico

Attività: diagnosticare `unauthorized` senza ruotare o divulgare credenziali.
Script: `api/knowledge_panel.html`; test: `tests/test_rag_v5_api.py`; report:
`docs/knowledge-panel-application-integration-02.md`. Risultato: token corrente
verificato con HTTP 200 locale e pubblico; individuato il limite UX sul formato
incollato; aggiunta normalizzazione di assegnazione/virgolette/spazi e guardia sui
valori troppo corti. Suite 18/18 e sintassi JavaScript PASS. Decisione: preservare
il segreto corrente e non memorizzarlo lato browser. Commit `12c7fe0`, deploy VPS
fast-forward, servizio attivo, suite VPS 18/18 e smoke HTTPS autenticato HTTP 200.
Stato: **VALIDATO e INTEGRATO**.

### 2026-10-26 — Recupero job e cronologia pannello

Attività: correggere la perdita apparente del job `259b7f4b...` dopo restart.
Script: `api/rag_v5_api.py`, `api/knowledge_panel.html`; test API; report
`docs/panel-job-recovery-01.md`. Risultato: evidenza RAG esistente sul disco ma
stato/cronologia solo in memoria. Implementata ricostruzione autenticata dei job
completati, lista recente e chiusura grafica dei job realmente interrotti. Suite
30/30, compilazione e JavaScript PASS, nessuna inferenza. Decisione: non riavviare
durante job attivi e rendere il risultato persistente indipendente dal processo.
Deploy commit `1d408ec` dopo controllo coda/processi: suite VPS 30/30, servizio
attivo, endpoint recente locale/pubblico 200 con 20 job e job `259b7f4b...`
ricostruito con risultato. Stato: **VALIDATO e INTEGRATO**.

### 2026-10-26 — Remediation offline HTTP 400 Groq copilot

Attività: diagnosticare il 400 della seconda smoke senza nuova chiamata API.
Script: `scripts/groq_tactical_copilot_v2.py`; test copilot, reviewer e API;
report `docs/groq-copilot-http400-remediation-01.md`. Risultato: documentazione
ufficiale conferma modello e strict schema; payload reso minimale con temperatura
0,1 e diagnostica redatta per categorie 400. Suite 33/33, compilazione PASS,
API_REQUESTS=0. Decisione: non introdurre fallback permissivi o retry; richiedere
una sola smoke differenziale sul caso congelato. Stato: **VALIDATO offline**,
runtime **DA FARE**.
Deploy del commit `301d3dd` sulla VPS: suite 33/33, compilazione PASS, servizio
attivo, checkout pulito e nessuna chiamata Groq. Stato applicativo:
**IMPLEMENTATO** e **VALIDATO offline**; runtime **DA FARE**.

### 2026-10-26 — Prova utente Groq e normalizzazione contratto

Attività: analizzare il test lanciato dal titolare senza ripeterlo. Job
`a5b991d0561548c09d82a1a75da0ccce`; script copilot V2 e test omonimi; report
`docs/groq-copilot-http400-remediation-01.md`. Risultato: RAG 168 s, Groq 8 s,
Gemini legacy 8 s/503, totale 184 s; Groq non restituisce piu HTTP 400 ma il
validatore aggregava tutti gli errori locali in `INVALID_STRUCTURED_RESPONSE`.
Implementata normalizzazione deterministica dei soli ID e del verdetto derivato
dal voto; contenuto tattico intatto; codici PASS1/PASS2 redatti. Suite 34/34,
API_REQUESTS=0 nella correzione. Decisione: disattivare reviewer Gemini API
legacy e attendere una sola verifica utente prima di VALIDARE runtime. Stato:
**IMPLEMENTATO e VALIDATO offline**.

### 2026-10-26 — Smoke isolata Groq job a5b991d0

Attività: rieseguire soltanto il copilot sul risultato RAG esistente dopo
autorizzazione esplicita; quattro estratti, nessun PDF/credenziale e nessun nuovo
RAG. Script: copilot V2; output temporaneo redatto; report
`docs/groq-copilot-http400-remediation-01.md`. Risultato: passaggio 1 accettato,
passaggio 2 BLOCCATO in 6,697 s con `GROQ_PASS2_FINDING_COVERAGE`. Decisione:
non inventare check mancanti; classificarli localmente come
`ULTERIORE_RETRIEVAL`, rimuoverli dagli applicati e conservarli irrisolti.
Extra/duplicati restano errori. Suite 35/35, nessuna API successiva. Stato:
smoke **ESEGUITA**, correzione **IMPLEMENTATA e VALIDATA offline**, runtime
finale **DA FARE** previa nuova autorizzazione.

## Sintesi corrente per il revisore

La fotografia consolidata, con evidenze e limiti, è
`docs/current-status-summary-01.md`. In breve:

| Ambito | Stato corrente | Riferimento |
|---|---|---|
| Manifest locked, runtime congelato e wrapper CLI | **CERTIFICATO** | `docs/v5-certification-closeout-01.md`, `040c6a5`, `e2c093a` |
| API locale, pannello, osservabilità e manutenzione | **INTEGRATO** | `docs/rag-v5-http-api-validation-01.md`, `docs/knowledge-panel-api-v1.md`, `docs/rag-v5-api-observability-01.md`, `docs/rag-v5-runtime-maintenance-01.md` |
| Holdout esterno Drive11 6/6 | **VALIDATO** | `docs/v5-external-drive11-holdout-01.md`, `21eaada`, `31ff5ad` |
| Benchmark generico breve/medio/complesso 3/3 | **VALIDATO** | `docs/rag-v5-api-profile-benchmark-01.md`, `37d3ee0`–`3a0af91` |
| Cinque PDF FIGC, collection API 6410/157 | **VALIDATO e INTEGRATO** | `docs/figc5-candidate-integration-01.md`, `936b4c4` |

Il `CERTIFICATO` locked non si estende a Drive11, FIGC5, API o domande
arbitrarie. L'attività tecnica corrente è l'osservazione prolungata. La
pubblicazione di `football-lab.byoursite.com` è **VALIDATA e INTEGRATA** e il
reboot completo è VALIDATO. Consumer esterno,
parallelismo generativo e nuove certificazioni sono decisioni facoltative.

Le voci sotto sono cronologia immutabile: uno stato storico non prevale sulla
sintesi corrente e non costituisce automaticamente un'attività aperta.

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
| V5-CERT-02 | Certificazione V5 locked e confronto V4 | `040c6a5`, closeout corrente | `docs/v5-certification-closeout-01.md` | 10/10 V5; V4 non eleggibile 0/10 per fonti assenti; freeze e default CLI verificati | CERTIFICATO |

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

Attività: isolare assenza nel pool o perdita nel rerank di estratti per fresh_03 e fresh_10. Script: `scripts/diagnose_v5_rerank_failures_v1.py`. Commit: `e7f9e4b`, correzione normalizzazione `c4ee2b5`. Report: `docs/v5-rerank-trace-01.md` (commit `adf47ee`), dati VPS `evaluation/runtime-archive/diagnostica_v5_rerank_failures_v1.json`. Risultato: collection 5319/34 invariata; fresh_03 manuale Transizioni assente dai 24 candidati dense; fresh_10 Ussia pagina 17 presente nel pool filtrato ma al rango 9, fuori dalla top8. Decisione: preservare corpus e Chroma, progettare correzioni motivate di recupero e selezione senza ripetere il benchmark equivalente. TODO aggiornato `26154a0`. Stato: ESEGUITO.


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

### V5-HYBRID-CANDIDATE-INTERNAL-ASSESSMENT-02

Attività: aggiornare l'audit locked sostituendo soltanto fresh_03 con la nuova evidenza V4 e riusando gli altri nove esiti già valutati. Script: nessuno; audit read-only dei report. Report: `docs/v5-hybrid-candidate-internal-assessment-02.md`. Risultato: fresh_03 passa da FAIL a PASS; PASS interni fresh_02/03/04/05/06/08, FAIL fresh_01/07/09/10, totale composito 6/10. Decisione: non ripetere il benchmark completo; proseguire con differenze tecniche documentate sui quattro FAIL. Valore ufficiale locked ancora 5/10 fino a integrazione e valutazione complessiva. Stato: ESEGUITO; non VALIDATO, INTEGRATO o CERTIFICATO come sistema completo.

### V5-POST-LOSS-PRESSURE-GUIDANCE-01

Attività: eliminare la confusione fresh_10 tra riaggressione immediata dopo perdita e pressing alto generico mostrata dal report targeted esistente. Script: `smoke_test_rag_v5_e2e.py`, `tests/test_v5_source_hybrid_rank_v4.py`. Commit: `8b62956`. Report: `docs/v5-post-loss-pressure-guidance-01.md`. Risultato: guida attivata da concetti perdita + pressione/riaggressione, senza ID o fonti hardcoded; richiede evidenze esplicitamente post-perdita ed esclude fuorigioco/rimesse laterali come prova equivalente. Test offline 7/7 e compilazione superati; VPS DA FARE. Decisione: consentire una sola generazione fresh_10 con copertura targeted già verificata e valutazione mandatory/forbidden claim. Stato: IMPLEMENTATO; non ESEGUITO, VALIDATO, INTEGRATO o CERTIFICATO.

### V5-POST-LOSS-PRESSURE-GUIDANCE-01 — generazione VPS

Attività: verificare la guida generica fresh_10 con copertura targeted già validata. Script: wrapper locked con source-aware, exercise-candidate, priority-exact, targeted-coverage e `--only-ids fresh_10`; implementazione `8b62956`. Report: `docs/v5-post-loss-pressure-guidance-01.md`; evidenza VPS `evaluation/v5_post_loss_pressure_fresh10_v1.json`, SHA-256 `d1cdad96dcdb7f5cd37fbd69e04f04f47807f2a4c6449a3c2898688d8bf321aa`. Risultato: mandatory claim presenti e distinzione finale esplicita, ma la rimessa laterale F8 resta elencata fra le condizioni post-perdita; forbidden claim non completamente risolto. Citazioni invalide 0, Chroma 5319 invariato, 150.02 s. Decisione: non validare o ripetere; prossima variante soltanto con omissione esplicita delle evidenze di pressing generale dalla risposta post-perdita. Stato: ESEGUITO; non VALIDATO, INTEGRATO o CERTIFICATO.

### V5-POST-LOSS-CONTEXT-FILTER-02

Attività: rimuovere dal contesto post-perdita le evidenze di pressing generale che la guida precedente non ha escluso dalla risposta. Script: `smoke_test_rag_v5_e2e.py`, `tests/test_v5_source_hybrid_rank_v4.py`. Commit: `ecad16b`. Report: `docs/v5-post-loss-context-filter-02.md`. Risultato: filtro concettuale conserva targeted promoted e testi esplicitamente con perdita/palla persa/riaggressione/copertura preventiva, registra gli esclusi; nessun ID o fonte hardcoded. Test offline 8/8 e compilazione superati; VPS DA FARE. Decisione: consentire una sola generazione fresh_10 e verificare mandatory/forbidden claim, citazioni e indice. Stato: IMPLEMENTATO; non ESEGUITO, VALIDATO, INTEGRATO o CERTIFICATO.

Attività: verificare il filtro contestuale post-perdita con l'unica generazione differenziale autorizzata. Script: wrapper locked con source-aware, exercise-candidate, priority-exact, targeted-coverage e `--only-ids fresh_10`; implementazione `ecad16b`. Report: `docs/v5-post-loss-context-filter-02.md`; evidenza VPS `evaluation/v5_post_loss_context_fresh10_v2.json`, SHA-256 `25c19cf4497ff4205d016a24e14a55e24c164ddaa8c988d78bed61541c92dc60`. Risultato: `COMPLETE 1/1`, 93.89 s; mandatory claim Ussia e manuale presenti, forbidden claim assente, cinque evidenze generiche escluse, citazioni invalide 0, Chroma 5319 e candidato 34 invariati. Decisione: `fresh_10` VALIDATO nel perimetro opt-in; non ripetere. Audit composito aggiornato a 7/10 in `docs/v5-hybrid-candidate-internal-assessment-03.md`; valore ufficiale locked ancora 5/10. Stato: VALIDATO; non INTEGRATO o CERTIFICATO.

Attività: impedire la contaminazione fra tassonomie omonime quando la domanda attribuisce una tesi a un singolo autore, osservata in `fresh_07` fra zona B di Foscarini e zona B di Indiani. Script: `smoke_test_rag_v5_e2e.py`, `run_rag_v5_locked_candidate_v2.py`, `tests/test_v5_source_hybrid_rank_v4.py`. Commit: `33749bf`, wrapper scoped `8404495`. Report: `docs/v5-named-source-context-filter-01.md`. Risultato: il filtro source-aware conserva soltanto la fonte esplicitamente nominata quando presente, ma non si attiva per confronti o richieste del manuale interno; registra gli esclusi. Nessun ID benchmark, pagina o tassonomia hardcoded; test offline 8/8 e compilazione superati. Decisione: consentire una sola generazione differenziale `fresh_07`, quindi valutare mandatory/forbidden claim, citazioni e indici. Stato: IMPLEMENTATO; non ESEGUITO, VALIDATO, INTEGRATO o CERTIFICATO.

Attività: verificare il filtro di fonte nominata su `fresh_07`. Script: wrapper locked combinato con `--only-ids fresh_07`; implementazione `33749bf`, `8404495`. Report: `docs/v5-named-source-context-filter-01.md`; JSON VPS `evaluation/v5_named_source_context_fresh07_v1.json`, SHA-256 `4298e32bdff76615fa1cd0369e2bb36ee928a96c611b8bb70245b2c1d812230f`. Risultato: `COMPLETE 1/1`, 97.32 s; quattro fonti estranee escluse, quattro evidenze Foscarini, citazioni invalide 0, indici 5319/34 invariati. La risposta copre pressione laterale e perdita pericolosa, ma omette i playmaker braccati e attribuisce ambiguamente il pericolo all'avversario. Decisione: non validare o ripetere; consentire solo una variante con guida concettuale sulla completezza e sull'attribuzione prudente. Stato: ESEGUITO; non VALIDATO, INTEGRATO o CERTIFICATO.

Attività: completare l'attribuzione concettuale della risposta su laterali, zona B e pressione a invito dopo l'esito V1 incompleto. Script: `smoke_test_rag_v5_e2e.py`, `tests/test_v5_source_hybrid_rank_v4.py`. Commit: `9a1a903`. Report: `docs/v5-named-source-context-filter-01.md`. Risultato: guida attivata dai concetti della domanda, senza ID o fonte hardcoded; richiede playmaker braccati e laterali pressati, attribuzione prudente del pericolo e limite contro il divieto universale. Test offline 9/9 e compilazione superati. Decisione: consentire una sola generazione V2 `fresh_07`; valutare tutti i claim e gli indici. Stato: IMPLEMENTATO; non ESEGUITO, VALIDATO, INTEGRATO o CERTIFICATO.

Attività: verificare la V2 di attribuzione laterali/zona B su `fresh_07`. Script: wrapper locked combinato con `--only-ids fresh_07`; implementazione `33749bf`, `8404495`, `9a1a903`. Report: `docs/v5-named-source-context-filter-01.md`; JSON VPS `evaluation/v5_named_source_context_fresh07_v2.json`, SHA-256 `9da89f8287a02504445501800fbf73df6c752603f30b9a043216ae51ee40b371`. Risultato: `COMPLETE 1/1`, 78.5 s; mandatory claim completo, rischio situazionale e forbidden claim assente; sole quattro evidenze Foscarini, quattro estranee escluse, citazioni invalide 0, indici 5319/34 invariati. Decisione: `fresh_07` VALIDATO, non ripetere. Audit composito aggiornato a 8/10 in `docs/v5-hybrid-candidate-internal-assessment-04.md`; valore ufficiale locked 5/10. Stato: VALIDATO; non INTEGRATO o CERTIFICATO.

Attività: recuperare le evidenze mancanti per la decisione di consolidare dopo riconquista senza mescolare fasi difensive. Script: diagnostica read-only Chroma, `v5_targeted_coverage_v1.py`, `smoke_test_rag_v5_e2e.py`, test offline. Commit: `7004986`. Report: `docs/v5-consolidation-context-reservation-01.md`. Risultato: nei 62 chunk del manuale, `Quando è opportuno` e `Pro e contro` a pagina 3 contengono rispettivamente le quattro condizioni e il trade-off richiesto; collection 5319 invariata. La riserva usa concetti e headings, non ID benchmark/chunk; test 10/10 e compilazione superati. Decisione: consentire una sola generazione `fresh_09` con configurazione combinata e valutazione claim-level. Stato: IMPLEMENTATO; non ESEGUITO, VALIDATO, INTEGRATO o CERTIFICATO.

Attività: eseguire la prima generazione con riserva di contesto su `fresh_09`. Script: wrapper locked combinato con `--only-ids fresh_09`; implementazione `7004986`. Report: `docs/v5-consolidation-context-reservation-01.md`; JSON VPS `evaluation/v5_consolidation_context_fresh09_v1.json`, SHA-256 `39a8678d9831ee350a83856480dd2bb68df85a0495ace03278a4b7267f21d410`. Risultato: `COMPLETE 1/1`, 69.32 s; mandatory claim completi, ma risposta include passaggi estranei sul possesso avversario consolidato e raddoppio difensivo; citazioni invalide 0, indici 5319/34 invariati. Decisione: non validare o ripetere; filtrare la fase prima di una V2. Stato: ESEGUITO; non VALIDATO, INTEGRATO o CERTIFICATO.

Attività: escludere dal contesto di consolidamento dopo riconquista le fasi difensive estranee. Script: `v5_targeted_coverage_v1.py`, `smoke_test_rag_v5_e2e.py`, test offline. Commit: `1bbfb60`. Report: `docs/v5-consolidation-context-reservation-01.md`. Risultato: filtro concettuale conserva i promossi e gli estratti dello stesso manuale che citano consolidare, riconquista o recuperatore; registra gli esclusi. Test offline 11/11 e compilazione superati. Decisione: consentire una sola V2 `fresh_09` e applicare la rubrica completa. Stato: IMPLEMENTATO; non ESEGUITO, VALIDATO, INTEGRATO o CERTIFICATO.

Attività: verificare il filtro di fase V2 su `fresh_09`. Script: wrapper locked combinato; implementazione `1bbfb60`. Report: `docs/v5-consolidation-context-reservation-01.md`; JSON VPS `evaluation/v5_consolidation_context_fresh09_v2.json`, SHA-256 `b73e17b767d913a6230c0d76b974ea563f03554640778068e90a3d9aa4169e55`. Risultato: `COMPLETE 1/1`, 60.23 s; mandatory completi, ma `riconquista del territorio` supera il marker generico e introduce ancora fase difensiva; citazioni invalide 0, indici 5319/34 invariati. Decisione: non validare; distinguere semanticamente evento di recupero e territorio. Stato: ESEGUITO; non VALIDATO, INTEGRATO o CERTIFICATO.

Attività: distinguere «dopo una riconquista» da «riconquista del territorio» nel filtro di consolidamento. Script: `v5_targeted_coverage_v1.py`, test offline. Commit: `c9a41e8`. Report: `docs/v5-consolidation-context-reservation-01.md`. Risultato: marker reso contestuale, test 11/11 e compilazione superati. Decisione: consentire una sola V3 `fresh_09`; nessun altro rerun equivalente. Stato: IMPLEMENTATO; non ESEGUITO, VALIDATO, INTEGRATO o CERTIFICATO.

Attività: verificare la distinzione evento/territorio V3 su `fresh_09`. Script: wrapper locked combinato; implementazione `c9a41e8`. Report: `docs/v5-consolidation-context-reservation-01.md`; JSON VPS `evaluation/v5_consolidation_context_fresh09_v3.json`, SHA-256 `56d4dd6bc68a0056adcc438e87f704ebfd113802953be9d03e8de92d1b0d1bc3`. Risultato: `COMPLETE 1/1`, 47.44 s; mandatory completi, forbidden assente, quattro evidenze estranee escluse, citazioni invalide 0, indici 5319/34 invariati. Decisione: `fresh_09` VALIDATO e non ripetere; audit composito `docs/v5-hybrid-candidate-internal-assessment-05.md` a 9/10. Il valore ufficiale locked resta 5/10 fino a integrazione e regressione completa. Stato: VALIDATO; non INTEGRATO o CERTIFICATO.

Attività: integrare le correzioni validate in un unico profilo locked senza targeting basato sugli ID del benchmark. Script: `run_rag_v5_locked_candidate_v2.py`, `smoke_test_rag_v5_e2e.py`, `v5_targeted_coverage_v1.py`, test offline. Commit: `41c86bb`. Report: `docs/v5-integrated-candidate-profile-01.md`. Risultato: `--integrated-candidate` abilita source-aware, exercise candidate, exact priority, coperture concettuali e heading routing V4; confronto Ussia/manuale attivato dai concetti della domanda e routing heading compatibile con le altre coperture. Test offline 12/12, compilazione superata. Decisione: consentire una sola regressione completa dei dieci casi locked; il 9/10 composito non sostituisce tale evidenza. Stato: IMPLEMENTATO; non ESEGUITO, VALIDATO, INTEGRATO o CERTIFICATO.

Attività: regressione completa e adjudication del profilo unico locked. Script: `run_rag_v5_locked_candidate_v2.py --execute --integrated-candidate`; profilo commit `41c86bb`. Report: `docs/v5-integrated-candidate-final-assessment-01.md`; JSON VPS `evaluation/rag_v5_integrated_candidate_full_v1.json`, SHA-256 `20ec77d22cb5bb4548d6589a41aecd01e529ee53fd45fb199631d766c471c86d`. Risultato: `COMPLETE 10/10`, 814.98 s, zero citazioni invalide, Chroma 5319 e candidato 34 invariati. Adjudication: PASS fresh_02–fresh_10; FAIL fresh_01 perché non esplicita assenza di misure comparative/percentuali. Punteggio ufficiale locked integrato 9/10. Decisione: soglia raggiunta; non ripetere. Profilo INTEGRATO nel wrapper e risultato VALIDATO; non CERTIFICATO, confronto V4 ancora DA FARE. Stato: INTEGRATO.

Attività: correggere il solo FAIL integrato distinguendo giudizio qualitativo e prova comparativa nelle domande sul limite di una maggiore efficacia. Script: `smoke_test_rag_v5_e2e.py`, test offline. Commit: `77e568c`. Report: `docs/v5-qualitative-efficacy-limit-01.md`. Risultato: guida concettuale senza ID/autore/pagina hardcoded; conserva il giudizio della fonte, richiede dichiarazione dell'assenza di misure/percentuali e vieta di sostituire un limite didattico diverso. Test offline 13/13, compilazione superata. Decisione: consentire una sola generazione differenziale `fresh_01`; regressione completa soltanto dopo PASS. Stato: IMPLEMENTATO; non ESEGUITO, VALIDATO, INTEGRATO o CERTIFICATO.

Attività: verificare la guida sul limite probatorio con un solo differenziale `fresh_01`. Script: wrapper locked `--integrated-candidate --only-ids fresh_01`; implementazione `77e568c`. Report: `docs/v5-qualitative-efficacy-limit-01.md`; JSON VPS `evaluation/v5_qualitative_efficacy_fresh01_v1.json`, SHA-256 `42f7200c217c4cdd2c40ff55034c8fb04cbc481a8a997ad01d8d388b94bcc13e`. Risultato: `COMPLETE 1/1`, 139.16 s; tre zone complete, giudizio qualitativo preservato, assenza di misure/percentuali esplicitata, forbidden assenti, citazioni invalide 0, indici 5319/34 invariati. Decisione: `fresh_01` VALIDATO, non ripetere; consentire una sola regressione completa per attestare 10/10 integrato. Stato: VALIDATO; non ancora INTEGRATO nella regressione completa o CERTIFICATO.

Attività: regressione finale del profilo integrato dopo la correzione `fresh_01`. Script: `run_rag_v5_locked_candidate_v2.py --execute --integrated-candidate`; implementazione `77e568c`, profilo `41c86bb`. Report: `docs/v5-integrated-candidate-final-assessment-02.md`; JSON VPS `evaluation/rag_v5_integrated_candidate_full_v2.json`, SHA-256 `f2d54944085b1586067679ac76fb6e2696e5ab24d36d40e84cd3ffb2d4f76a55`. Risultato: `COMPLETE 10/10`, 824.35 s, citazioni invalide 0, Chroma 5319 e candidato 34 invariati. `fresh_01` unico output cambiato e ora PASS; fresh_02–fresh_10 risposte/evidenze identiche alla V1 già PASS. Adjudication ufficiale 10/10. Decisione: soglia massima raggiunta, non ripetere; restano confronto V4, fingerprint/freeze runtime e decisione di promozione ordinaria prima della certificazione. Stato: INTEGRATO; risultato VALIDATO, non CERTIFICATO.

Attività: predisporre un confronto V4/V5 sullo stesso manifest che verifichi prima l'eleggibilità delle fonti gold. Script: `compare_v4_v5_locked_source_coverage.py`. Commit: `12b2769`. Report: `docs/v4-v5-locked-source-coverage-comparison-01.md`. Risultato: inventario VPS preliminare mostra V4 `dribbling_tactics_v4_qwen3_embedding_06b` con 86 chunk da due fonti e V5 con 5319 chunk da 141; lo script verifica hash e presenza per caso senza embedding, LLM o scritture. Decisione: eseguire una sola verifica read-only; non generare risposte V4 se le fonti gold sono assenti. Stato: IMPLEMENTATO; non ESEGUITO, VALIDATO, INTEGRATO o CERTIFICATO.

Attività: confrontare la disponibilità delle fonti gold nel manifest locked fra V4 e V5. Script: `compare_v4_v5_locked_source_coverage.py`, commit `12b2769`. Report: `docs/v4-v5-locked-source-coverage-comparison-01.md`; JSON VPS SHA-256 `7e16980a7ef014b991e4c92905e85a490163bf19420368dbbb7109566fa38f56`. Risultato: V4 0/10 casi eleggibili (86 chunk, due fonti); V5 10/10 (5319 chunk, 141 fonti); nessuna scrittura. Decisione: non eseguire dieci generazioni V4 prive delle fonti ammesse; confronto qualitativo locked non applicabile alla V4, vantaggio V5 dimostrato a livello di copertura. Stato: VALIDATO.

Attività: predisporre fingerprint e freeze riproducibile del runtime V5 integrato. Script: `fingerprint_v5_integrated_runtime.py`. Commit: `5262067`. Report: `docs/v5-runtime-fingerprint-freeze-01.md`. Risultato: registra commit, branch, pulizia tracked, Python, librerie, modelli Ollama, hash file critici, configurazioni e conteggi collection; invarianti 5319/34, nessuna scrittura agli indici. Compilazione superata. Decisione: consentire una sola esecuzione VPS e verificare il report prima del freeze. Stato: IMPLEMENTATO; non ESEGUITO, VALIDATO, INTEGRATO o CERTIFICATO.

Attività: acquisire e validare il fingerprint runtime V5 integrato. Script: `fingerprint_v5_integrated_runtime.py`, commit `5262067`. Report: `docs/v5-runtime-fingerprint-freeze-01.md`; JSON VPS SHA-256 `55a117b045c9420660f13f4ba192b292954587e79f202e8f300931b3f351a2eb`. Risultato: commit `37fee73`, tracked clean, Python 3.12.3, Chroma 1.5.9, llama-index-embeddings-ollama 0.10.0, sentence-transformers 6.1.0, torch 2.6.0+cpu, Ollama 0.40.5, modelli e hash file registrati, collection 5319/34. Decisione: freeze VALIDATO; ogni variazione richiede nuova evidenza. Stato: VALIDATO.

Attività: promuovere il profilo integrato a default dell'entry point CLI mantenendo rollback esplicito. Script: `run_rag_v5_locked_candidate_v2.py`, test offline. Commit: `040c6a5`. Report: `docs/v5-default-promotion-01.md`. Risultato: invocazione senza flag usa il profilo integrato; `--legacy-profile` ripristina i flag precedenti; nessun servizio RAG attivo da riconfigurare. Test offline 14/14, compilazione superata. Decisione: consentire un solo smoke test post-promozione `fresh_03` senza flag profilo; verificare output e rollback statico. Stato: IMPLEMENTATO; non ESEGUITO, VALIDATO, INTEGRATO o CERTIFICATO.

Attività: smoke post-promozione e freeze definitivo. Script: wrapper senza flag profilo su `fresh_03`, poi `fingerprint_v5_integrated_runtime.py`. Commit promozione `040c6a5`, deploy `e46746a`. Report: `docs/v5-default-promotion-01.md`, smoke SHA-256 `81481332bac25ab6cfdac60f72060e1dcb4f2cdff93fe95c402c69989deee472`; fingerprint V2 SHA-256 `f5718a39978495894964f79c4a9b5f4be42277affde88fe692b5382cb7c6cca9`. Risultato: `PROFILE integrated`, tutti i flag attivi, risposta/evidenze identiche alla regressione 10/10, citazioni invalide 0, indici 5319/34 invariati; runtime post-promozione tracked clean e congelato. Decisione: promozione INTEGRATA, freeze VALIDATO, rollback `--legacy-profile` disponibile. Stato: INTEGRATO.

Attività: closeout di certificazione e riconciliazione degli stati. Script: nessuna nuova esecuzione; audit delle evidenze qualità, confronto, freeze, promozione e smoke. Report: `docs/v5-certification-closeout-01.md`. Risultato: tutte le correzioni isolate VALIDATE risultano successivamente INTEGRATE nel profilo default; V5 10/10, V4 non eleggibile per assenza fonti, runtime congelato e rollback verificato. Decisione: certificare il manifest locked e il wrapper CLI predefinito; escludere esplicitamente servizi HTTP/UI non esistenti. Stato: CERTIFICATO.

Attività: riconciliare il TODO dopo certificazione e merge in `main`. Script: nessuno, revisione documentale. Commit: `5b9f9b1`. Report: `docs/todo-reconciliation-post-certification-01.md`. Risultato: la testata operativa separa closeout concluso, prossima fase applicativa, manutenzione e miglioramenti opzionali; le caselle storiche restano preservate ma non sono più una lista operativa. Decisione: usare esclusivamente P0-P3 iniziali per scegliere nuovo lavoro e non riaprire test assorbiti dal 10/10. Stato: VALIDATO.

Attività: audit alberatura e pulizia Alibaba. Script: nessuno; inventario Git/VPS e controlli read-only su processi, servizi, cron, file aperti, cache, modelli e fingerprint. Commit: `957f350`. Report: `docs/project-tree-cleanup-audit-01.md`. Risultato: nessuna dipendenza Alibaba operativa; cache/lock rimossi, runner invariato, collection 5319/34, mMARCO/BGE/Surya presenti. Il precedente dato 600M dereferenziava storage condiviso; rimozione fisica diretta circa 152K. Decisione: validare la sola rimozione Alibaba; preservare `.venv`, knowledge, indici e modelli attivi, classificare il resto prima di altre cancellazioni. Stato: VALIDATO.

Attività: pulizia dei componenti rigenerabili non usati dal runtime certificato. Script: nessuno; controlli su file aperti, processi, riferimenti runtime e CLI ufficiale `hf cache`. Commit: `66d877d`. Report: `docs/project-tree-cleanup-audit-01.md`. Risultato: rimossi ambiente Ragas 766M, cache pip 259M, BGE 2.3G, Qwen3-Reranker 1.2G e blob non referenziati 629M; arrestati due Surya orfani. Root 48%→33%, 39G liberi, swap quasi vuota; runtime importabile, collection 5319/34 e runner invariato. Decisione: preservare codice/test/evidenze, `.venv`, knowledge, mMARCO, Docling/Surya e indici; modelli eliminati riscaricabili. Stato: VALIDATO.

Attività: classificazione completa script e riconciliazione evidenze runtime. Script: `audit_script_dependencies.py`, `inventory_runtime_evidence.py`. Commit scanner: `b081230`, documentazione `9fbb8a3`; report: `docs/script-classification-v2.md`, `docs/runtime-evidence-reconciliation-01.md`; manifest: `evaluation/script_inventory_v2.json`, `evaluation/runtime_evidence_manifest_v1.json`. Risultato: 200 script senza errori sintattici (32 keep, 7 guarded, 161 archivio in sede); 87 JSON runtime per 2.724.476 byte catalogati con hash, inclusi 4 di certificazione, 55 diagnostici, 26 storici e 2 riservati. Decisione: non cancellare o spostare codice/evidenze di pochi MB; preservare import, link e privacy, usare i manifest come indice autorevole. Stato: VALIDATO.

Attività: riordino fisico dei JSON runtime sparsi. Script: aggiornato default di `diagnose_v5_rerank_failures_v1.py`; nessun test o report cancellato. Report: `docs/runtime-evidence-reconciliation-01.md`. Risultato: 15 JSON spostati dalla radice del motore a `evaluation/runtime-archive/`, radice portata a zero JSON, riferimenti Git aggiornati e manifest rigenerato. Decisione: ogni nuovo output runtime deve essere scritto sotto `evaluation/`; vietare nuovi JSON nella radice. Stato: VALIDATO.

Attività: implementare e validare l'adattatore HTTP applicativo V5. Script: `api/rag_v5_api.py`, `scripts/run_rag_v5_query.py`, test `tests/test_rag_v5_api.py`; commit `9472564`, unità utente `60bf7b2`. Report: `docs/rag-v5-http-api-contract-01.md`, `docs/rag-v5-http-api-validation-01.md`. Risultato: test offline 3/3, health 200, readiness autenticata 200 e 401 senza token; singola domanda nuova completata con 8 evidenze, F1–F8 valide, output SHA-256 `9483b5b7f4b5a04b991185c76e85a8a2680f303aef979cce6008a46965ebfc31`, indici 5319/34 invariati. Servizio utente active/enabled su localhost, token 0600; `Linger=no`. Decisione: API VALIDATA e INTEGRATA solo come servizio locale di sessione; non certificata per domande arbitrarie né persistente al boot, nessuna esposizione Internet. Stato: INTEGRATO.

Attività: abilitare la persistenza del servizio utente API. Script: nessuno; configurazione host `loginctl enable-linger football` eseguita dal titolare. Report: `docs/rag-v5-http-api-validation-01.md`. Risultato: `Linger=yes`, unità riavviata, active/enabled, health e readiness verificati da nuova sessione SSH, bind `127.0.0.1:8088`, permessi token 0600 e output 0700. Decisione: persistenza utente VALIDATA; non eseguire un reboot dedicato, verificare al prossimo riavvio manutentivo. Stato: INTEGRATO.

Attività: carico control-plane, recovery, client e preparazione HTTPS. Script: `benchmark_rag_v5_api_control_plane.py`, `api/rag_v5_client.py`; commit `d9eafc1`; report `docs/rag-v5-api-operational-validation-01.md`. Risultato: health 500/500 a concorrenza 25, mediana 3.36 ms, readiness 200; nessun job; kill del main process recuperato da systemd con nuovo PID e `NRestarts=1`. Client applicativo implementato. Template Nginx pronto, ma nessun dominio o proxy installato. Decisione: VALIDARE carico controllo/recovery; mantenere worker RAG seriale; collegamento consumer DA FARE; HTTPS BLOCCATO fino a DNS/certificato, nessuna esposizione diretta di 8088. Stato: VALIDATO.

### V5-TACTICAL-CORPUS-DRIVE11-CANDIDATE-01

Attività: riapertura autorizzata dal titolare dopo la certificazione V5 per acquisire gli 11 PDF calcistici già riconciliati e verificare il flusso completo della pipeline. Differenza tecnica: corpus nuovo; non è ripetizione del benchmark sul corpus 141/5319. Script: `ingest_pdfs.py`, `build_rag_index_v5_multisource.py`, `run_rag_v5_locked_candidate_v2.py`; builder e runner resi parametrizzabili per collection/count espliciti. Commit: DA FARE. Report: `docs/v5-tactical-corpus-drive11-candidate-01.md`. Risultato: 11 PDF trasferiti nella directory candidata isolata; file privato escluso; ingestion e test DA FARE. Decisione: non modificare né promuovere la collection certificata finché integrità, retrieval e benchmark end-to-end del candidato non sono verificati. Stato: IMPLEMENTATO.

Attività: esecuzione Drive11 e benchmark end-to-end candidato. Script: pipeline parametrizzata; report runtime `evaluation/runtime-archive/v5_drive11_candidate_locked_v1.json`. Commit implementazione iniziale `ed3bc50`. Risultato: 11/11 hash e output Docling v2 validi, 877 chunk aggiunti alla copia della baseline, candidato 6196 invariato durante il test; 10/10 esecuzioni con citazioni valide, audit qualitativo 9/10 perché fresh_10 non include il manuale esplicitamente richiesto. Decisione: non promuovere; implementare discovery metadata-driven dei manuali e riserva di una fonte manuale quando la domanda la richiede esplicitamente, poi verifica differenziale. Stato: ESEGUITO.

Attività: correzione regressione, integrazione API e collaudo reale della pipeline Drive11. Script: runner/routing V5 e `api/rag_v5_api.py`; commit `21639cb`, `aca6a8d`, `b5eb4bf`, `9b0c35a`, `fda0a81`. Report runtime: `v5_drive11_candidate_fresh10_manual_v2.json`, `v5_drive11_candidate_locked_v2.json`, `v5_drive11_named_source_retrieval_v1.json`, più job API su `vincenzo-italiano_tesi`. Risultato: regressione generativa 10/10 con fresh_01-09 invariati e fresh_10 corretto; retrieval post-routing 10/10; query HTTP sulla nuova fonte con routing ed evidenze esclusivamente dalla tesi, citazioni valide, 6196→6196. Durante il collaudo è stata scoperta e corretta una race: il job veniva accodato prima della scrittura completa della request, poteva uccidere il worker lasciando health 200; ora scrittura atomica precede la coda, le eccezioni non terminano il worker e readiness ne verifica la vitalità. Test API 3/3. Decisione: configurare l'API persistente sulla collection Drive11; conservare la collection 5319 come rollback. Stato: INTEGRATO; non CERTIFICATO per domande arbitrarie.

### FIGC-PDF-DISCOVERY-V1

Attività: implementare il primo stadio del monitor documentale FIGC senza modificare il corpus operativo. Differenza tecnica: nuova sorgente esterna e nuovo registro acquisizioni; nessun test RAG equivalente. Script: `scripts/figc_pdf_discovery.py`, test `tests/test_figc_pdf_discovery.py`. Commit: DA FARE. Report: `docs/figc-pdf-discovery-v1.md`. Risultato: dry-run predefinito, allowlist HTTPS FIGC, crawl limitato categoria/news, verifica MIME/firma/size/SHA-256, download atomico opt-in, eventi JSONL append-only e classificazione prudente. Decisione: collaudo shadow con tre URL già documentati e crawl bounded; nessuna ingestion/Chroma fino a verifica risultati e deduplica. Stato: IMPLEMENTATO.

Attività: collaudo shadow, deduplica interna, catalogo e scheduling del monitor FIGC. Script: `figc_pdf_discovery.py`, unit/timer `football-figc-discovery.user.*`; commit `be0c7f2`, `fa893b9`, `266d8a8`, `5f38313`, `9232e25`. Report: `docs/figc-pdf-discovery-v1.md`; JSON `figc_discovery_shadow_v1.json`, `figc_discovery_initial_crawl_v2.json`, `figc_discovery_internal_dedup_v1.json`. Risultato: test 5/5; tre documenti storici riconosciuti duplicati; otto pagine crawl, zero errori, un nuovo PDF Maresi; nome normalizzato e rerun `duplicate_existing`; contenuto classificato non pertinente e non indicizzato. API sulla collection Drive11 6196 attiva, health/readiness 200. Decisione: integrare il monitor giornaliero senza ingestion automatica; ampliare censimento e similarità solo con nuova evidenza. Stato: VALIDATO per discovery; scheduling INTEGRATO; non CERTIFICATO per archivio storico completo.

Attività: validare l'unit systemd installata con il crawl bounded configurato. Script: `football-figc-discovery.service` tramite timer utente. Report: `figc_discovery_latest.json` e `docs/figc-pdf-discovery-v1.md`. Risultato: `Result=success`, 30 pagine, 10 PDF verificati, due duplicati, otto nuovi candidati, zero errori; 38G liberi. Decisione: nessuna ingestion automatica; completare review editoriale, escludere traduzione duplicata e costruire solo dopo una collection candidata isolata. Stato: ESEGUITO; monitor INTEGRATO, nuovi documenti non VALIDATI per ingestion.

Attività: ridurre la frequenza del monitor FIGC su indicazione del titolare. Script: `football-figc-discovery.user.timer`. Report: `docs/figc-pdf-discovery-v1.md`. Risultato: calendario impostato a sabato 03:15 con jitter massimo di 30 minuti e persistenza dei run saltati; il sabato evita un secondo run immediato durante il cambio CEST/CET del 25 ottobre 2026. Decisione: mantenere il crawl settimanale finché volume e frequenza delle pubblicazioni non giustificano una revisione. Stato: INTEGRATO.

### KNOWLEDGE-PANEL-API-V1

Attività: avviare l'integrazione applicativa con il primo consumer read-only previsto dal TODO Knowledge Base. Differenza tecnica: nuovi endpoint di inventario/provenienza, nessuna generazione o mutazione indice. Script: `api/knowledge_catalog.py`, `api/rag_v5_api.py`; test `test_knowledge_catalog.py`, `test_rag_v5_api.py`. Report: `docs/knowledge-panel-api-v1.md`. Risultato: audit reale 6196 chunk/152 fonti; endpoint stats, documents e search implementati con autenticazione e paginazione limitata. Decisione: test offline e smoke HTTP VPS prima della UI. Stato: IMPLEMENTATO.

Attività: validare il contratto Knowledge API sulla VPS. Script: API e catalogo read-only; report `docs/knowledge-panel-api-v1.md`. Risultato: 7/7 test, endpoint 200, conteggi 6196/152, ricerca con provenienza, primo caricamento 1355,90 ms e cache 1,72–38,42 ms; health/readiness 200 e collection invariata. Decisione: implementare il consumer web locale senza esposizione Internet. Stato: VALIDATO.

Attività: implementare il primo consumer applicativo web. Script: `api/knowledge_panel.html`, route `/panel` in `rag_v5_api.py`; test segreto non incorporato. Risultato: inventario, ricerca e submit/polling RAG implementati; token solo in memoria, header di sicurezza e bind localhost. Decisione: test statici e smoke VPS prima dell'integrazione. Stato: IMPLEMENTATO.

Attività: validare e integrare il consumer web locale. Script: pannello e API; commit `8a7a797`, `2452afa`. Report: `docs/knowledge-panel-api-v1.md`. Risultato: 8/8 test; `/panel` 200 con CSP; nessun token incorporato; inventario recupera tutte le pagine e risposta usa il contratto runtime `questions[0].answer`; health 200. Decisione: usare `/panel` come primo consumer ufficiale locale, accessibile tramite tunnel SSH; vista Qualità e catalogo FIGC restano separati. Stato: INTEGRATO.

### V5-EXTERNAL-DRIVE11-HOLDOUT-01

Attività: ampliare la certificazione oltre i dieci casi locked con fonti realmente nuove. Differenza tecnica: sei fonti Drive11 assenti dalla collection 5319 e domande non eseguite in precedenza. Script: `run_rag_v5_external_holdout_v1.py`; manifest `rag_v5_external_drive11_holdout_v1.json`, SHA-256 `ef3acb4f3499553e1f525d0c09f40bc69eff1a78f6f9990c0ca36d1dbe83c651`. Report: `docs/v5-external-drive11-holdout-01.md`. Risultato: domande, fonti, pagine, evidence ID e claim congelati prima della generazione. Decisione: preflight read-only, poi una sola esecuzione e adjudication claim-level. Stato: IMPLEMENTATO.

Attività: eseguire e giudicare l'holdout esterno Drive11 congelato. Script: `run_rag_v5_external_holdout_v1.py`; commit `21eaada`. Report JSON SHA-256 `e7cbcfcaaf1e069c45551c8a9e7fcfd3deb08fa31e310acc263af3c035b6f04a`. Risultato: 6/6 complete, 668,43 s, mandatory claim completi, forbidden assenti, F1 uguale all'evidence congelata in ogni caso, citazioni invalide zero, collection 6196 invariata. Decisione: estensione fuori locked VALIDATA e da conservare come regressione; non dichiarare certificazione universale. Stato: VALIDATO.

### RAG-V5-API-OBSERVABILITY-01

Attività: aggiungere metriche persistenti al servizio applicativo senza ripetere benchmark generativi. Differenza tecnica: nuovo endpoint e persistenza aggregata; il benchmark control-plane precedente resta riutilizzato. Script: `api/rag_v5_api.py`, test `test_rag_v5_api.py`. Report: `docs/rag-v5-api-observability-01.md`. Risultato: worker/coda/job, contatori cumulativi, durate e stato collection/cache implementati; file atomico privo di domande, risposte e token. Decisione: test offline e smoke VPS, poi misura read-only del control-plane. Stato: IMPLEMENTATO.

Attività: validare metriche persistenti e integrarle nella vista Qualità. Script: API, `knowledge_panel.html`, test; commit `fbf4162`, `424a4b2`. Report: `docs/rag-v5-api-observability-01.md`. Risultato: test 10/10, file 0600 creato all'avvio, endpoint 200; 500/500 richieste a concorrenza 25, mediana 4,19 ms, worker vivo 500/500; nessuna inferenza. Decisione: INTEGRARE osservabilità nel pannello, mantenere worker seriale e raccogliere campioni reali. Stato: VALIDATO e INTEGRATO.

### RAG-V5-RUNTIME-MAINTENANCE-01

Attività: automatizzare controlli e retention del runtime applicativo. Differenza tecnica: nuovo job settimanale; nessun benchmark generativo. Script: `maintain_rag_v5_runtime.py`, test e unit/timer `football-rag-maintenance.user.*`. Report: `docs/rag-v5-runtime-maintenance-01.md`. Risultato: dry-run predefinito, cancellazione limitata ai job API oltre 30 giorni preservando i 100 più recenti; fail-closed su API, worker, collection 6196 e disco; report senza contenuti sensibili. Decisione: test VPS, dry-run e singola esecuzione reale prima di integrare il timer. Stato: IMPLEMENTATO.

Attività: collaudare e integrare la manutenzione runtime. Script/unit commit `5b877cb`. Report: `docs/rag-v5-runtime-maintenance-01.md`. Risultato: 12/12 test; dry-run e run reale con health/readiness 200, collection 6196, disco 30,77%, Git pulito, zero errori e zero rimozioni; unit success, timer domenicale attivo. Decisione: mantenere retention 30 giorni/100 job, fail-closed; nessun intervento su corpus o indici. Stato: VALIDATO e INTEGRATO.

### RAG-V5-PERFORMANCE-PROFILE-01

Attività: implementare un profilo applicativo reversibile per ridurre la latenza di generazione. Differenza tecnica: il campione Coverciano attribuisce 285,42 dei 292,61 secondi a Ollama; il profilo opt-in usa 6 evidenze, guida concisa entro 500 parole e tetto 700 token, mentre il default locked resta 8/senza limite. Script: `smoke_test_rag_v5_e2e.py`, `run_rag_v5_query.py`, `rag_v5_api.py`; report `docs/rag-v5-performance-profile-01.md`. Risultato: implementazione e telemetria estesa completate; test offline e confronto differenziale VPS DA FARE. Decisione: promuovere solo con completezza, citazioni valide, arresto naturale, indice 6196 invariato e latenza materialmente inferiore. Stato: IMPLEMENTATO.

Attività: primo gate VPS del profilo prestazioni. Script: query Coverciano identica alla baseline, 6 evidenze/700 token; JSON `evaluation/runtime-archive/rag_v5_coverciano_performance_v1.json`. Risultato: test 9/9, 193,54 contro 292,61 secondi (-33,8%), prompt 2588 contro 3155, citazioni F1–F5 valide, 6196 invariato; `done_reason=length`, seconda parte troncata. Decisione: non validare né integrare; correggere la guida con due sezioni obbligatorie, niente premessa e massimo 350 parole, quindi un solo nuovo differenziale. Stato: ESEGUITO; correzione IMPLEMENTATO.

Attività: secondo gate e integrazione del profilo prestazioni API. Script: stessa query con guida corretta, 6 evidenze/700 token; JSON `rag_v5_coverciano_performance_v2.json`, SHA-256 `de7c9fee020a67db43c1ef2d4c0bb001c9a65eececcd070a4e63cfa98ab019d2`. Risultato: 161,09 contro 292,61 secondi (-45,0%), `done_reason=stop`, 534 token, due sezioni complete, 6/6 evidenze citate, zero citazioni invalide, collection 6196 invariata. API configurata 6/700, servizio active e health 200; runner locked resta 8/0. Decisione: promuovere nella sola API con rollback 8/0; prestazioni/servizio 9/10, nessuna certificazione universale delle domande arbitrarie. Stato: VALIDATO e INTEGRATO.

### KNOWLEDGE-PANEL-APPLICATION-INTEGRATION-02

Attività: completare il consumer web locale con stato/tempo job, metriche risposta, evidenze navigabili, cronologia effimera ed errori comprensibili. Differenza tecnica: sola UI; nessuna modifica a retrieval, modello, collection o benchmark. Script: `api/knowledge_panel.html`, test statici `test_rag_v5_api.py`; report `docs/knowledge-panel-application-integration-02.md`. Risultato: implementazione completata, token solo in memoria e dati dinamici sottoposti a escaping. Decisione: test offline e smoke HTTP prima dell'integrazione. Stato: IMPLEMENTATO.

### RAG-V5-API-PROFILE-BENCHMARK-01

Attività: misurare il profilo API su domande breve, media e complessa nuove. Differenza tecnica: tre livelli di lunghezza/struttura mai eseguiti, non benchmark locked e non scenario Coverciano. Script: `benchmark_rag_v5_api_profiles_v1.py`; report `docs/rag-v5-api-profile-benchmark-01.md`. Risultato: harness sequenziale e gate automatici implementati. Decisione: una sola esecuzione VPS e audit qualitativo delle tre risposte. Stato: IMPLEMENTATO.

Attività: eseguire e giudicare il benchmark applicativo a tre profili. JSON SHA-256 `06e0f419a9623cd9f973593a7e6e54c944651305e894670c8b5b89ec7fa8783e`. Risultato: 160,18/194,19/146,13 s; 3/3 stop, citazioni valide, 6196 invariato; caso complesso confonde possesso/non possesso e riconquista/perdita. Decisione: non VALIDARE; correzione generica delle fasi e un solo retest complesso. Stato: ESEGUITO.

Attività: revisione editoriale candidati FIGC. Report `docs/figc-candidate-editorial-review-01.md`. Risultato: Soncin, Di Camillo, Rausse, calcio relazionale IT e Mastroianni ammessi come candidati; Venturini/Pica esclusi come statistici, traduzione EN duplicata; Maresi/Santoni già esclusi. Decisione: preservare cinque file in area candidata e non indicizzare senza collection isolata. Stato: VALIDATO.

Attività: remediation audit API `cc2a0cdd-2e17-4a97-b5ef-6c4e1bed4126`. Script: API, template env e guida generazione; report `docs/rag-v5-api-security-remediation-01.md`. Risultato: placeholder rifiutato, server 32 connessioni/timeout 15s, ricerca rate-limited, distinzione fasi tattiche rafforzata. Decisione: test offline/VPS prima dell'integrazione. Stato: IMPLEMENTATO.

Attività: validazione hardening, pulizia FIGC e retest complesso. Risultato: API 10/10 test, placeholder respinto, server bounded 32, undicesima ricerca 429, servizio active; rimossi 24 MB (Venturini, Pica, traduzione EN) e preservati cinque candidati; root 31%/40 GB liberi. Retest complesso 143,29 s, stop, citazioni valide e 6196 invariato ma una frase ancora ambigua. Decisione: hardening VALIDATO/INTEGRATO, pulizia VALIDATA, caso complesso non promosso. Stato: INTEGRATO per sicurezza; ESEGUITO per benchmark complesso.

Attività: chiudere il benchmark complesso con controllo temporale verificabile. Script: `smoke_test_rag_v5_e2e.py`; JSON finale `rag_v5_complex_phase_prune_v2.json`. Risultato: rilevazione delle violazioni, una rigenerazione e rimozione fail-closed dei soli claim completi ancorati a citazione; 132,7 s, stop, sezioni coerenti, citazioni invalide zero, 6196 invariato. Decisione: benchmark applicativo 3/3. Stato: VALIDATO.

Attività: costruire e integrare la candidata FIGC5. Script: ingestion e builder V5 esistenti; report `docs/figc5-candidate-integration-01.md`; locked JSON SHA-256 `3663a392506937da5bc0d989fd3ffa5cfb4578818e7815b2d2590bd4f689784d`. Risultato: 5 documenti/214 chunk, candidata 6410; Soncin validato. Regressione iniziale 9/10 per falso named-source `conclusione`; resolver corretto per richiedere nome proprio su overlap singolo, fresh_04 torna a Ussia/5 secondi. Composito finale 10/10. API ready su 6410/157, baseline 6196 rollback. Decisione: promuovere la candidata nell'API, senza certificazione universale. Stato: VALIDATO e INTEGRATO.

Attività: verificare l'avvio automatico dopo reboot completo della VPS. Script: nessuno; controllo operativo systemd/HTTP; report `docs/rag-v5-full-reboot-validation-01.md`. Risultato: boot 12:42:05, API avviata automaticamente 12:42:14 con `Linger=yes`; health/readiness verdi, pannello 200, collection 6410/157, timer manutenzione e FIGC attivi, zero unità fallite. Decisione: non ripetere senza cambi a unità, linger, boot o configurazione; proseguire soltanto con osservazione prolungata. Stato: VALIDATO.

Attività: completare il pannello con fonti espandibili, export Markdown e feedback persistente privo di contenuti. Script: `api/knowledge_panel.html`, `api/rag_v5_api.py`; test `tests/test_rag_v5_api.py`, `tests/test_knowledge_catalog.py`; report `docs/knowledge-panel-feedback-export-01.md`. Risultato: compilazione Python, suite 14/14, sintassi JavaScript e diff check superati; feedback limitato ai job riusciti e file atomico senza domanda/risposta. Decisione: deploy e smoke VPS senza inferenza. Stato: IMPLEMENTATO.

Attività: integrare e collaudare feedback/export del pannello. Script e report come sopra; commit `e9dda93`. Risultato: suite VPS 14/14, servizio active/running, readiness ready, collection 6410/157 invariata, UI aggiornata servita e contratto negativo feedback 404 corretto; percorso positivo coperto dal test unitario senza contenuti sensibili. Nessuna inferenza eseguita. Decisione: promuovere il completamento del consumer locale; raccogliere feedback soltanto dall'uso reale. Stato: VALIDATO e INTEGRATO.

Attività: rendere osservabile il feedback reale senza contenuti sensibili. Script: API/pannello e test esistenti; report `docs/knowledge-panel-feedback-export-01.md`. Risultato: metriche aggregano totale/utili/non utili da un file per job, ignorano file non validi; vista Qualità aggiornata; test locale 14/14 e sintassi superati. Decisione: deploy e smoke metriche VPS senza inferenza. Stato: IMPLEMENTATO.

Attività: integrare osservabilità feedback; implementazione `8e9b9ce`. Risultato: test VPS 14/14; servizio active, worker vivo, coda zero, collection attesa 6410, feedback iniziale totale/utili/non utili 0/0/0 e vista pannello presente. Nessuna inferenza. Decisione: usare i giudizi reali come segnale operativo, senza promuoverli a certificazione. Stato: VALIDATO e INTEGRATO.

Attività: pubblicare il pannello tramite `footballlab.byoursite.com`. Script: template `deploy/nginx-football-rag-api.conf.example`; report `docs/public-panel-https-01.md`. Risultato: nome e IP target definiti; DNS, Nginx, certificato e collaudo ancora mancanti. Decisione: procedere senza esporre 8088; emissione TLS subordinata alla risoluzione DNS pubblica verso `163.5.26.155`. Stato: DA FARE; certificato BLOCCATO fino al DNS.

Attività: predisporre in sicurezza il reverse proxy pubblico. Configurazioni: `deploy/nginx-footballlab-bootstrap.conf`, `deploy/nginx-footballlab-https.conf`; report come sopra. Risultato: Nginx 1.24 attivo/enabled, Certbot 5.8 installato; bootstrap porta 80 limitato alla challenge ACME e 404 per il resto; API ancora su 127.0.0.1:8088 e health ok. DNS pubblico assente. Decisione: non tentare ACME prima della risoluzione verso `163.5.26.155`; non esporre 8088. Stato: IMPLEMENTATO; emissione TLS BLOCCATO.

Attività: audit sicurezza pre-pubblicazione. Script: API, test e configurazione HTTPS; report `docs/public-panel-security-audit-01.md`. Risultato: porte, permessi 700/600, hardening systemd, segreti e log baseline conformi; individuati tentativi token errato non limitati e query string potenzialmente loggata. Correzioni: bucket auth separato 20/min, log applicativo senza query e formato Nginx `$uri`, TLS/header rafforzati; test offline 16/16. Decisione: deploy e smoke VPS senza inferenza; HTTPS resta dipendente dal DNS. Stato: IMPLEMENTATO.

Attività: validare e integrare hardening pre-pubblicazione; implementazione `9961a39`. Risultato: test VPS 16/16; token errati 20×401 poi 429, token valido ancora ready 200; marker ricerca assente dai log; UFW trovato inattivo e abilitato con sole regole OpenSSH/Nginx Full IPv4/IPv6, nessuna 8088/11434; riconnessione SSH, Nginx/API e bootstrap 404 verificati. Decisione: conservare API/Ollama localhost e completare TLS solo dopo DNS. Stato: VALIDATO e INTEGRATO.

Attività: riconciliare il nome DNS effettivo. Configurazioni Nginx e report HTTPS aggiornati da `footballlab.byoursite.com` al nome creato `football-lab.byoursite.com`; la voce precedente resta cronologia della pianificazione. Risultato: risoluzione pubblica verificata verso `163.5.26.155`. Decisione: procedere con ACME e collaudo pubblico. Stato: VALIDATO per DNS; HTTPS DA FARE.

Attività: completare la pubblicazione HTTPS del Knowledge Panel. Script/configurazione: `deploy/nginx-footballlab-https.conf`; commit di predisposizione e riconciliazione `9961a39`, `5868dbc`; report `docs/public-panel-https-01.md`. Risultato: certificato Let's Encrypt ECDSA emesso per `football-lab.byoursite.com`, scadenza 2027-01-23; `nginx -t` e reload riusciti; HTTP→HTTPS 301, pannello HTTPS 200, endpoint readiness/catalogo/metriche 200 con token e 401 senza token; API e Ollama ancora su localhost; `certbot renew --dry-run` riuscito e timer attivo. Decisione: usare esclusivamente l'URL HTTPS pubblico, non aprire 8088 e non estendere la certificazione locked. Stato: VALIDATO e INTEGRATO.

Attività: correggere l'onboarding del pannello dopo evidenza utente `Domanda fallita: unauthorized`. Differenza tecnica: UI pubblica utilizzabile prima della connessione e assenza di istruzioni per il token; nessuna modifica a retrieval, modello o indice. Script: `api/knowledge_panel.html`, test `tests/test_rag_v5_api.py`; commit `6bca4f0`, guardia nome segreto `e70c674`; report `docs/knowledge-panel-application-integration-02.md`. Risultato: help operativo e recupero amministrativo del token, stato connesso/non connesso, domanda e ricerca disabilitate prima dell'autenticazione, 401 tradotto in istruzione; test VPS 13/13, servizio active, smoke HTTPS catalogo 200 con token e 401 senza token, nessuna inferenza. Decisione: non memorizzare il token nel browser; reinserirlo dopo refresh e mantenere il gate di assenza segreti nella pagina. Stato: VALIDATO e INTEGRATO.

Attività: rendere parlante l'inventario documentale del pannello. Differenza tecnica: nuova tassonomia editoriale derivata e filtri UI; nessuna modifica a collection, embedding, retrieval o generazione. Script: `api/knowledge_catalog.py`, `api/knowledge_panel.html`; test catalogo e pannello; commit `7650fbd`. Report: `docs/knowledge-panel-application-integration-02.md`. Risultato: 157/157 documenti esposti; categorie primarie 120 tattica, 27 tecnica e 10 allenamento; categorie pertinenti non esclusive 153/91/42; conteggi, ricerca titolo e filtro categoria operativi; suite combinate 19/19 e smoke HTTPS superati. Decisione: integrare la biblioteca come vista derivata, senza usare la tassonomia per alterare retrieval o certificazione. Stato: VALIDATO e INTEGRATO.

Attività: predisporre un log analizzabile dopo l'errore UI `not_found`. Differenza tecnica: il job mostrato come running è stato interrotto dal riavvio applicativo effettuato durante il deploy, mentre lo stato dei job è in memoria. Script: `api/rag_v5_api.py`, `api/knowledge_panel.html`; test API; commit `20a0001`. Report: `docs/rag-v5-api-observability-01.md`. Risultato: registro JSONL privacy-safe di avvio e transizioni job, endpoint autenticato e vista pannello; job presente su disco ma assente dalla memoria restituisce `job_lost_after_restart`; suite 19/19, servizio active, endpoint con evento service_started e file `0600`. Decisione: integrare il registro senza contenuti o stderr; usare il messaggio specifico per distinguere riavvii da ID sconosciuti. Stato: VALIDATO e INTEGRATO.

Attività: audit read-only dell'ultimo test applicativo Coverciano fornito dall'utente. Script: lettura del report runtime esistente, nessuna nuova inferenza. Risultato: risposta completa e arresto naturale in 159,18 s, 619 token, ma prevalentemente teorica; evidenze selezionate generiche su triangoli e strategia difensiva, mentre il catalogo contiene fonti più specifiche su 4-3-3/3-5-2 e catene laterali. Il report registra `citation_ids` 1,2,3,4,5,6,10 e `invalid_citation_ids=[10]` con sole sei evidenze. Decisione: non validare il risultato; rendere fail-closed il wrapper applicativo sulle citazioni e diagnosticare separatamente il routing strutturale. Stato: ESEGUITO; qualità non VALIDATA.

Attività: implementare il gate applicativo fail-closed per citazioni. Differenza tecnica: il wrapper accettava report integri anche con citazioni fuori range. Script: `scripts/run_rag_v5_query.py`, test API; commit `ff1461e`. Risultato: validazione esplicita di singolo risultato, indice invariato, almeno una citazione e zero riferimenti invalidi; compilazione e suite VPS 15/15, deploy eseguito senza riavvio e senza interrompere job. Decisione: un report JSON resta conservato per diagnosi, ma il job HTTP fallisce e non presenta la risposta come riuscita. Stato: VALIDATO e INTEGRATO.

Attività: audit read-only della seconda domanda applicativa, eseguita dall'utente prima del deploy del gate. Script: lettura del report runtime `cc23256c...result.json`; nessuna nuova inferenza. Risultato: 172,84 s, citazioni formalmente valide F2/F3/F6, ma risposta tatticamente incoerente con il 4-3-3 iniziale: introduce un “centrocampista esterno”, non costruisce chiaramente la linea a tre e usa fonti su 4-4-2/3-4-1-2. Il catalogo contiene invece estratti specifici su 4-3-3 vs 3-5-2 e sulla catena terzino-mezzala-esterno. Decisione: trattare il limite come debolezza generale del routing strutturale; non ripetere le due baseline, implementare prima una riserva generica verificabile retrieval-only. Stato: ESEGUITO; qualità non VALIDATA; correzione DA FARE.

Attività: implementare routing strutturale generico per domande applicative complesse. Differenza tecnica: selezione attuale diluisce moduli, ruoli e principi nelle domande lunghe. Script: `v5_structural_scenario_routing_v1.py`, integrazione opt-in in `smoke_test_rag_v5_e2e.py` e default della sola API in `run_rag_v5_query.py`; test dedicati e guida generativa. Risultato: estrazione generica di moduli, ruoli e principi; riserva massima di due fonti distinte; istruzione ruolo di partenza → movimento → spazio → dilemma, con divieto di inventare ruoli avversari assenti. Il profilo locked resta invariato. Decisione: test offline, poi retrieval-only sull'ultima domanda; generazione ammessa soltanto se le fonti diventano strutturalmente pertinenti. Stato: IMPLEMENTATO.

Attività: validare e integrare il routing strutturale. Script: router `6233e30`, serializzazione `f372938`, movimento sincronizzato `c68af7e`, riserva a tre `97d84a1`, fixed-choice `d8d3743`; report `docs/structural-scenario-routing-01.md`. Risultato: suite 33/33 e 19/19; retrieval-only v3 include fonti pertinenti su 3-5-2, dilemma quinto/braccetto e combinazioni ala–terzino; generazione v1 6/10 scartata, v2 8,5/10 con corsa diagonale nello spazio alle spalle del braccetto, 96,43 s, stop naturale, citazioni F1/F3/F4/F5/F6 valide e collection 6410 invariata. Decisione: integrare nella sola API, non modificare locked e non ripetere lo stesso scenario; prossimo controllo su scenari indipendenti. Stato: VALIDATO e INTEGRATO.

Attività: verificare la generalizzazione su uno scenario indipendente 3-4-2-1 contro 4-2-4 e confrontare la risposta con una revisione esterna conversazionale. Script: runner API integrato, nessuna modifica preventiva; job `e890ef205ae342868a610ef819b3020a`. Report: `docs/structural-scenario-routing-01.md`; JSON runtime VPS in `evaluation/api-runs/`. Risultato: 189 s, job riuscito, citazioni F1-F4 formalmente valide e indice invariato; risposta incoerente su ruoli, linea a cinque, lato debole e libero, con due evidenze offensive non pertinenti. Google AI Mode ha segnalato le stesse criticita; il voto 27/30 e considerato non calibrato per effetto della conversazione guidata. Decisione: non validare e non ripetere senza separazione di fase, riserva specifica scivolamento/lato debole e telemetria strutturale. Stato: ESEGUITO; non VALIDATO, INTEGRATO o CERTIFICATO.

Attività: stabilire una baseline esterna comparativa sui sei report Coverciano senza rigenerare risposte. Script: `review_runtime_series_gemini_v1.py`, commit `98a615b`; invio autorizzato di domande, risposte ed estratti delle evidenze, senza segreti o PDF completi. Report: `evaluation/gemini_coverciano_runtime_series_v1.json`. Risultato: preflight PASS, richiesta a `gemini-3.1-flash-lite-preview` BLOCCATA da HTTP 503; nessun voto, un tentativo locale, nessun retry automatico. Decisione: conservare V1 e consentire un solo output V2 con il modello `gemini-3-flash-preview` gia collaudato. Stato: BLOCCATO; baseline media non disponibile.

Attività: fallback esplicito del revisore comparativo sul modello gia collaudato. Script: `review_runtime_series_gemini_v1.py`, modello selezionabile commit `92f0a63`. Report: `evaluation/gemini_coverciano_runtime_series_v2.json`. Risultato: risposta Gemini ricevuta ma rifiutata fail-closed con `REVIEW_ID_MISMATCH`; nessuna media o voto accettato. Decisione: preservare V2, usare ID brevi mappati agli UUID runtime e persistere la risposta diagnostica prima del gate; rubrica invariata, un solo V3 consentito. Stato: BLOCCATO.

Attività: verificare se ID brevi e payload singolo sbloccano il revisore Gemini. Script: hardening ID/persistenza commit `35e6002`; report `gemini_coverciano_runtime_series_v3.json` e `gemini_coverciano_runtime_case01_v4.json`. Risultato: sia il batch V3 con ID brevi sia il solo caso 1 V4 hanno restituito HTTP 503 prima del contenuto; ledger locale 4/10, nessun voto. Decisione: non consumare i sei tentativi residui durante l'indisponibilita; riprendere la baseline solo dopo ripristino del servizio, mantenendo report separati. Stato: BLOCCATO.

Attività: riconciliare il client Gemini con la documentazione ufficiale e definire il benchmark Coverciano 100 richiesto dal titolare. Script: `review_runtime_series_gemini_v1.py`; report di progetto `docs/coverciano-100-gemini-benchmark-01.md`. Risultato: `gemini-3.1-flash-lite-preview` risulta spento dal 25 maggio 2026; `gemini-3-flash-preview` e deprecato con sostituzione `gemini-3.6-flash`; `models.list` con la chiave VPS vede 3.6, 3.7 e 3.8 Flash stabili. Google definisce 503 come indisponibilita/sovraccarico transitorio e raccomanda backoff; Batch API e indicata per valutazioni offline massive. Decisione: usare Gemini 3.8 Flash stabile per generare le 100 domande/rubriche e revisione isolata o Batch API, dopo probe minima; modelli preview rimossi dall'allowlist. Stato: IMPLEMENTATO nel client e protocollo; probe/generazione DA FARE.

Attività: probe di inferenza del modello stabile prima del benchmark 100. Script: reviewer migrato a `gemini-3.8-flash` commit `a268dd9`, piu richiesta minima senza dati di progetto. Report: `docs/coverciano-100-gemini-benchmark-01.md`; runtime `gemini_coverciano_runtime_case01_stable_v5.json`. Risultato: caso reale HTTP 503; anche la sola frase “Rispondi esclusivamente con OK” restituisce 503 con messaggio Google di alta domanda temporanea. Decisione: il payload non e la causa; fermare retry immediati, applicare backoff e predisporre Batch API per le 100 domande. Stato: BLOCCATO per capacita esterna; implementazione locale puo proseguire.

Attività: trovare un endpoint Gemini stabile realmente operativo per la seconda AI. Script: probe minime su modelli visibili e reviewer comparativo. Report: `docs/coverciano-100-gemini-benchmark-01.md`; runtime `evaluation/gemini_coverciano_runtime_case01_stable36_v6.json`. Risultato: `gemini-3.6-flash` HTTP 200/OK; revisione reale del caso 1 completata in 27,8 s con 3,0/10, citazione F10 invalida, preventiva errata e fonti generiche correttamente individuate. Decisione: rendere 3.6 Flash il primario, ammettere 3.1 Flash-Lite come fallback e sospendere 3.8 durante alta domanda; usare Batch API per scala 100. Stato: VALIDATO per connettivita e singola revisione; benchmark 100 DA FARE.

### V5-GEM-06 — Revisione Gemini nel pannello applicativo

Attività: collegare realmente la seconda AI al job applicativo dopo il completamento RAG, senza modificare pipeline locked o collection. Script: `api/rag_v5_api.py`, `scripts/review_runtime_series_gemini_v1.py`, pannello `api/knowledge_panel.html`, test `tests/test_rag_v5_api.py`. Commit: DA FARE. Report: `docs/rag-v5-gemini-runtime-review-01.md`. Risultato: implementata revisione opt-in con `gemini-3.6-flash`, stato intermedio `reviewing`, riepilogo limitato a voto/verdetto/errori/evidenze/correzione e fallback non bloccante; prompt base del benchmark 100 registrato integralmente. Decisione: testare sulla VPS, attivare nel servizio e svolgere una sola smoke nuova prima della generazione delle 100 tracce. Stato: IMPLEMENTATO; non ESEGUITO, VALIDATO o INTEGRATO.

### V5-GEM-07 — Generatore Gemini delle 100 tracce

Attività: trasformare il prompt del titolare in un manifest congelabile generato realmente da Gemini. Script: `scripts/generate_coverciano_100_gemini_v1.py`. Commit: DA FARE. Report: `docs/coverciano-100-gemini-benchmark-01.md`. Risultato: generatore fail-closed con modello stabile 3.6, esattamente 100 ID ordinati, dieci categorie bilanciate, controllo duplicati/difficolta/rubriche nascoste, output atomico e divieto di sovrascrittura; nessuna chiamata eseguita. Decisione: compilazione e pubblicazione, poi una singola generazione prompt-only sulla VPS; non inviare PDF, evidenze o segreti nel contenuto. Stato: IMPLEMENTATO; non ESEGUITO o VALIDATO.

Attività: prima generazione prompt-only delle 100 tracce. Script: `generate_coverciano_100_gemini_v1.py`, commit `6da9d37`. Report: output terminale VPS, nessun manifest creato. Risultato: test offline 2/2; `gemini-3.6-flash` HTTP 503 dopo circa 16 secondi. Nessun PDF, estratto o output RAG inviato. Decisione: non ritentare subito 3.6; abilitare come differenza tecnica un solo fallback stabile `gemini-3.1-flash-lite`, con output distinto. Stato: BLOCCATO sul 3.6; fallback DA FARE.

Attività: predisporre il trasporto asincrono raccomandato dalla documentazione ufficiale per evitare il blocco del canale sincrono. Script: `scripts/coverciano_100_gemini_batch_v1.py`. Commit: DA FARE. Report: `docs/coverciano-100-gemini-benchmark-01.md`. Risultato: submit Batch inline sotto 20 MB, job name persistito, status separato e materializzazione del manifest sottoposta agli stessi gate 100/100, categorie, ID, duplicati e rubriche. Decisione: inviare il job una sola volta; la creazione non e idempotente; monitorare fino a stato terminale senza duplicare submission. Stato: IMPLEMENTATO; submission DA FARE.

Attività: superare senza billing il 503 della richiesta monolitica. Script: `scripts/generate_coverciano_100_chunked_gemini_v1.py`. Commit: DA FARE. Risultato: dieci richieste riprendibili da dieci domande, una categoria per file, tetto output ridotto e merge finale sottoposto al validatore 100/100; nessuna richiesta eseguita. Decisione: collaudare una sola categoria; proseguire le altre solo se il payload ridotto viene accettato, senza sovrascrivere output. Stato: IMPLEMENTATO; runtime DA FARE.

Attività: esecuzione incrementale gratuita. Script: `generate_coverciano_100_chunked_gemini_v1.py`, commit `2e32f0a`. Report runtime VPS: directory `evaluation/coverciano-100-chunks-v1/`. Risultato: tre blocchi validi, 30 domande totali (`costruzione`, `sviluppo_rifinitura`, `transizione_positiva`); il quarto blocco `transizione_negativa` ha ricevuto HTTP 503 sia su 3.6 sia sul fallback 3.1. Decisione: preservare i tre file, nessun retry immediato; heartbeat `completa-100-domande-gemini` ogni 30 minuti genera solo categorie mancanti e fa merge al completamento. Stato: ESEGUITO 30/100; non VALIDATO come manifest completo.

Attività: ridurre ulteriormente la dimensione di risposta sulla base delle metriche AI Studio fornite dal titolare, che escludono saturazione RPM/TPM/RPD. Script: `generate_coverciano_100_chunked_gemini_v1.py`. Commit: DA FARE. Risultato: supporto parti 1/2 da cinque domande e merge categoria 5+5 con verifica ID; i tre blocchi completi restano invariati. Decisione: usare parti da cinque soltanto per categorie mancanti e non attribuire i 503 a quota esaurita. Stato: IMPLEMENTATO; runtime DA FARE.

Attività: collaudo runtime 5+5 su `transizione_negativa`. Script: `generate_coverciano_100_chunked_gemini_v1.py`, commit `9e91790`. Report: due file parte e blocco categoria nella directory runtime VPS. Risultato: parte 1 e parte 2 ESEGUITE, merge 10/10 valido; totale serie 40/100. Il tentativo immediatamente successivo `pressing` parte 1 ha ricevuto 503. Decisione: ipotesi dimensione confermata come fattore rilevante, ma persiste capacita intermittente; proseguire con heartbeat/backoff e parti da cinque. Stato: VALIDATO per strategia 5+5; benchmark completo DA FARE.

Attività: gestire output JSON incompleto ricevuto da Gemini su `pressing` parte 1. Script: `generate_coverciano_100_chunked_gemini_v1.py`. Commit: DA FARE. Risultato: nessun file risultato salvato dal tentativo malformato; aggiunti `responseSchema` obbligatorio, temperatura 0.5, tetto 10000 e diagnostica senza testo (hash, lunghezza, finish reason, errore). Decisione: una nuova esecuzione e giustificata dalla differenza tecnica; non alterare i 40 casi validi. Stato: IMPLEMENTATO; runtime DA FARE.

### V5-GROQ-01 — Proposta revisore esterno Groq Free (2026-10-25)
Attivita: documentare alternativa gratuita senza interferire con Gemini o benchmark Coverciano in corso. Script: nessuna implementazione nel repository; simulazione Python esterna su struttura JSON e aritmetica quote. Commit: `0e8b369` proposta, `257a9a2` report simulazione. Report: `docs/groq-free-reviewer-proposal-01.md`. Risultato: 5/5 mock con esito previsto (conforme, ID errato, citazione non ammessa, voto fuori range, campo mancante); 100x2850=285000 token, minimo teorico 2 giorni a 200000 TPD. Nessuna chiamata Groq, nessuna chiave, nessuna prova del client reale. Decisione: Codex deve riconciliare stato attuale, realizzare adapter opt-in e test offline distinti; probe live solo previa autorizzazione e chiave privata del titolare. Stato: **ESEGUITO** per simulazione documentale; **DA FARE** per implementazione, test API e integrazione. Non confondere con validazione tattica o certificazione.

Attivita: completare esclusivamente G0/G1 offline della proposta Groq. Script: `scripts/groq_free_reviewer_v1.py`; test `tests/test_groq_free_reviewer_v1.py`. Commit: DA FARE. Report: `docs/groq-free-reviewer-g0-g1-01.md`. Risultato: stato VPS riconciliato a 50/100, Groq runtime assente, servizio RAG attivo; adapter isolato riusa prompt/contratto Gemini senza modificarlo; suite mock 6/6 copre 200, 429, 503, 400/401/403, ID, score/verdetto, citazioni, quote e ripresa; API_REQUESTS=0. Decisione: chiudere G0/G1; nessuna chiave, API, deploy o integrazione prima di autorizzazione G2/G3. Stato: **VALIDATO offline**; non ESEGUITO live, INTEGRATO o CERTIFICATO.

Attivita: probe minima Groq autorizzata dal titolare con chiave fornita in chat. Script: richiesta diretta OpenAI-compatible con solo testo `Rispondi esclusivamente con OK`; nessun dato RAG. Report: appendice `docs/groq-free-reviewer-g0-g1-01.md`. Risultato: primo tentativo rifiutato per JSON alterato dall'escaping, senza inferenza; richiesta corretta a `openai/gpt-oss-120b` riuscita con completion ID, 78 prompt token, 16 completion di cui 14 reasoning, 94 totali, queue 0,208 s e model time 0,036 s, nessun errore. Contenuto finale vuoto per limite token minimo. Decisione: considerare ESEGUITA solo connettivita/autenticazione/usage; non validare structured output o qualita; nessun deploy e nessuna persistenza chiave. Revocare la chiave esposta prima di ulteriori prove. Stato: **ESEGUITO**; G4 e integrazione DA FARE.

Attivita: validare Structured Output e percorso completo dell'adapter Groq su dati sintetici. Script: `scripts/groq_free_reviewer_v1.py`; test `tests/test_groq_free_reviewer_v1.py`. Commit: `01b87d8` diagnostica HTTP redatta, `bfc775c` User-Agent esplicito; commit documentale successivo. Report: `docs/groq-free-reviewer-g0-g1-01.md` e proposta aggiornata. Risultato: isolato HTTP 403 Cloudflare 1010 causato dallo User-Agent `urllib`; probe strict equivalente via curl HTTP 200; dopo correzione, caso sintetico completo HTTP 200 in 1,628 s, 816 token prompt, 638 completion (488 reasoning), 1.454 totali, score 8,5 PASS e output conforme; suite offline 6/6. Nessun dato RAG reale, PDF o segreto inviato. Decisione: G3 VALIDATO per compatibilita tecnica, non per competenza tattica; G4 fermato prima dell'invio finche il titolare non autorizza specificamente domanda, risposta RAG ed estratti. Nessun deploy o modifica a Gemini/pipeline. Stato: **VALIDATO** G3 sintetico; **BLOCCATO** G4 per consenso privacy.

Attivita: eseguire l'unico G4 tattico reale autorizzato riutilizzando il caso congelato `928f9702e19148c3a80e500ebe02fec9`, senza rigenerare RAG. Script: `scripts/groq_free_reviewer_v1.py`; modello `openai/gpt-oss-120b`. Report: `docs/groq-free-reviewer-g4-01.md`; output `evaluation/groq_g4_tactical_case_928f9702_v1.json`. Risultato: HTTP 200, 3,770 s; 3.250 prompt + 1.544 completion (1.160 reasoning) = 4.794 token; voto 5,8/10 REVISIONE. Groq individua utilmente l'assenza della corsa diagonale interna e la genericita delle fonti, ma segnala erroneamente mancata corrispondenza di F4/F5: gli ID dichiarati `1,2,4,5` corrispondono esattamente a F1,F2,F4,F5. Confronto con giudizio esterno comunicato dal titolare: 7,5/10, scarto -1,7. Nessun PDF, credenziale, indice o dato ulteriore inviato; chiave rimossa dalla memoria e temporanei VPS cancellati. Decisione: non promuovere Groq a giudice automatico sulla base del singolo campione; G4 ESEGUITO ma affidabilita generale NON VALIDATA. Vietati altri test, integrazione e deploy senza nuova autorizzazione; revocare la chiave esposta. Stato: **ESEGUITO**.

### V5-GROQ-02 — Completamento Coverciano e copilot tattico, Fase A (2026-10-26)

Attivita: sostituire Gemini con Groq nei due ruoli decisi dal titolare, preservando le 50 domande Gemini valide: completamento delle 50 mancanti e seconda AI propositiva del RAG. Script: `scripts/generate_coverciano_100_groq_completion_v1.py`, `scripts/groq_tactical_copilot_v2.py`; test omonimi. Commit: `7596ba4`, `f03b66d`, `9031661`, `2d034c7`; report `docs/groq-coverciano-completion-copilot-phase-a-01.md`. Risultato: inventario VPS 50/100 con cinque categorie complete e cinque mancanti; suite combinata 10/10, compilazione PASS, preflight generatore e copilot PASS, API_REQUESTS=0. Generatore preserva schema/rubriche/ID, produce solo parti mancanti, rileva quasi-duplicati, non sovrascrive e applica hard stop Free Tier; copilot separa revisione tattica senza fonti da verifica documentale e demanda al software la validita delle label. Heartbeat Gemini eliminato per impedire doppia generazione. Decisione: Fase A chiusa; attendere autorizzazione per 10 chiamate di generazione (budget pianificato 75.000 token) e autorizzazione separata per 3 casi differenziali/6 chiamate. Nessun deploy, risposta RAG o modifica alla pipeline. Stato: **VALIDATO offline**; generazione e copilot live **DA FARE**.

### V5-COV-RESET-01 — Correzione del protocollo d'esame (2026-10-26)

Attivita: riconciliare l'intento originario dopo aver rilevato che la campagna
50/100 aveva assegnato a Gemini il ruolo sbagliato. Script: nessuna inferenza;
audit TODO, registro, report, commit e inventario VPS. Commit: DA FARE. Report:
`docs/coverciano-examiner-copilot-reset-01.md`. Risultato: il flusso corretto è
Gemini Cloud esaminatore e valutatore, RAG candidato documentale, Groq spalla
tattica con verifica separata delle evidenze. I 50 casi batch e il completamento
Groq sono fuori perimetro. Una singola prova manuale sul 4-3-3 contro pressione
alta a uomo ha trasformato una risposta RAG generica in una risposta valutata
30/30 con lode; job RAG `ad41e872d5f44a66a7626f8429f30e5e`, circa 170 s.
Decisione: registrare la prova come ESEGUITA ma non VALIDATA, eliminare soltanto
la directory runtime dei 50 casi, ottimizzare prima la latenza e solo dopo
congelare il nuovo benchmark. Stato: **ESEGUITO** per riconciliazione e prova;
pulizia e ottimizzazione **DA FARE**.

Attivita: rimuovere dalla VPS soltanto gli artefatti del protocollo batch
annullato. Script: shell fail-closed con `readlink -f`, confronto del percorso,
conteggio, dimensione e verifica post-rimozione. Commit decisionale: `ab837fd`.
Report: `docs/coverciano-examiner-copilot-reset-01.md`. Risultato: percorso
`/opt/football-data-lab/projects/tactical-engine/evaluation/coverciano-100-chunks-v1`,
9 file, 156 KB; directory assente dopo la rimozione. Nessun altro report,
indice o PDF incluso nel target. Decisione: chiudere il vecchio avanzamento
50/100 e ripartire da zero soltanto dopo il nuovo protocollo congelato. Stato:
**VALIDATO** per la pulizia mirata.

### V5-PERF-INTERACTIVE-01 — Profilo generativo interattivo (2026-10-26)

Attivita: isolare il collo di bottiglia del ciclo Coverciano senza ripetere
inferenze equivalenti. Script: lettura del job esistente e dei due report
prestazionali; opzioni applicative in `smoke_test_rag_v5_e2e.py`,
`run_rag_v5_query.py` e `rag_v5_api.py`. Commit: DA FARE. Report:
`docs/rag-v5-interactive-performance-01.md`. Risultato: 165,92 dei 173,34 s
sono dentro Ollama; 75,90 s prompt, 79,58 s output e 10,40 s load. Implementato
profilo opt-in con modello, contesto e keep-alive configurabili; default locked
invariati; compilazione PASS e suite API 17/17. Decisione: collaudare una sola
volta `qwen3.5:4b`, contesto 4096, massimo 450 token, sei evidenze e keep-alive
30m; la differenza di modello/parametri giustifica il test. Stato:
**IMPLEMENTATO**; runtime **DA FARE**.

Attivita: collaudare il profilo 4B senza alterare locked o collection. Script:
`run_rag_v5_query.py`, report runtime separati
`api-runs/perf4b_ad41e872_v1.result.json` e V2. Commit: `080bba4`. Report:
`docs/rag-v5-interactive-performance-01.md`. Risultato: V1 87,64 s, completa
ma tatticamente insufficiente; V2 con quattro evidenze e 300 token 31,59 s,
ma `done_reason=length`, risposta incompleta e ruoli errati. Entrambe con zero
citazioni invalide e collection 6410 invariata. Decisione: non promuovere il
4B; rimuoverlo dalla VPS e recuperare 3,3 GB, disco finale 32%. Conservare le
opzioni reversibili e proseguire sul copilot Groq con composizione controllata.
Stato: **ESEGUITO**, non `VALIDATO` o `INTEGRATO`.

### V5-GROQ-COPILOT-03 — Composizione controllata e pannello (2026-10-26)

Attivita: trasformare il prototipo Groq in spalla tattica applicativa senza
toccare locked, collection o risposta RAG originale. Script:
`groq_tactical_copilot_v2.py`, `rag_v5_api.py`, `knowledge_panel.html`; test
copilot e API. Commit: DA FARE. Report:
`docs/groq-copilot-panel-integration-01.md`. Risultato: due passaggi, finding
supportati/irrisolti, composizione finale con citazioni ammesse e fallback non
bloccante; pannello ridisegnato con quattro fasi, risposta finale, bozza e fonti.
Compilazione e sintassi JavaScript PASS, suite 25/25. Decisione: pubblicare il
codice con flag disattivo; attivazione soltanto dopo configurazione privata
della chiave e una smoke live. Stato: **IMPLEMENTATO**, non ancora `ESEGUITO`,
`VALIDATO` o `INTEGRATO` live.

Attivita: pubblicare e collaudare la nuova interfaccia senza attivare il
copilot esterno. Script: `api/knowledge_panel.html`, API e test gia descritti;
commit `a77420e`. Report: `docs/groq-copilot-panel-integration-01.md`.
Risultato: pull VPS, suite 25/25, servizio active, `/healthz`, `/readyz` e
pagina HTTPS pubblica HTTP 200; albero accessibile e verifica visiva confermano
guida, autenticazione, quattro fasi, risposta finale, bozza, evidenze,
diagnostica e biblioteca. Decisione: chiudere la riprogettazione UI come
**VALIDATA e INTEGRATA**; mantenere separato il copilot Groq, ancora
**IMPLEMENTATO** e disattivato in assenza di configurazione privata e smoke
live. Nessuna estensione della certificazione locked.

### V5-FIGC-PANEL-01 — Stati monitor FIGC nel pannello (2026-10-26)

Attivita: integrare il catalogo del monitor nella UI senza confondere download
e indicizzazione. Script: `api/knowledge_catalog.py`, `api/rag_v5_api.py`,
`api/knowledge_panel.html`; test catalogo/API. Commit: DA FARE. Report:
`docs/figc-catalog-panel-integration-01.md`. Risultato: proiezione read-only
senza percorsi locali, endpoint autenticato e tabella separata; suite 25/25,
compilazione e sintassi JavaScript PASS. Decisione: pubblicare e verificare sul
catalogo VPS reale; nessuna ingestion o scrittura Chroma. Stato:
**IMPLEMENTATO**; runtime **DA FARE**.

Attivita: verifica runtime distinta dell'integrazione FIGC. Script e commit:
`5b55967`. Report: `docs/figc-catalog-panel-integration-01.md`. Risultato: VPS
25/25, servizio active, endpoint autenticato con schema corretto, 10 documenti,
zero errori e nessun percorso privato; sezione pubblica “Monitor FIGC” presente
nell'albero accessibile. Decisione: chiudere la vista come **VALIDATA e
INTEGRATA**; non confondere lo stato UI con conversione o ingestion automatica,
che restano processi separati.

### V5-FIGC-REVIEW-02 — Review match analysis (2026-10-26)

Attivita: revisione editoriale read-only di Di Camillo, Rausse e Venturini.
Script: `apply_figc_editorial_decisions_v1.py`; decisioni:
`docs/figc-match-analysis-decisions-v1.json`. Commit: DA FARE. Report:
`docs/figc-match-analysis-editorial-review-01.md`. Risultato: Di Camillo e
Rausse candidati tattici; Venturini escluso dal RAG tattico perché focalizzato
su analytics/metriche. Rilevato inoltre catalogo Venturini stale: stato
downloaded ma file locale assente, URL FIGC ancora accessibile. Test atomico
3/3 e compilazione PASS. Decisione: pubblicare, applicare le tre decisioni al
catalogo VPS senza ingestion e conservare separata l'anomalia file. Stato:
**IMPLEMENTATO** per applicatore, review **ESEGUITA**, runtime **DA FARE**.

Attivita: applicazione runtime delle tre decisioni con backup del catalogo e
successiva esposizione nel pannello. Commit base `48ef114`; commit UI: DA FARE.
Risultato: aggiornamento 3/3 per SHA-256, Di Camillo/Rausse candidati tattici e
Venturini escluso; suite 25/25 e sintassi JavaScript PASS. Decisione: chiudere
la review come **VALIDATA**; nessuna indicizzazione inclusa.

### VPS-CLEAN-02 — Archivio artefatti runtime (2026-10-26)

Attivita: riconciliare 122 file runtime non tracciati senza perdere evidenze.
Report: `docs/vps-runtime-artifact-cleanup-01.md`. Risultato: 3.409.525 byte
compressi in archivio verificato da 692.765 byte con manifest per file e
SHA-256 archivio `f32263a...e5fd`; checkout VPS pulito. Decisione: conservare
l'archivio recuperabile fuori dal checkout; nessuna modifica a Git, PDF,
collection o output API corrente. Stato: **VALIDATO**.

### V5-FIGC-RECONCILE-03 — Duplicazione candidata evitata (2026-10-26)

Attivita: costruire una candidata isolata per Di Camillo e Rausse. Il dry-run
ha prodotto 33+58=91 chunk; in scrittura il gate fail-closed ha rilevato un ID
esistente con metadata differente prima di qualunque nuovo inserimento.
L'ispezione esatta della baseline ha confermato entrambi i documenti già
integrati nella FIGC5 (33 e 58 chunk). Risultato: candidata parziale contenente
soltanto la baseline 6410 rimossa insieme alla copia temporanea; collection
operativa invariata a 6410. Decisione: correggere catalogo e pannello da
`candidate_tactical` a `integrated_tactical`; nessuna regressione necessaria
perché non è cambiato alcun indice. Stato: **VALIDATO**.

### V5-GROQ-LIVE-04 — Prima smoke applicativa (2026-10-26)

Attivita: attivare il copilot privato e verificare API → RAG → Groq. Job
`0edcc041b11c405f80d389a92b84fda4`. Risultato: RAG 151,76 s, sei evidenze,
zero citazioni invalide; copilot `unavailable`, fallback corretto e bozza RAG
preservata. Il vecchio client non ha persistito il motivo redatto. Correzione:
report fallimento con soli codici HTTP/rete/timeout/schema, senza contenuti o
segreti; test 27/27. Decisione: pubblicare la diagnostica, non ripetere la
chiamata senza nuova autorizzazione esplicita. Stato: smoke **ESEGUITA**,
copilot live **BLOCCATO**, diagnostica **IMPLEMENTATA**.

### V5-OPENROUTER-QUALITY-02 — Contesto preservato (2026-10-26)

Attività: seconda prova differenziale dal pannello sul caso Coverciano 001,
job `8de1cbcc`. Risultato: RAG 73,3 s, OpenRouter 15,701 s, totale 113 s,
5.155 token, costo $0,02551, stato `verified`; valutazione Gemini **25/30**.
Decisione: miglioramento reale rispetto a 18/30, ma risposta ancora diagnostica
e non proattiva; omessi tre cambi/due slot. Implementare risposta sostitutiva
completa nei due passaggi e ripetere una sola volta. Stato: **ESEGUITO**.

### V5-OPENROUTER-QUALITY-03 — Risposta sostitutiva (2026-10-26)

Attività: job pannello `08f5015c` con risposta sostitutiva obbligatoria.
Risultato: RAG 128,27 s, revisore 18,993 s, totale 170 s; 5.505 token, costo
$0,0290325; voto interno 3/10. Errori: lato invertito, ruolo inesistente e cambi
generici. Decisione: non inviare a Gemini; introdurre mappa geometrica e distinta
N cambi/M slot, quindi usare `openai/gpt-6.1-sol` come primario. Stato:
**ESEGUITO**, non VALIDATO.

### V5-OPENROUTER-QUALITY-04 — Root cause adapter PASS2 (2026-10-26)

Attività: job pannello `6d5e64b6`. Risultato: 117 s totali, 6.125 token,
$0,032585, fallback GPT-4o, voto interno 2/10. Causa verificata: override
OpenRouter di PASS2 ometteva domanda, bozza, risposta sostitutiva e piano;
`temperature` rendeva GPT-6.1 non eleggibile col gate parametri. Decisione:
correggere payload e usare reasoning high senza temperatura; nuova prova
giustificata, nessun invio Gemini dell'output respinto. Stato: **ESEGUITO**.

### V5-OPENROUTER-QUALITY-05 — Timeout reasoning high (2026-10-26)

Attività: job pannello `24ae6aba` con payload PASS2 completo e GPT-6.1 Sol.
Risultato: RAG 71,39 s; timeout revisore 240 s; totale 334 s e fallback sulla
bozza. Usage locale assente per completion non conclusa. Decisione: ridurre
reasoning a low e riconciliare il costo tramite telemetria OpenRouter; nessun
invio Gemini. Stato: **ESEGUITO**.

### V5-RAG-COPILOT-ATTRIBUTION-01 — Audit preliminare 70/30 (2026-10-26)

Attivita: riconciliare il ruolo effettivo di RAG e spalla OpenRouter nelle
prime 16 prove Coverciano eseguite dal pannello, senza nuove chiamate. Evidenze:
bozze RAG e revisioni conservate nella cronologia della sessione, valutazioni
interne frequentemente comprese fra 2 e 4/10 nei casi recenti, risposte finali
valutate dalla commissione esterna 29-30/30 nei primi 15 casi; valutazione del
caso 16 ancora pendente. Risultato: stima qualitativa preliminare RAG 25-35% e
spalla 65-75%; il retrieval e il grounding restano prevalentemente RAG, mentre
la maggioranza del miglioramento di ragionamento ed esposizione proviene oggi
dalla spalla. Decisione: obiettivo RAG >=70%, spalla <=30% e bozza autonoma
>=26/30; progettare attribuzione per caso sui concetti preservati, corretti,
aggiunti e non supportati prima di dichiarare una percentuale validata. Vietata
la sostituzione integrale della risposta da parte del revisore. Stato:
**ESEGUITO** per l'audit preliminare; misura causale **DA FARE**, non VALIDATA.

### V5-COVERCIANO-RAG-AUTONOMY-AUDIT-01 — Stop e diagnosi (2026-10-26)

Attivita: sospendere il benchmark e analizzare senza nuove chiamate le prime 16
prove conservate nella sessione del pannello, il runner, il prompt RAG e i due
passaggi OpenRouter. Report:
`docs/v5-coverciano-rag-autonomy-audit-01.md`. Risultato: 15/16 bozze a 2-4/10,
media interna 3,06/10, mediana 2/10; risposta finale mediamente 2,87x piu
lunga. Accertato che il copilot richiede una `replacement_answer` e la usa come
ossatura per una riscrittura integrale. Retrieval e generazione non impongono
una mappa strutturale generale; i gate API controllano citazioni sintattiche e
indice, non coerenza tattica. Il voto nominale 28/30 della prova 16 e INVALIDO:
dopo perdita della sessione e stato trasmesso il segnaposto `Connettiti per
iniziare`, dal quale la commissione ha inferito impropriamente un giudizio usando
la cronologia. Decisione: non usare domanda 17, non proseguire il benchmark;
implementare parser/gate strutturale, retrieval per sottoproblemi, spalla
delta-only e gate autonomia su tre casi congelati. Stato: **ESEGUITO** per
l'audit; correzioni **DA FARE**, benchmark sospeso.

Decisione aggiuntiva del titolare: la perdita della sessione dimostra che
persistenza e tracciamento devono diventare un requisito tecnico autonomo.
Attivita `V5-PANEL-PERSISTENT-HISTORY-01` aperta nel TODO: storico server-side,
ripresa sicura, associazione caso/job, blocco dei placeholder ed export
cumulativo. Stato: **DA FARE**; nessuna implementazione o test eseguito.

### V5-COVERCIANO-RAG-ONLY-100-01 — Baseline autonoma ridotta a 10 casi (2026-10-26)

Attivita: eseguire dal pannello il flusso Gemini Cloud esaminatore → RAG-only →
Gemini Cloud valutatore, con risposta RAG invariata e spalla OpenRouter
disabilitata. Il titolare ha ridotto esplicitamente il perimetro da 100 a 10 e
richiesto l'arresto esatto al caso 10. Script: pannello pubblico e pipeline API
gia integrata; nessuna modifica alla pipeline durante la baseline. Commit:
DA FARE. Report: `docs/coverciano-rag-only-100-report-01.md`. Risultato: 10/10
job `succeeded`, 199/300, media 19,90/30, mediana 21,50, minimo 0 e massimo 26;
tempo RAG totale 1.512,17 s, media 151,22 s; 5.506 token complessivi. Caso 9:
retrieval di sole due evidenze generiche e risposta completamente astensiva,
voto 0/30. Decisione: target autonomo >=26/30 respinto; non continuare oltre
10 e non riattivare la spalla per compensare. Aprire remediation su parsing dei
sottoproblemi, retrieval per fase/ruolo, gate di copertura, risposta applicativa
e normalizzazione terminologica; ripetere soltanto dopo una differenza tecnica
documentata. Stato: **ESEGUITO**, non **VALIDATO**.


### V5-REVISIONE-DOMANDE-01 — 2026-10-28

Attività: raccolta diagnostica di due trascrizioni d'esame e confronto con TODO, registro e report routing/V9/V10. Script: nessuno nuovo, sola lettura. Commit: quello che introduce `docs/revisione_domande.md` e questa voce insieme al TODO. Report: `docs/revisione_domande.md`. Risultato: RD-001 19/30 e RD-002 22/30, scenari distinti; perdita di aderenza e contaminazione tra fasi osservabili, causa retrieval/prompt/modello/deploy ancora da isolare. Il salto 29–30 dopo rettifica resta un comportamento riferito senza coppia comparabile acquisita. Decisione: riusare job e fonti esistenti, identificare versione runtime e verificare le correzioni V6–V10.2 prima di nuovi interventi. Nessuna nuova chiamata RAG/valutatore, test equivalente o modifica applicativa. Stato: **ESEGUITO** per revisione documentale; diagnosi causale **DA FARE**.


### V5-REVISIONE-DOMANDE-01 — RD-002-R1 (2026-10-28)
Attività: analizzare il seguito del 22/30 fornito in chat. Script: nessuno nuovo. Commit: quello che aggiorna insieme report/TODO/registro con RD-002-R1. Report: `docs/revisione_domande.md`. Risultato: risposta RAG limitata alle definizioni F1/F2; applicazione allo scenario scritta da Gemini prima del voto 30/30. Decisione: non usare quel voto come salto autonomo 22→30; acquisire input effettivo, contesto conversazionale ed estratti dei due turni. Stato: **ESEGUITO** per analisi documentale; causa tecnica **DA FARE**. Nessuna nuova inferenza o modifica runtime.


### V5-REVISIONE-DOMANDE-01 — RD-003 e conferma RD-002-R1 (2026-10-28)
Attività: confronto documentale di risposta/correzione 4-3-3 contro blocco basso e ulteriore giustificazione del 30 precedente. Script: nessuno nuovo. Commit: aggiornamento contestuale report/TODO/registro. Report: `docs/revisione_domande.md`. Risultato: 21→29/30 dichiarati dal valutatore; terminologia migliorata ma preventive centrali/play e applicazione dei cinque offensivi non sviluppate. Conferma RD-002 miscela 19 e 22/30 e premia forma senza colmare omissioni. Decisione: non utilizzare i voti alti come prova causale di autonomia; acquisire gli artefatti esistenti e stabilizzare rubrica/attribuzione, confrontando V6–V10.2. Stato: **ESEGUITO** per revisione; diagnosi tecnica **DA FARE**. Nessuna inferenza o modifica applicativa.


### RD-THINK-01 — 2026-10-28
Attività: verificare richiesta utente su thinking Qwen. Script: lettura runner smoke_test_rag_v5_e2e.py, wrapper query e API. Commit: aggiornamento documentale corrente. Report: `docs/revisione_domande.md`. Risultato: `think: False` esplicito nel payload iniziale e repair, anche main; documentazione ufficiale Ollama distingue modalità e visualizzazione. Decisione: priorità a confronto controllato off/on con contesto congelato e budget adeguato, previa verifica supporto locale; non attribuire causalità senza esito. Stato: **ESEGUITO** per verifica statica; runtime/causalità **DA FARE**. Nessuna nuova inferenza, patch o deploy.

### RD-THINK-01 — confronto runtime isolato (2026-10-28)

Attività: verificare modello/digest e memoria del pannello, quindi confrontare
thinking off/on senza rieseguire retrieval. Script:
`scripts/compare_frozen_thinking_rd01.py`. Commit: commit contestuale.
Report: `docs/rd-think-01-runtime-01.md`; artefatto completo:
`evaluation/rd-think-01-result.json`. Risultato: off termina naturalmente in
204,932 s con 647 token e 348 parole; on esaurisce 4096 token di thinking in
546,484 s senza output, e il repair replica l'esito in 552,773 s. La risposta
off passa il gate ma contiene trasformazioni 4-3-3→3-5-2 contraddittorie:
falso positivo sostanziale. Il pannello non invia cronologia ai nuovi job.
Decisione: mantenere `think:false`; aprire controlli relazionali e gestione
esplicita del contesto follow-up, senza deploy o nuova campagna. Stato:
**ESEGUITO**, qualità >=26/30 non VALIDATA.
### RD-TSC-V1-GITHUB-EVIDENCE-01 — prima patch deterministica (2026-10-28)

Attività: implementare e pubblicare separatamente il Tactical State Contract v1
deterministico, senza generazione, API o deploy. Script:
`scripts/v5_tactical_state_contract_v1.py`; ingresso riutilizzato
`scripts/v5_tactical_query_plan_v1.py::analyse`; test
`tests/test_v5_tactical_state_contract_v1.py` e regressione planner esistente.
Commit implementazione/test: `c1c2b233f048873368b94900dad779cf14649679`;
report `docs/tactical-state-contract-v1-deterministic-01.md`. Risultato: 17/17
test nuovi e 18/18 storici PASS, `py_compile` e `git diff --check` PASS; nessuna
chiamata Qwen/Ollama o servizio esterno. Sono distinti attori, ruoli, slot e
candidati, con provenienza, eventi, fasi, cardinalità, invarianti relazionali,
normalizzazioni conservative, errori classificati e rendering qualificato.
Decisione: sottoporre lo stesso commit GitHub a revisione indipendente; seconda
patch generativa DA FARE soltanto dopo nuova autorizzazione. Stato: **VALIDATO**
offline per la componente deterministica; non INTEGRATO o CERTIFICATO.

Attività distinta: la verifica statica del feedback conferma che i file
`*.feedback.json` alimentano metriche aggregate, ma un job recuperato dopo riavvio
non è accettato da `record_feedback()` e il feedback individuale non è caricato da
`persisted_job()`. Decisione: registrare `RD-FEEDBACK-RECOVERY-01` nel TODO senza
modificare feedback in questa patch. Stato: **DA FARE**.

### RD-TSC-V1-RELATIONAL-CORRECTION-01 — correzione deterministica (2026-10-28)

Attività: recepire le lacune relazionali emerse nel confronto tecnico
Codex–ChatGPT sulla prima patch, distinguendo il confronto fra colleghi
dall'autorizzazione operativa del titolare. Script:
`scripts/v5_tactical_state_contract_v1.py`; test
`tests/test_v5_tactical_state_contract_v1.py`; regressione storica
`tests/test_v5_tactical_query_plan_v1.py`. Commit codice/test `947e667`; report
`docs/tactical-state-contract-v1-relational-correction-01.md`. Risultato: presenza
autorevole per stato, ordine parziale aciclico, riferimenti concreti separati dai
mapping astratti, controllo di sostituzioni/rotazioni/espulsioni e cardinalità,
continuità completa quando dichiarata, provenienza ricorsiva e rendering che
omette eventi bloccati. Suite 41/41 e 18/18 PASS, compilazione e diff check PASS;
zero chiamate esterne. Decisione: pubblicare sul ramo dedicato per nuova revisione
condivisa; nessuna seconda patch, merge o deploy. Stato: **IMPLEMENTATO** per il
codice, **ESEGUITO** per i test, **VALIDATO** offline per gli invarianti coperti e
l'isolamento; non INTEGRATO o CERTIFICATO.

### RD-TSC-V1-CONSOLIDATED-REMEDIATION-01 — chiusura differenziale (2026-10-28)

Attività: verificare e correggere esclusivamente sette condizioni relazionali
non coperte dalla suite precedente. Script:
`scripts/v5_tactical_state_contract_v1.py`; test:
`tests/test_v5_tactical_state_contract_v1.py`; regressione planner esistente.
Commit codice/test: `0d69be6`; report:
`docs/tactical-state-contract-v1-consolidated-remediation-01.md`. Risultato:
delta aggregato per espulsioni multiple, rientro basato sul grafo temporale,
rendering che omette eventi dipendenti da blocchi globali o di transizione,
registrazione sicura dei numeri nudi, archi invalidi strutturati, verifica della
presenza completa e continuità fra mapping e assegnazioni concrete. Contratto
48/48, planner storico 18/18, compilazione e diff check PASS; zero chiamate
esterne. Decisione: chiudere `RD-RELATION-01` sul solo perimetro deterministico
offline e procedere separatamente con l'audit tattico relazionale non
bloccante. Stato: **IMPLEMENTATO** codice, **ESEGUITO** test, **VALIDATO**
offline; non **INTEGRATO** o **CERTIFICATO**.

### RD-TACTICAL-RELATIONAL-AUDIT-01 — audit offline non bloccante (2026-10-28)

Attività: distinguere copertura lessicale e relazione tattica per
sottoproblema senza riattivare il blocco globale. Script:
`scripts/v5_tactical_query_plan_v1.py`; test:
`tests/test_v5_tactical_query_plan_v1.py`. Commit codice/test `b4a5f64`;
report `docs/tactical-relational-audit-offline-01.md`. Risultato: segnali
clause-local per attore, fase, compito, spazio, trigger e finalità; diagnosi di
attore/fase errati, omissioni indipendenti e citazioni formalmente valide ma
non pertinenti. Sette test differenziali nuovi; planner/audit 25/25, contratto
48/48, compilazione e diff check PASS. Il supporto semantico documentale non
viene dichiarato verificato e l'esito non modifica `complete`. Decisione:
mantenere l'audit offline e non bloccante; richiedere casi indipendenti completi
prima dell'integrazione. Stato: **IMPLEMENTATO**, **ESEGUITO**, **VALIDATO**
offline per il comportamento coperto; non **INTEGRATO** o **CERTIFICATO**.

### RD-FEEDBACK-RECOVERY-01 — feedback dei job persistiti (2026-10-28)

Attività: consentire raccolta e consultazione del feedback dopo riavvio senza
creare un secondo archivio. Script: `api/rag_v5_api.py`; test:
`tests/test_rag_v5_api.py`. Commit codice/test `8102eb1`; report:
`docs/feedback-recovery-01.md`. Risultato: recupero del job persistito prima
della validazione dello stato, associazione del sidecar al job live o
ricostruito, verifica schema/job/tipo, scrittura atomica e singolo voto corrente
per job. Casi riuscito, fallito, inesistente/mismatch e aggiornamento coperti;
suite API 28/28, compilazione e diff check PASS. Decisione: chiudere il difetto
offline preservando `/v1/feedback` e `rag_api_feedback_v1`; non equiparare il
feedback a diagnosi o apprendimento. Stato: **IMPLEMENTATO**, **ESEGUITO**,
**VALIDATO** offline; non distribuito, quindi non **INTEGRATO** in produzione o
**CERTIFICATO**.

### RD-SESSION-01 / V5-PANEL-PERSISTENT-HISTORY-01 — backend isolato (2026-10-28)

Attività: implementare un solo contratto backend per contesto confermato e
ricostruzione della cronologia, senza modificare il pannello. Script:
`api/rag_v5_api.py`; test `tests/test_rag_v5_api.py`. Commit codice/test
`863a943`; report `docs/api-session-context-history-01.md`. Risultato: payload
legacy invariato; estensione opzionale con sessione/caso, fatti confermati e
riferimenti a soli job riusciti; domanda originale ed effettiva entrambe
persistite; nessuna risposta generata promossa a fatto; sessione ricostruita dai
sidecar esistenti dopo riavvio. Suite API 32/32, compilazione e diff check PASS.
Decisione: validare offline il backend e mantenere UI/deploy separati. Stato:
supporto API **IMPLEMENTATO**, test **ESEGUITO**, recovery e retrocompatibilità
**VALIDATO** offline; collegamento al pannello **DA FARE**, non **INTEGRATO** in
produzione o **CERTIFICATO**.

### RD-CONSOLIDATED-REMEDIATION-20261028 — regressione finale (2026-10-28)

Attività: eseguire esclusivamente le regressioni pertinenti dopo le quattro
correzioni isolate. Script/test: contratto relazionale, planner/audit e API.
Report: `docs/consolidated-remediation-2026-10-28.md`. Risultato: 48/48 test
contratto, 25/25 planner/audit e 32/32 API, totale 105/105 PASS; compilazione dei
tre moduli e diff check PASS. Nessuna chiamata esterna, modifica al pannello,
VPS, indice, corpus, modello, merge o deploy. Decisione: considerare validate
offline le sole proprietà coperte e preservare come aperte integrazione Qwen,
UI, validazione runtime indipendente e decisione di distribuzione. Stato:
regressione **ESEGUITO**, perimetro offline **VALIDATO**; nuovi componenti non
**INTEGRATI** o **CERTIFICATI**.

### RD-SECOND-PEER-REVIEW-DIFFERENTIAL-01 — seconda revisione (2026-10-28)

Attività: verificare criticamente e correggere soltanto le lacune differenziali
segnalate nella seconda revisione paritaria del commit `ebc6722`. Script:
`scripts/v5_tactical_query_plan_v1.py`,
`scripts/v5_tactical_state_contract_v1.py`, `api/rag_v5_api.py`; relativi test.
Commit codice/test `d34ad7c`; report:
`docs/second-peer-review-differential-remediation-01.md`. Risultato: relazioni
negate e associazioni fra due attori non sono più promosse; requisiti generici
restano non dimostrati; finestra anaforica limitata; riferimenti job vincolati a
sessione/caso; snapshot paginato metadata-only; provenienza descritta come
dichiarazione del client; feedback concorrente serializzato; mapping concreto
verificato con presenza parziale; rientro non ordinabile qualificato. Nove test
nuovi; planner 29/29, contratto 50/50, API 35/35, totale 114/114 PASS;
compilazione e diff check PASS. HTML e profilo API predefinito invariati.
Decisione: proporre validazione indipendente su casi congelati completi, senza
attivare blocchi o integrazioni automatiche. Stato: **IMPLEMENTATO**,
**ESEGUITO**, **VALIDATO** offline; non **INTEGRATO** o **CERTIFICATO**.

### RD-FOURTH-PEER-RELATIONAL-REMEDIATION-01 — quarta revisione (2026-10-28)

Attività: correggere esclusivamente i controesempi B2/B3/B4, qualificare A2/A3
e separare l'estrazione di requisiti aperti/espliciti dalla loro verifica.
Script: `scripts/v5_tactical_query_plan_v1.py`; test:
`tests/test_v5_tactical_query_plan_v1.py`. Commit codice/test: `6f20bcd`.
Report: `docs/fourth-peer-review-relational-remediation-01.md`. Risultato:
inciso comitativo e soggetto postverbale delimitato riconosciuti; `uno/l'altro`
non attribuito; polarità a quattro stati; sottodomande congelate e compiti
atomici; requisiti aperti verificabili soltanto tramite relazione operativa.
Nove test nuovi, planner/audit 38/38, compilazione e diff check PASS. Le suite
contratto/API non sono state ripetute perché prive di file o dipendenze
modificate. Nessuna chiamata esterna, VPS, inferenza o benchmark. Decisione:
validare offline il solo delta e mantenere audit non bloccante. Gold E/Gold V
sono definiti ma non disponibili: validazione indipendente **BLOCCATO**. Stato:
correzioni **IMPLEMENTATO**, test **ESEGUITO**, perimetro differenziale
**VALIDATO** offline; non **INTEGRATO** o **CERTIFICATO**.

### RD-FIFTH-PEER-RELATIONAL-REMEDIATION-01 — quinta revisione (2026-10-28)

Attività: riprodurre e correggere soltanto i rischi residui su B3, pertinenza
dei requisiti aperti, associazioni atomiche e polarità multipla. Script:
`scripts/v5_tactical_query_plan_v1.py`; test:
`tests/test_v5_tactical_query_plan_v1.py`. Commit codice/test: `b4eb68b`.
Report: `docs/fifth-peer-review-relational-remediation-01.md`. Risultato: B3
postverbale limitato al costrutto esplicito; obiettivo semantico congelato
dalla domanda e osservabile separatamente; coordinazioni `mentre` segmentate
con vincoli locali; polarità mista qualificata `AMBIGUOUS`. Quattro test nuovi,
planner/audit 42/42, compilazione e diff check PASS. Contratto/API non ripetuti
per assenza di dipendenze modificate; nessuna chiamata esterna, VPS, inferenza,
benchmark, merge o deploy. Decisione: validare offline soltanto le proprietà
differenziali, mantenere audit non bloccante e Gold E/Gold V **BLOCCATO**.
Stato: correzioni **IMPLEMENTATO**, test **ESEGUITO**, delta **VALIDATO**
offline; non **INTEGRATO** o **CERTIFICATO**.

### RD-SIXTH-PEER-RELATIONAL-VERIFICATION-01 — sesta verifica (2026-10-28)

Attività: verificare prestito della pertinenza, trasferimento di trigger/fasi e
permissività residua di B3. Script: `scripts/v5_tactical_query_plan_v1.py`;
test: `tests/test_v5_tactical_query_plan_v1.py`. Commit codice/test: `9e63efc`.
Report: `docs/sixth-peer-review-relational-verification-01.md`. Risultato: A
riprodotto in due varianti e corretto con gruppi-obiettivo e ambito attore; B1
riprodotto e corretto dando priorità ai valori locali, preservando la cornice
comune B2; C non riprodotto, quindi nessuna patch al costrutto postverbale.
Quattro test nuovi, planner/audit 46/46, compilazione e diff check PASS.
Contratto/API non ripetuti per assenza di dipendenze modificate; zero chiamate
esterne, VPS, inferenze, benchmark, merge o deploy. Decisione: validare offline
soltanto A/B e registrare C come non riprodotto; Gold E/Gold V resta
**BLOCCATO**. Stato: correzioni **IMPLEMENTATO**, test **ESEGUITO**, delta
**VALIDATO** offline; non **INTEGRATO** o **CERTIFICATO**.

### RD-SEVENTH-PEER-RELATIONAL-VERIFICATION-01 — chiusura differenziale (2026-10-28)

Attività: verificare ambito misto proprio/avversario, co-localizzazione dei
gruppi-obiettivo e aggiornamento della cornice su tre segmenti. Script:
`scripts/v5_tactical_query_plan_v1.py`; test:
`tests/test_v5_tactical_query_plan_v1.py`. Commit codice/test: `084cb5b`.
Report: `docs/seventh-peer-review-relational-verification-01.md`. Risultato: A
positivo era un falso negativo ed è corretto associando ambito e obiettivi a
unità relazionali interne; A negativo resta respinto; B1 e B2 erano già
corretti e restano tali senza sinonimi ad hoc; C corretto con cornice corrente
aggiornata dal trigger locale. Quattro test nuovi, planner/audit 50/50,
compilazione e diff check PASS. Contratto/API non ripetuti perché indipendenti;
zero chiamate esterne, VPS, inferenze, benchmark, merge o deploy. Decisione:
arrestare il ciclo di euristiche costruite e passare alla sola preparazione
indipendente Gold E/Gold V. Stato: correzioni **IMPLEMENTATO**, test
**ESEGUITO**, delta **VALIDATO** offline; audit non **INTEGRATO** o
**CERTIFICATO**, validazione indipendente ancora **BLOCCATO**.

### RD-RELATIONAL-GOLD-E-V-PREPARATION-01 — preparazione metodologica (2026-10-28)

Attività: predisporre senza popolare il processo indipendente Gold E
(estrazione requisiti dalla sola domanda) e Gold V (verifica relazionale su
requisiti umani congelati). Script:
`scripts/validate_relational_gold_preparation_v1.py`; test:
`tests/test_validate_relational_gold_preparation_v1.py`; protocollo:
`docs/relational-gold-e-v-protocol-v1.md`; schemi e template in
`evaluation/annotations/`. Commit tecnico: `6f4579f`. Risultato: schemi
`relational_gold_e_v1`, `relational_gold_v_v1` e manifest v1, template con
zero casi, provenienza/indipendenza, doppia review, adjudication, freeze e
metriche documentati. Validatore `PREPARATION_VALID`, 5/5 test, compilazione e
diff check PASS. Nessun caso generato o annotato, modello, benchmark, modifica
al motore, merge, deploy o VPS. Decisione: preparazione metodologica
**VALIDATO offline**; raccolta/annotazione/freeze **DA FARE** e validazione
indipendente `RD-RELATIONAL-GOLD-E-V-01` ancora **BLOCCATO**. Gold e audit non
**INTEGRATO** o **CERTIFICATO**. Report:
`docs/relational-gold-e-v-preparation-01.md`.

### RD-RAG-DOCUMENTARY-GAP-AUDIT-01 — registrazione della ricognizione (2026-10-28)

Attività: pianificare audit supervisionato della copertura documentale RAG e gestione delle lacune, separato da Gold E/Gold V e dall'apprendimento. Script: nessuno; sola registrazione documentale nel TODO e nel registro. Risultato: perimetro definito per distinguere assenza reale del documento, mancato retrieval, evidenza insufficiente e fonti in conflitto; richiesta riconciliazione di originali, estrazioni, chunk, indici, provenienza e diritti prima di diagnosticare lacune. Decisione: eseguire in futuro ricognizione delle evidenze esistenti e predisporre registro lacune e flusso di approvazione prima di qualsiasi acquisizione o indicizzazione. Nessun test, inferenza, download, deploy o modifica pipeline. Stato: **DA FARE**. Registrazione TODO: commit `28d802b1`.

Aggiornamento conclusivo: ricognizione statica eseguita su codice, report,
inventari e prove GitHub; script non applicabile. Report:
`docs/rag-documentary-gap-audit-01.md`. Ricostruita la catena PDF → Docling →
chunk → embedding Qwen → Chroma → dense24/rerank → evidenze F → risposta e
citazioni. Riutilizzati audit preesistenti senza ripetere query o benchmark.
Consolidati cinque rilievi storici accertati di retrieval/chunking, un errore
Qwen già corretto e due limiti F non determinabili; nessuna assenza A dichiarata
dal solo checkout. Schema registro e procedura controllata documentati;
implementazione **DA FARE**. Decisione: ricognizione **ESEGUITO**; snapshot runtime, linkage
hash completo, diritti e copertura complessiva **BLOCCATO/DA FARE**. Nessun
download, inferenza, indicizzazione, benchmark, modifica pipeline, VPS, merge o
deploy; non **VALIDATO**, **INTEGRATO** o **CERTIFICATO**.

### RAG-CORPUS-PROVENANCE-INTEGRITY-DESIGN-01 — progettazione (2026-10-28)

Attività: progettare il collegamento verificabile PDF originale → estrazione
Docling → chunk → record Chroma a seguito dell'audit `8650121`. Script: non
applicabile, sola progettazione documentale. Report:
`docs/rag-corpus-provenance-integrity-design-01.md`. Risultato: definiti root
manifest content-addressed, record documento/chunk, stati di verifica,
canonicalizzazione, verificatore read-only, anomalie, snapshot su copia
consistente, rapporto con categorie A–F, rollback e cancelli G0–G4. Previsto
riuso di SHA ingestion, ID deterministici chunk e utility RFC 8785 da rendere
comune; il Provenance Registry Gold resta separato. Nessun validatore statico
aggiunto per evitare duplicazione prematura. Decisione: progettazione
**ESEGUITO**; schema/template/verificatore/fixture **DA FARE**; runtime
**BLOCCATO** fino a nuova autorizzazione e decisioni su collocazione, custodia
e snapshot. Nessun accesso VPS, test, Qwen, benchmark, modifica corpus/indice,
merge o deploy; non **VALIDATO**, **INTEGRATO** o **CERTIFICATO**.

Correzione revisione indipendente del commit `5c0b6a3`: conservata l'identità
derivata da hash storicamente verificato quando l'artefatto corrente è
inaccessibile, senza confonderla con l'integrità corrente; introdotta la
precondizione `inventory_completeness` per distinguere orfani reali da record
non riconciliati; resi deterministici ordinamento e hash del contenuto tecnico
del report separandoli dai timestamp di esecuzione; precisato che conteggi e ID
prima/dopo sono controlli accessori e non provano la consistenza dello snapshot.
Script: non applicabile. Test: nessuno. Perimetro esclusivamente documentale;
stato invariato: progettazione **ESEGUITO**, implementazione **DA FARE**,
runtime **BLOCCATO**, non **VALIDATO**, **INTEGRATO** o **CERTIFICATO**.

Nota di stato successiva: `DA FARE` descrive lo stato storico alla chiusura del
design; l'implementazione offline è registrata separatamente nella voce
seguente. Il runtime rimane **BLOCCATO**.

### RAG-CORPUS-PROVENANCE-INTEGRITY-OFFLINE-IMPLEMENTATION-01 — patch offline (2026-10-29)

Attività: implementare senza runtime il contratto approvato al commit
`38df9c5`. Script: `scripts/validate_rag_corpus_integrity_v1.py`. Commit
tecnico: `d12d636fa33411f24a390fe5d2666b08f3f9316a`. Report:
`docs/rag-corpus-provenance-integrity-offline-implementation-01.md`.
Risultato: schema/template manifest v1, snapshot adapter JSON read-only,
validazione di identità/hash/relazioni, classificazione completa/parziale,
report canonicale deterministico e CLI atomico **IMPLEMENTATO**. Test nuovi:
`python -m unittest projects/tactical-engine/tests/test_validate_rag_corpus_integrity_v1.py`,
16/16 OK; regressione Gold E/V v2 21/21 OK prima e dopo; compilazione Python
3.13.15 OK. Decisione: percorso offline su fixture **VALIDATO**, test
**ESEGUITO**, runtime **BLOCCATO**. Nessun accesso VPS, collection operativa,
Qwen, embedding, indicizzazione, benchmark, merge o deploy; non **INTEGRATO** o
**CERTIFICATO**.

### RAG-CORPUS-PROVENANCE-INTEGRITY-OFFLINE-CORRECTIONS-01 — correzione differenziale (2026-10-29)

Attività: chiudere cinque lacune della revisione indipendente senza estendere il
perimetro. Script: `scripts/validate_rag_corpus_integrity_v1.py`. Commit
tecnico: `f77cb9dfa694367430719022c1e01cb143168ada`. Report:
`docs/rag-corpus-provenance-integrity-offline-corrections-01.md`. Risultato:
derivazione sintetica Docling→chunk verificata; chunker reale privo di adapter
qualificato `UNVERIFIABLE_RELATION`; sottoinsieme JSON Schema applicato
integralmente; evidenze snapshot e identità storica risolte e confrontate per
hash; hash ID calcolato sulla sequenza completa con duplicati preservati.
Test Corpus Integrity 22/22 OK, regressione Gold E/V 21/21 OK, compilazione
Python 3.13.15 OK. Decisione: correzioni **IMPLEMENTATO**, test **ESEGUITO**,
controlli sintetici **VALIDATO**; chunker reale e runtime **BLOCCATO**. Nessun
accesso VPS, Chroma operativo, Qwen, embedding, indicizzazione, benchmark,
merge o deploy; non **INTEGRATO** o **CERTIFICATO**.

### RAG-CORPUS-PROVENANCE-INTEGRITY-OFFLINE-CLOSEOUT-01 — chiusura residui (2026-10-29)

Attività: chiudere le tre osservazioni residue della revisione indipendente,
senza ripetere l'audit né ampliare il perimetro. Script:
`scripts/validate_rag_corpus_integrity_v1.py`. Commit tecnico:
`66752e0aad42f89e28d6aed8a2b33357abb72f0b`. Report:
`docs/rag-corpus-provenance-integrity-offline-closeout-01.md`. Risultato: gli
ID duplicati nell'estrazione sintetica sono rilevati prima del dizionario;
l'estrazione sintetica inaccessibile conserva `NOT_ACCESSIBLE` e aggiunge
`UNVERIFIABLE_RELATION`; le evidenze distinguono accessibilità, hash,
pertinenza al soggetto e garanzia qualificata mediante attestazione JSON
tipizzata e legata agli identificativi verificati. Tre test differenziali
nuovi; Corpus Integrity 25/25 OK, regressione Gold E/V 21/21 OK, compilazione
Python e diff check PASS. Decisione: codice **IMPLEMENTATO**, test
**ESEGUITO**, controlli sintetici **VALIDATO**; chunker reale e runtime
**BLOCCATO**. Nessuna VPS, Chroma operativo, Qwen, embedding, indicizzazione,
benchmark, merge o deploy; non **INTEGRATO** o **CERTIFICATO**.

### RAG-CORPUS-INTEGRITY-REAL-CHUNKER-ADAPTER-01 — decisione di riproducibilità (2026-10-29)

Attività: verificare se il chunker reale V5 fosse ricostruibile esattamente dal
solo codice ed evidenze offline disponibili. Script esaminati:
`scripts/ingest_pdfs.py` e `scripts/build_rag_index_v5_multisource.py`;
nessun nuovo script. Report: `docs/rag-corpus-real-chunker-adapter-01.md`.
Risultato: algoritmo statico ricostruito fino a ID, testo contextualizzato,
metadata, pagine e heading; la riproducibilità esatta non è dimostrabile perché
il tokenizer `nomic-ai/nomic-embed-text-v1.5` non ha revision/digest congelati
e abilita codice remoto, versioni/configurazione non sono legate alla singola
run e manca un bundle reale isolato estrazione→record. Dipendenze locali
docling-core/Transformers/Chroma assenti e non scaricate. Decisione: **Caso B**,
nessun adapter approssimativo, nessun test artificiale e nessuna ripetizione
delle regressioni non necessarie. Ricostruzione statica **ESEGUITO**;
verificatore sintetico precedente **VALIDATO**; adapter reale e runtime
**BLOCCATO**. Nessuna VPS, collection operativa, indicizzazione, embedding,
Qwen/Ollama, benchmark, merge o deploy; non **INTEGRATO** o **CERTIFICATO**.

### RD-SUPERVISED-AUTO-LEARNING-DESIGN-01 — registrazione progettazione (2026-10-28)

Attività: progettare auto-learning supervisionato separato dalla verifica intelligente dei documenti, senza attivare apprendimento. Script: nessuno; registrazione documentale. Risultato: perimetro previsto per feedback, correzioni tattiche approvate, lacune RAG, versionamento delle conoscenze, controllo umano, rollback, separazione dati di sviluppo/gold e misurazione indipendente. Decisione: riconciliare componenti e prove esistenti prima di progettare, distinguere aggiornamento controllato RAG da fine-tuning Qwen; subordinare futura implementazione e attivazione a Gold E/V e audit documentale, con autorizzazioni separate. Nessun test, training, inferenza, download, indicizzazione, deploy o modifica della pipeline. Stato: **DA FARE**. Registrazione TODO: commit `7be4d826`.

### RD-RELATIONAL-GOLD-E-V-COLLECTION-PLANNING-01 — piano operativo (2026-10-28)

Attività: definire la raccolta indipendente senza avviarla. Script: non
applicabile, attività esclusivamente documentale; nessun eseguibile o test
aggiunto. Report: `docs/relational-gold-e-v-collection-plan-01.md`. Risultato:
proposti pilot procedurale 12 permanentemente escluso dal gold, Gold E 60
domande in dieci famiglie con provenienza 24/18/18 e Gold V naturale 60
risposte solo dopo freeze Gold E; definiti screening, ruoli A/B/C/D, flusso
G0–G9, freeze, dati per diagnosi documentale, separazione auto-learning,
rischi e decisioni del titolare. Nessuna raccolta, annotazione, inferenza,
benchmark, chiamata esterna, modifica runtime, merge o deploy. Decisione:
pianificazione **ESEGUITO**; raccolta/annotazione/freeze **DA FARE**,
`RD-RELATIONAL-GOLD-E-V-01` **BLOCCATO**, audit documentale e auto-learning
**DA FARE**; gold/audit non **VALIDATO**, **INTEGRATO** o **CERTIFICATO**.

Revisione indipendente ChatGPT sul commit `cbece0f`: **APPROVABILE CON
CORREZIONI**. Commit rettifiche `f2242c4`: C1 estende i limiti a autore,
organizzazione e origine comune e vieta autori esposti ai failure mode; C2
introduce matrice di sottotemi/dimensioni senza forzare etichette; C3 definisce
misure, accettazione del pilot, disaccordi e versionamento istruzioni; C4
traccia esclusioni/sostituzioni e nuovi manifest; C5 separa analisi per
risposta/requisito, dipendenza per `case_id` e fallimenti tecnici; C6 definisce
accessi, retention, revoca, licenze, pubblicabilità e isolamento dai flussi
automatici. Pilot 12, Gold E 60, Gold V 60 e quote 24/18/18 invariati. Nessun
test, raccolta, annotazione, inferenza, benchmark o runtime modificato. Stato
invariato: pianificazione **ESEGUITO**; G0–G8 **DA FARE**, G9 e validazione
indipendente **BLOCCATO**.

Compatibilità rilevata senza modifica degli schemi: Gold E v1 non tipizza
autore/organizzazione/origine comune/licenza/retention e vieta proprietà
aggiuntive; Gold V v1 richiede `answer` non vuoto e non rappresenta
timeout/errori. Decisione: preservare gli hash v1 e sottoporre al titolare
un'evoluzione versionata prima di G1/G6, senza usare campi provvisori o archivi
paralleli. Stato della correzione schema: **DA FARE**; non impedisce la chiusura
della pianificazione ma impedisce l'avvio corretto delle fasi interessate.

### RD-RELATIONAL-GOLD-E-V2-OFFLINE-CONTRACTS-01 — contratti v2 isolati (2026-10-28)

Attività: implementare offline l'evoluzione v2 approvata congiuntamente da
Codex e ChatGPT, preservando integralmente v1. Script:
`scripts/validate_relational_gold_preparation_v2.py`; test:
`tests/test_validate_relational_gold_preparation_v2.py`; report:
`docs/relational-gold-e-v2-offline-contracts-01.md`; commit tecnico:
`d26f364`. Risultato: Provenance Registry, Gold E/Gold V, Annotation Ledger e
manifest v2 con template vuoti; quattro esiti tecnici Gold V, riferimenti Gold
E senza duplicazione, ledger A/B/C, dipendenze tipizzate, hash/cicli/freeze e
profilo RFC 8785 standard-library. JSON 10/10, compilazione PASS, validatore
`V2_PREPARATION_VALID`, test v2 12/12 e regressione v1 5/5; sette SHA-256 v1
invariati, `CASES 0`, `INFERENCE NOT_RUN`. Decisione: contratti
**IMPLEMENTATO**, verifiche **ESEGUITO**, patch isolata **VALIDATO** offline.
Raccolta, annotazione, adjudication e freeze **DA FARE**; gold indipendente e
benchmark **BLOCCATO**. Nessun runtime, RAG, Qwen, corpus, indice, API,
pannello, VPS, merge o deploy; non **INTEGRATO** o **CERTIFICATO**.

### RD-RELATIONAL-GOLD-E-V2-FREEZE-VALIDATION-01 — correzione freeze completo (2026-10-28)

Attività: recepire la revisione indipendente del commit `dabfff6` senza
duplicare i controlli già esistenti. Script aggiornato:
`scripts/validate_relational_gold_preparation_v2.py`; test aggiornato:
`tests/test_validate_relational_gold_preparation_v2.py`; report:
`docs/relational-gold-e-v2-freeze-validation-correction-01.md`; commit tecnico:
`596c4ba`. Risultato: CLI `--freeze-manifest` collega le verifiche
referenziali su file effettivi; manifest Gold V indicizzato per `attempt_id`;
hash di answer/input/configurazione ricalcolati; hash e versione del manifest
Gold E coerenti fra dipendenza, dataset e tentativi; precondizioni di freeze,
ledger A/B/C, stati e dipendenze validate congiuntamente e ricorsivamente. Sei
test differenziali nuovi; v2 18/18 e v1 5/5, totale 23/23 PASS, compilazione e
diff check PASS. Decisione: correzione **IMPLEMENTATO**, test **ESEGUITO**,
percorso freeze offline **VALIDATO**. Nessun dato reale, inferenza, benchmark,
runtime, pannello, RAG, Qwen, corpus, indice, API, VPS, merge o deploy. Gold
indipendente ancora **BLOCCATO**; non **INTEGRATO** o **CERTIFICATO**.

### RD-RELATIONAL-GOLD-E-V2-CASE-FREEZE-01 — precondizioni per caso (2026-10-28)

Attività: chiudere l'unico limite residuo indicato dalla revisione indipendente
di HEAD `40dfd73`, riutilizzando il percorso completo già validato. Script:
`scripts/validate_relational_gold_preparation_v2.py`; test:
`tests/test_validate_relational_gold_preparation_v2.py`; report:
`docs/relational-gold-e-v2-case-freeze-preconditions-01.md`; commit tecnico:
`454ebad`. Risultato: manifest congelato senza `frozen_at`, record non
`frozen` e caso Gold E non `independent_frozen` sono rifiutati fail-closed.
Tre test negativi nuovi; test positivo completo riutilizzato. V2 21/21 e v1
5/5, totale 26/26 PASS, compilazione e diff check PASS. Decisione: delta
**IMPLEMENTATO**, test **ESEGUITO**, percorso freeze aggiornato **VALIDATO**
offline. Nessuna raccolta, annotazione reale, inferenza, benchmark, runtime,
pannello, RAG, Qwen, corpus, indice, API, VPS, merge o deploy. Gold indipendente
ancora **BLOCCATO**; non **INTEGRATO** o **CERTIFICATO**.

### RD-FEEDBACK-UX-CONFIRMATION-01 — conferma visuale persistita (2026-10-28)

Attività: ricostruire il percorso pannello → API → persistenza → recupero e
correggere soltanto la UX se il backend risultava funzionante. Script
applicativo: `api/knowledge_panel.html`; test differenziale:
`tests/test_knowledge_panel_feedback_ui.js`; report:
`docs/feedback-ux-confirmation-01.md`; commit tecnico `ed7a84c`. Risultato: il
backend esistente salva atomicamente un voto per job e lo restituisce nelle
letture live/persistite; il pannello non ne rappresentava lo stato. Aggiunti
caricamento, blocco dei doppi clic, verifica della conferma server, spunta
verde soltanto dopo successo, errore ritentabile e ripristino da
`job.feedback`. Contratto `/v1/feedback`, schema e backend invariati. Test UX
4/4 e suite API 35/35 PASS; script inline eseguiti dal test Node e diff check
PASS. Decisione: chiudere il difetto esclusivamente frontend. Stato:
correzione **IMPLEMENTATO**, test **ESEGUITO**, comportamento coperto
**VALIDATO offline**; nessun Qwen, benchmark, merge o deploy, quindi non
**INTEGRATO** o **CERTIFICATO** nel pannello pubblico.

### RAG-CORPUS-REAL-CHUNKER-EVIDENCE-READINESS-01 — inventario GitHub (2026-10-29)

Attività: verificare se gli artefatti già pubblicati permettono di predisporre
il bundle probatorio del chunker reale senza accedere a VPS o indici. Script:
nessuno; sola ricognizione Git e documentale. Baseline: `83b235c`. Report:
`docs/rag-corpus-real-chunker-evidence-readiness-01.md`. Risultato: algoritmo,
costanti e storia del builder disponibili; evidenze di hash PDF, versioni,
fingerprint e record diagnostici soltanto parziali; assenti dal checkout JSON
Docling reali con hash, export record della stessa run, revisione/hash del
tokenizer e del remote code e collegamento extraction→record. I file runtime
inventariati in `runtime_evidence_manifest_v1.json` conservano percorso,
dimensione e hash, ma non sono pubblicati con il loro contenuto. Decisione:
**Caso B** invariato; definito contratto minimo per un singolo bundle pilota
read-only da acquisire solo con autorizzazione separata. Stato: inventario e
progettazione documentale **ESEGUITO**; acquisizione **DA FARE**; adapter reale
e runtime **BLOCCATO**. Nessun test ripetuto, VPS, download, indicizzazione,
inferenza, merge o deploy; non **IMPLEMENTATO**, **VALIDATO**, **INTEGRATO** o
**CERTIFICATO**.

### RAG-CORPUS-REAL-CHUNKER-PILOT-BUNDLE-PLAN-01 — piano acquisizione (2026-10-29)

Attività: preparare, senza accessi runtime, il piano per acquisire in futuro un
solo bundle probatorio read-only. Script: nessuno; ricognizione statica degli
strumenti Ussia già esistenti. Baseline: `3137c6f`. Report:
`docs/rag-corpus-real-chunker-pilot-bundle-plan-01.md`. Risultato:
`Transizioni.Ussia` proposto come candidato provvisorio grazie a source path,
riferimenti Docling `#/texts/151`–`154`, ID target completo e mapping già
inventariato; l'idoneità resta subordinata alla presenza degli artefatti e
all'attribuzione alla stessa run. Definiti cancelli G0–G5, export completo del
solo documento, fingerprint run/tokenizer/remote code, manifest
content-addressed, riservatezza e criteri completo/parziale/non utilizzabile.
Closeout documentale: `PersistentClient` con sole chiamate applicative
`get()`/`count()` non costituisce garanzia di assenza di effetti interni e il
secondo diagnostico scrive un report; l'acquisizione futura deve operare su
snapshot coerente e isolato, verificato prima/dopo. Gli export per `source` e
`source_relative` devono essere confrontati per ID; record mancanti,
discordanti o non riconciliati impediscono la completezza documentale e i
conteggi filtrati non provano quella dell'intera collection. Decisione:
pianificazione **ESEGUITO**; acquisizione **DA FARE**; verificatore
sintetico precedente **VALIDATO**; adapter reale e collection **BLOCCATO**.
Pre-acquisizione: aggiunta nello stesso report una checklist non eseguita con
percorsi verificati/storici/da confermare, cancelli di autorizzazione e
snapshot, hash pre/post, doppio export e riconciliazione ID, provenienza della
stessa run, manifest e riuso di `sha256_file`, `manifest_hash`,
`validate_manifest_contract`, `ReadOnlySnapshotAdapter` e `verify_integrity`.
Decisione nuova: l'acquisizione non è autorizzabile finché titolare e custode
non confermano snapshot isolato, staging riservato, sorgenti, retention e
perimetro copiabile; stato operativo invariato.
Nessun accesso VPS/Chroma, export, download, test, inferenza, indicizzazione,
merge o deploy; nulla di nuovo **IMPLEMENTATO**, **INTEGRATO** o
**CERTIFICATO**.

### RAG-CORPUS-USSIA-READONLY-PREFLIGHT-01 — metadati filesystem (2026-10-29)

Attività: eseguire una sola connessione SSH autorizzata per `stat` e controllo
di accessibilità teorica sui percorsi letterali JSON Ussia, sidecar e root
Chroma, senza leggere contenuti o enumerare directory. Script: nessuno; comando
SSH non interattivo predisposto inline. Baseline: `bc752fd`. Report:
`docs/rag-corpus-ussia-readonly-preflight-01.md`. Risultato: autenticazione
rifiutata con `Permission denied (publickey,password)` prima dell'esecuzione di
qualunque comando remoto. Nessun secondo tentativo, in rispetto del limite di
una connessione. I tre percorsi restano `nominal_unconfirmed`; PDF, snapshot,
staging e provenienza restano non verificati. Decisione: preflight
**BLOCCATO**; nuovo tentativo solo con nuova autorizzazione e autenticazione
utilizzabile. Piano **ESEGUITO**, acquisizione **DA FARE**, verificatore
sintetico **VALIDATO**, adapter e runtime **BLOCCATO**. Nessun contenuto letto
o copiato, nessun Chroma/SQLite, hash, export, modifica, test, merge o deploy;
non **INTEGRATO** o **CERTIFICATO**.

Aggiornamento differenziale: il titolare ha confermato accesso SSH manuale
riuscito con password. Un secondo e singolo tentativo Codex, espressamente
autorizzato, è terminato con `ssh: connect to host 163.5.26.155 port 22:
Permission denied` prima del prompt password; nessun comando remoto è stato
eseguito e non è seguito alcun retry. Il blocco non prova un difetto delle
credenziali o della VPS, ma l'indisponibilità della connessione SSH nel contesto
processo Codex impiegato. Decisione: preflight ancora **BLOCCATO**; tre percorsi
`nominal_unconfirmed`; eventuale procedura manuale metadata-only o diverso
terminale con rete effettiva richiedono perimetro e autorizzazione distinti.

Closeout: con autorizzazione distinta il titolare ha eseguito una sola volta il
comando manuale metadata-only revisionato. Risultato: JSON Ussia `confirmed`,
regular file, 501909 byte, mtime `2026-10-21 03:16:21.319698605 +0200`,
`football:football`, mode `600`; sidecar `confirmed`, regular file, 500 byte,
mtime `2026-10-21 03:16:24.888796756 +0200`, `football:football`, mode `600`;
root Chroma `confirmed`, directory, 4096 byte, mtime
`2026-10-29 09:01:05.208828426 +0100`, `football:football`, mode `775`.
Nessun contenuto, enumerazione, hash, copia, snapshot, export o modifica.
Separatamente, chiave Ed25519 locale dedicata con pubblica `restrict` installata
dal titolare e singolo test non interattivo `SSH_KEY_ACCESS_OK`; la privata non
è nel repository e non costituisce autorizzazione permanente alle operazioni.
Decisione: preflight **ESEGUITO**, tre percorsi `confirmed`; acquisizione **DA
FARE**; snapshot probatorio, adapter reale e collection runtime **BLOCCATO**;
non **INTEGRATO** o **CERTIFICATO**.

### RAG-CORPUS-USSIA-GATE-A-READONLY-01 — readiness snapshot (2026-10-29)

Attività: singola ricognizione SSH autorizzata e preventivamente delimitata su
metadati, mount/dispositivi, unità/timer, processi/file descriptor accessibili,
cron e parent dello staging. Script: inline non persistito; due errori di
composizione locale sono avvenuti prima dell'invocazione SSH, quindi una sola
connessione remota effettiva. Baseline `3bbb3c6`; report
`docs/rag-corpus-ussia-gate-a-readonly-01.md`. Risultato: Chroma su ext4 diretto
`/dev/vda1`, 41.794.781.184 byte liberi; comandi LVM/Btrfs presenti ma backing
store non LVM/Btrfs/ZFS, nessuno snapshot atomico locale dimostrato. API RAG
`active/running`, maintenance e FIGC service inattivi con timer attivi; un
processo Python visibile mantiene un descriptor sotto Chroma. Nessun cron
pertinente osservato. Parent staging `evidence` mode `700`, directory `ussia`
assente. Decisione: Gate A **ESEGUITO**; raccomandata cold copy con quiescenza,
ma stop/start, staging, dimensionamento, copia e hash richiedono Gate B. Nessun
contenuto corpus, Chroma/SQLite, stop, snapshot, copia, hash o modifica.
Acquisizione **DA FARE**; snapshot/adattatore/runtime **BLOCCATO**; non
**VALIDATO**, **INTEGRATO** o **CERTIFICATO**.

### RAG-CORPUS-USSIA-GATE-B-SSH-DIAGNOSTIC-01 — processo API e avvio (2026-10-30)

Attività: singola diagnostica SSH read-only autorizzata per identificare il
processo API e i meccanismi di avvio pertinenti, senza ripetere il controllo
privilegiato `lsof +D`. Script: nessuno; comandi diagnostici inline non
persistiti. Baseline `9bcc033`.

Evidenze osservate: PID `76562`, PPID `939`, utente `football`, comando
`rag_v5_api.py` tramite virtualenv; cgroup
`/user.slice/user-1000.slice/user@1000.service/app.slice/football-rag-api.service`.
`systemctl --user` ha risolto l'unità `football-rag-api.service`, caricata da
`/home/football/.config/systemd/user/football-rag-api.service`,
`active/running`, `enabled`, `MainPID=76562`, `Restart=on-failure`,
`RestartSec=5s`, `TimeoutStopSec=30s`. Il padre era il manager systemd utente
PID `939`; non sono stati osservati processi figli. I timer
`football-rag-maintenance.timer` e `football-figc-discovery.timer` risultavano
`active/waiting` ed `enabled`; i relativi oneshot erano `inactive/dead`.
Nessun crontab per `football`, job `at` o process manager Supervisor, PM2,
Docker o Podman pertinente è stato osservato. `Linger=yes` e avvio automatico
dopo reboot erano già documentati e validati in attività precedenti.

Inferenze tecniche: la futura procedura autorizzata deve arrestare l'API con
`systemctl --user stop football-rag-api.service`, non con `kill`; uno stop
esplicito non attiva normalmente `Restart=on-failure`. Il timer maintenance è
un potenziale utilizzatore diretto di Chroma; la sospensione FIGC è
prudenziale e non gli attribuisce accessi Chroma non dimostrati. Fermare un
timer non arresta un oneshot già avviato.

Limiti: la diagnostica non dimostra l'assenza universale di writer
privilegiati o invisibili, né la quiescenza continua durante una futura copia.
Campionamenti periodici dei descriptor non escludono accessi fra due
osservazioni. API `enabled` e `Linger=yes` lasciano un rischio di nuovo avvio
in caso di reboot, riavvio del manager utente o richiesta esterna. Nessun
runtime mask, stop, restart, copia, snapshot, hash o accesso Chroma/SQLite è
stato eseguito.

Decisione: integrare queste evidenze e i controlli di quiescenza nella sezione
9.9 del piano esistente, senza creare un piano parallelo. La procedura deve
registrare lo stato iniziale prima degli arresti e l'esito individuale di ogni
operazione, affinché un arresto parziale possa essere ripristinato in modo
idempotente senza avviare unità originariamente inattive.

Un cambiamento del boot ID o dell'identità del manager utente invalida il
tentativo: nessuna ripresa automatica e nessuna riapplicazione cieca dello
stato precedente. Sono richiesti una nuova ricognizione dello stato corrente
e un recupero manuale controllato. Eventuali bundle incompleti restano
`incomplete/non_promotable`.

La cold copy non è autorizzata e resta **BLOCCATO** finché dimensionamento,
controllo dei writer per l'intera finestra, autorizzazioni operative e
ripristino non siano definiti e verificabili.

Stato: diagnostica SSH **ESEGUITO**; preflight successivo **DA FARE**;
ulteriori controlli privilegiati **DA FARE** se necessari; cold copy, adapter
reale e certificazione runtime **BLOCCATO**. Non **VALIDATO**, **INTEGRATO** o
**CERTIFICATO**.

### RAG-CORPUS-USSIA-GATE-B-DIMENSIONAL-PREFLIGHT-INTEGRATION-01 — consolidamento locale (2026-10-30)

Attività: integrazione locale byte-per-byte dello script metadata-only USSIA
Gate B Derived 05, dopo revisione statica indipendente. Baseline
`23508fc3a7bb4f0b33ab95687ae5d55b6c6be6ab`; commit tecnico
`7e9dae3211c3a65113524cef3ca980e77eae5c77`. Script:
`scripts/ussia_gate_b_dimensional_preflight_v1.sh`, modalità Git `100755`,
1.486 righe, 36.372 byte, SHA-256
`2644d06899c74d1eae49c1de6bdbdde82e88382844993200bdee98edf3f800dd`.
Sorgente e destinazione hanno identità byte-per-byte; il commit tecnico
contiene soltanto il nuovo script.

Evidenze: fetch del solo branch GitHub pertinente, locale/remoto sulla stessa
baseline con divergenza `0/0`, working tree iniziale pulito, destinazione
assente, nessuno script Bash equivalente, hash/byte/righe e modalità
verificati, diff statico circoscritto. Report:
`docs/rag-corpus-ussia-gate-b-dimensional-preflight-integration-01.md`.

Decisione: revisione Derived 05 **VALIDATO** esclusivamente nel perimetro
statico; script **IMPLEMENTATO** localmente. Non sono stati eseguiti script,
`bash -n`, ShellCheck, test, SSH/VPS, Chroma/SQLite, snapshot, stop di
servizi o cold copy. Preflight dimensionale e misurazione RSS **DA FARE**;
cold copy, adapter reale e certificazione runtime **BLOCCATO**. I commit
locali non sono ancora pubblicati su GitHub; non **VALIDATO runtime**,
**INTEGRATO** o **CERTIFICATO**.

Closeout post-pubblicazione: il branch GitHub
`codex/tactical-state-contract-v1` espone il commit documentale pubblicato
`032bd5594b7939bb23c36eb05d436adbc317632a`, discendente diretto del commit
tecnico `7e9dae3211c3a65113524cef3ca980e77eae5c77`. Lo script
`scripts/ussia_gate_b_dimensional_preflight_v1.sh`, modalità Git `100755`,
mantiene SHA-256 `2644d06899c74d1eae49c1de6bdbdde82e88382844993200bdee98edf3f800dd`.
Pubblicazione GitHub **ESEGUITO**; script **IMPLEMENTATO**; revisione statica
**VALIDATO** esclusivamente nel perimetro statico. Nessuna esecuzione runtime.
Preflight dimensionale e misurazione RSS **DA FARE**; cold copy, adapter reale
e certificazione runtime **BLOCCATO**. La pubblicazione non equivale a
integrazione nella pipeline o certificazione: non **VALIDATO runtime**,
**INTEGRATO** o **CERTIFICATO**.

### RAG-CORPUS-USSIA-GATE-B-ATTESTATION-CONTRACT-01 — formalizzazione alternativa B (2026-11-01)

Attività: formalizzazione documentale della decisione espressa dal titolare
sul contratto USSIA Gate B. Script: Derived 05 invariato, SHA-256
`2644d06899c74d1eae49c1de6bdbdde82e88382844993200bdee98edf3f800dd`;
nessuna esecuzione. Report aggiornato:
`docs/rag-corpus-ussia-gate-b-dimensional-preflight-integration-01.md`.
Risultato: adottata l'alternativa B con quattro attestazioni indipendenti
(completezza dimensionale, valutazione strutturale con completezza ed esito,
verifica quote, idoneità finale della capacità). L'alternativa A resta
informativa e non promuovibile; l'alternativa C resta requisito separato per
la verifica effettiva delle quote. Exit `2` non dimostra completezza. Un esito
`verified_unfavorable` richiede una condizione bloccante positivamente
dimostrata, completa, attribuibile e conclusiva; timeout, output parziale,
misure non affidabili o attribuzione incerta non sono esiti negativi
verificati. Decisione: nessuna attestazione autorizza la cold copy e
l'approvazione non autorizza attività runtime. Stato: formalizzazione
documentale **ESEGUITO**; preflight dimensionale e RSS **DA FARE**; cold copy,
adapter reale e certificazione runtime **BLOCCATO**; non **INTEGRATO** o
**CERTIFICATO**.

### RD-TSC-GENERATIVE-OFFLINE-01 — integrazione generativa opt-in (2026-11-01)

Attività: implementare offline il nuovo percorso
`--tactical-state-contract`, distinto da `--tactical-plan` e disattivato nel
profilo pubblico. Script: `v5_tactical_state_contract_v1.py`,
`smoke_test_rag_v5_e2e.py`, `run_rag_v5_query.py`; test:
`test_v5_tactical_state_generation_v1.py`. Commit tecnico:
`acb7f7178e971173dbde1b6ff742fa5b67eebc5c`. Report:
`docs/tactical-state-contract-generative-offline-01.md`. Risultato: singola
funzione di trasporto e una sola chiamata per costruzione; nessun repair;
schema di trasporto che riusa `tactical_state_contract_v1`; controlli separati
per struttura, domanda-piano, piano-prosa e audit esistente; raw output,
normalizzazioni e motivazioni preservati. Solo `validated` promuove `answer`;
gli altri esiti sono fail-closed e il wrapper non li considera query complete.
Test nuovi 19/19, regressione mirata totale 154/154, compilazione in memoria
4/4 e diff check PASS. Decisione: codice **IMPLEMENTATO**, test **ESEGUITO**,
proprietà coperte **VALIDATO** offline. Compatibilità reale del formato
Ollama/Qwen, qualità tattica e stabilità runtime **DA FARE**; API, pannello,
corpus, indici e deploy invariati. Non **INTEGRATO** o **CERTIFICATO**.

### RD-TSC-GENERATIVE-OFFLINE-CORRECTIONS-01 — fail-closed conservativo (2026-11-01)

Attività: correggere esclusivamente i rilievi della revisione indipendente sul
commit `5992c5818fecef174fde4bd21fc839f14323e0cd`. Script:
`v5_tactical_state_contract_v1.py`; test:
`test_v5_tactical_state_generation_v1.py`. Commit tecnico: `21bfd36`.
Report: `docs/tactical-state-contract-generative-offline-corrections-01.md`.
Risultato: il controllo piano-prosa non passa più con scope critico vuoto o
insufficiente; le verifiche obbligatorie non valutabili impediscono
`validated`; forma JSON annidata e riferimenti tipizzati sono controllati e
classificati prima della validazione del dominio. Il modello tattico rimane
unicamente `tactical_state_contract_v1`; nessuna regex tattica ad hoc aggiunta.
Cinque test nuovi, suite generativa 24/24, regressione mirata totale 159/159,
compilazione 2/2 e diff check PASS. Decisione: correzioni **IMPLEMENTATO**,
test **ESEGUITO**, comportamento coperto **VALIDATO** offline. Runtime
Ollama/Qwen, qualità e stabilità **DA FARE**; percorso non **INTEGRATO** o
**CERTIFICATO**.

## RD-TSC-GENERATIVE-DIAGNOSTIC-MISSING-01 — Correzione motivazioni incomplete (2026-11-01)

Attività: propagare i codici dei campi mancanti del controllo domanda–piano nel riepilogo `reasons`, mantenendo `blocked`, `failed_scope` e la diagnostica originale. Script: `scripts/v5_tactical_state_contract_v1.py`; test mirato aggiunto a `tests/test_v5_tactical_state_generation_v1.py`. Commit codice: `480cd9e8f73cd3f2e3fcd54235d6d5c6245935fb`; commit test: `42a97b2dc3f64d7aff177fc1e23a2d8c7f92e812`. Report: `docs/tactical-state-contract-generative-diagnostic-missing-01.md`. Risultato: eseguito esclusivamente `ContractGenerationTests.test_incomplete_question_alignment_reports_missing_reasons`, 1/1 PASS in 0,004 s; verificati stato `blocked`, `question_compatibility` in `failed_scope`, dettaglio `missing`, codice in `reasons`, `promoted_answer` vuoto e deduplicazione preservata. Decisione: correzione **VALIDATO offline** nel perimetro differenziale; codice **IMPLEMENTATO**, test **ESEGUITO**. Nessuna inferenza Qwen/Ollama, VPS, API o deploy; non **INTEGRATO** o **CERTIFICATO**.

## RD-TSC-RUNTIME-GATE-FIGC5-CANDIDATE-01 — Chiusura diagnostica offline (2026-11-03)

Attivita: analizzare esclusivamente codice, documentazione e quattro artefatti gia prodotti dall'unica esecuzione autorizzata del Gate FIGC5. Script: nessuno eseguito nel closeout. Artefatti: JSON 44185 byte SHA-256 `a9c24186b9639d6e46c4b21795a74e5934269a8b6f0080b3c8be8a6c3bcc02b9`; stdout 511 byte `983faa69d3eb431d3bb02cdb6ec7cbb813ca7c30e19b77ba101bcd013b77aa22`; stderr/time 1891 byte `9aa6dcae25c0d2a54392301f2a8a45c9f36b64f715e90aee07b7194a066f6d10`; exit code 12 byte `85acfd2e79dd47df07d214334642196301332f72d792b52068cdfd8898755409`. Report: `docs/tactical-state-contract-runtime-gate-figc5-diagnostic-closeout-01.md`.

Risultato: exit `1`, `overall_status=blocked`, una generazione, zero repair, nessuna risposta promossa e collection invariata a 6410. Il piano applicato contiene 4-3-3 e slot astratti ma nessuna relazione operativa: e formalmente valido secondo la baseline, ma tatticamente insufficiente. `question_compatibility` passa perche controlla soltanto fatti espliciti; l'assenza di eventi, mapping e assignments produce `required_scope=[]` e `plan_prose_alignment=not_assessable`. Il blocco deriva direttamente da `tactical_documentary_audit.complete=false`; il piano-prosa non valutabile, da solo, avrebbe prodotto `not_evaluable`. F2/F3/F8 supportano solo parte dei claim effettivi della explanation. Densita/prossimita, palla coperta/scoperta e relazione completa attore-compito-spazio-trigger-finalita sono requisiti mancanti dell'audit, non claim automaticamente attribuiti alla explanation. L'assenza nell'intero corpus non e determinabile.

Decisione: nessuna correzione proposta in questa attivita. Chiusura diagnostica offline **ESEGUITO**; fail-closed osservato nel singolo caso **VALIDATO**; Gate runtime FIGC5 e integrazione runtime TSC **BLOCCATO**; certificazione runtime non conseguita. Nessuna inferenza, retry, repair, test, query Chroma/Ollama/API, modifica al codice/retrieval, deploy, merge o push eseguiti durante l'analisi.

## RD-TSC-OPERATIONAL-RELATIONS-CONTRACT-V2-01 — Implementazione offline (2026-11-03)

Attivita: implementare in un modulo isolato l'estensione versionata TSC V2 per relazioni attore-compito-spazio-trigger-finalita, senza modificare TSC V1 o collegare il runtime. Script: `scripts/v5_tactical_state_contract_v2.py`; test: `tests/test_v5_tactical_state_contract_v2.py`; commit tecnico `4cf91d6ae0c189d75d52ed52c7dda17e74d18274`; report `docs/tactical-state-contract-v2-operational-relations-offline-01.md`.

Risultato: proiezione deterministica dei `relation_requirements` con normalizzazione NFC/casefold, SHA-256 dei termini e fingerprint canonicale del requisito; rule ID e tabella fase chiusi; `position_ref` soltanto su risoluzione esatta univoca. `operational_relations` verifica fingerprint, riferimenti, attore, task, spazio, trigger, finalita e fase; il solo ID non copre un requisito. Solo `explicit_representable` e obbligatorio; open, inferiti e ambigui restano `unassessed`. Test V2 13/13, regressioni V1/generazione/planner 125/125, compilazione in memoria 2/2 e diff check PASS.

Decisione: codice **IMPLEMENTATO**, test **ESEGUITO**, controlli differenziali **VALIDATO offline**. Nessun handoff al prompt o runner e nessun flag V2: generazione V2, runtime, API e pannello **DA FARE**; integrazione e certificazione runtime **BLOCCATO**. Nessuna inferenza, retry, repair, query Ollama/Chroma/API, modifica al retrieval, deploy o merge.

### Remediation fail-closed conclusiva (2026-11-03)

Attivita: correggere esclusivamente la validazione offline V2 rilevata dalla
revisione indipendente. Script e test: gli stessi dell'esperimento; commit
tecnico `fa56b8b`; report aggiornato
`docs/tactical-state-contract-v2-operational-relations-offline-01.md`.

Risultato: applicata la validazione strutturale deterministica di campi, tipi,
proprieta aggiuntive, riferimenti, cardinalita e provenienza; riferimenti ad
attore, fase e posizione verificati per ogni relazione; ID requisito mancanti
o duplicati rifiutati; fingerprint legato anche alla provenienza di
estrazione; proiezione assente o incompleta distinta da input malformato e da
assenza esplicita verificata; risoluzione della fase fail-closed in presenza di
termini sconosciuti. Eseguiti soltanto otto test differenziali nuovi e una
regressione positiva direttamente interessata: 9/9 PASS in 0,019 s. Le
campagne precedenti 13/13 e 125/125 non sono state ripetute; `git diff --check`
PASS.

Decisione: remediation **IMPLEMENTATO**, test mirati **ESEGUITO**, proprieta
corrette **VALIDATO offline**. TSC V1, planner V1, retrieval, runner, prompt,
API e pannello invariati. Handoff generativo e runtime **DA FARE**;
integrazione e certificazione runtime **BLOCCATO**. Nessuna inferenza, retry,
repair, accesso Ollama/Chroma/API, deploy o merge.

### Remediation finale sicurezza tipi JSON (2026-11-03)

Attivita: rendere fail-closed le operazioni su valori JSON non hashable nel
solo modulo offline V2. Script e test: gli stessi dell'esperimento; commit
tecnico `ac4100d`; report aggiornato
`docs/tactical-state-contract-v2-operational-relations-offline-01.md`.

Risultato: guardie di tipo applicate a provenance, assertion mode, kind,
relation ID e required dimensions prima di appartenenza a insiemi o
deduplicazione. La ricognizione statica delle funzioni modificate e delle
chiamate dirette ha individuato e corretto gli equivalenti requirement
type/specificity e rule ID. Input lista, oggetto, numero, booleano o null non
genera piu `TypeError`: il piano applicato malformato e `failed`, mentre una
proiezione incompleta resta `not_assessable`. Eseguiti soltanto cinque casi
obbligatori, un caso equivalente e una regressione positiva: 7/7 PASS in
0,063 s; `git diff --check` PASS. Non ripetute le campagne 13/13, 125/125 o
9/9 gia concluse.

Decisione: correzione **IMPLEMENTATO**, test differenziali **ESEGUITO**,
sicurezza tipi JSON **VALIDATO offline**. TSC V1, planner V1, retrieval,
runner, prompt, API e pannello invariati. Runtime, integrazione e
certificazione **BLOCCATO**; nessuna inferenza, retry, repair, deploy o merge.

## RD-TSC-V2-GENERATIVE-HANDOFF-IMPLEMENTATION-01 — Blocco pre-implementativo (2026-11-03)

Attivita: riconciliare il piano implementativo approvato con planner V1 e
dominio V2 prima di modificare i quattro file tecnici. Script: nessuno
modificato o eseguito. Report:
`docs/tactical-state-contract-v2-generative-handoff-blocker-01.md`.

Risultato: `relation_requirements()` puo produrre una fase esplicita
`negative_transition`, mentre `build_question_plan()` materializza soltanto
`state:initial` con fase `unknown`. Il contratto approvato impone di risolvere
`phase_state_ref` soltanto su stati gia presenti nel question plan e vieta di
derivare nuovi state ID. L'handoff non puo quindi soddisfare il contratto per
le relazioni esplicite di fase senza rendere il caso `not_evaluable` o
modificare planner/dominio fuori perimetro.

Decisione: arresto fail-closed prima dell'implementazione. Handoff generativo
TSC V2 **BLOCCATO** in attesa di una decisione separata del titolare; dominio
TSC V2 precedente resta **VALIDATO offline**. Nessun test, inferenza, retry,
repair, Ollama, Chroma, API, deploy o merge eseguito; TSC V1, planner,
dominio V2, retrieval, runner, prompt e pannello invariati.

## RD-TSC-V2-GENERATIVE-HANDOFF-IMPLEMENTATION-01 — implementazione offline (2026-11-03)

Attivita: sbloccare il phase-state nel solo applied plan V2 e implementare l'handoff
generativo opt-in senza modificare planner V1 o dominio V2. Script:
`scripts/v5_tactical_state_generation_v2.py`, integrazioni mirate in
`scripts/smoke_test_rag_v5_e2e.py` e `scripts/run_rag_v5_query.py`; test:
`tests/test_v5_tactical_state_generation_v2.py`. Commit tecnico `307064c`.
Risultato: materializzazione deterministica `state:phase:<canonical_phase>`, uno stato
per fase compatibile, question plan originale immutato, preflight fail-closed,
massimo una chiamata trasporto simulata e zero repair. Eseguiti esclusivamente i 13
test differenziali della nuova suite: 13/13 PASS; `git diff --check` PASS. Report:
`docs/tactical-state-contract-v2-generative-handoff-offline-01.md`. Decisione: codice
**IMPLEMENTATO**, test **ESEGUITO**, proprieta differenziali **VALIDATO offline**.
Nessuna inferenza Qwen/Ollama, query Chroma/API, runtime o deploy; integrazione e
certificazione restano **BLOCCATO**.

## RD-TSC-V2-GENERATIVE-HANDOFF-REMEDIATION-01 — fail-closed offline (2026-11-03)

Attivita: correggere esclusivamente troncamento, audit negativo e relazioni
malformate nel percorso generativo TSC V2. Script:
`scripts/v5_tactical_state_generation_v2.py`; test:
`tests/test_v5_tactical_state_generation_v2.py`; commit tecnico `8a16a73`.
Risultato: `done_reason=length` e `not_evaluable` salvo violazioni dimostrate;
un audit richiede completezza e assenza di segnali negativi; il confronto canonico
restituisce errori strutturati per container, riferimenti e termini malformati.
Eseguiti soltanto i tre nuovi casi differenziali, 3/3 PASS in 0,015 s, e una
regressione positiva direttamente interessata, 1/1 PASS in 0,097 s. Non ripetuta la
campagna 13/13; `git diff --check` PASS. Report:
`docs/tactical-state-contract-v2-generative-handoff-remediation-01.md`. Decisione:
remediation **IMPLEMENTATO**, test **ESEGUITO**, proprieta **VALIDATO offline**;
runtime, integrazione e certificazione **BLOCCATO**. Nessuna inferenza o accesso
Ollama/Chroma/API.

## RD-TSC-V2-RUNTIME-GATE-PREFLIGHT-01 — preflight statico (2026-11-03)

Attivita: definire senza esecuzione il primo Gate runtime del percorso
`--tactical-state-contract-v2`. Script: nessuno eseguito; ispezionati wrapper,
runner, handoff V2 e documentazione consolidata. Report:
`docs/tactical-state-contract-v2-runtime-gate-preflight-01.md`. Risultato: confermati
flag opt-in, mutua esclusione pre-runtime, preflight deterministico, una sola chiamata
possibile, zero retry/repair, diagnostica e promozione fail-closed. Selezionato un
caso minimo di transizione negativa, distinto dal Gate FIGC5, e predisposto comando
non eseguito. Decisione: **BLOCCATO** per assenza di un checkout runtime attestato
alla baseline `965d6b6` e di una conferma live corrente della collection candidata
e del count 6410. Nessuna inferenza, Chroma/API, test E2E o modifica tecnica.

## RD-TSC-V2-RUNTIME-STAGING-PREFLIGHT-01 — staging/metadata preflight (2026-11-03)

Attivita: verificare staging, ambiente e collection prima del Gate V2. Script:
sole letture SSH metadata-only e un tentativo autorizzato di clone indipendente;
nessun test o Gate. Report:
`docs/tactical-state-contract-v2-runtime-staging-preflight-01.md`. Risultato:
parent staging regolare con spazio disponibile, staging V1 esistente ma non idoneo,
commit `965d6b6` assente dai repository VPS. Il clone diretto GitHub e fallito per
autenticazione public key prima del checkout e non ha lasciato il target. Checkout
operativo invariato a `1a80fe0`; Python 3.12.3, time e timeout presenti. Per arresto
fail-closed non e stata aperta la collection e il count corrente non e attestato.
Decisione: staging/preflight/Gate/integrazione/certificazione **BLOCCATO**. Nessuna
inferenza, Chroma/API, servizio, codice o checkout operativo modificato.

## RD-TSC-V2-GIT-BUNDLE-TRANSFER-01 — staging isolato (2026-11-03)

Attivita: trasferire in modo verificabile la baseline tecnica TSC V2 senza usare le
credenziali GitHub della VPS. Bundle locale/remoto: 1926658 byte, SHA-256
`70f7f5b4325513f78f4f42480bb7654bd4f9145398fd8b3b58b5e07b4c848e7d`;
`git bundle verify` PASS su entrambi, storia completa e ref del branch a `6526384`.
Clone indipendente creato in
`/home/football/.local/share/football-data-lab/staging/tsc-v2-965d6b6`, detached
HEAD `965d6b6`, status pulito, `.git` autonomo e nessun alternate. Evaluation regolare
e scrivibile; quattro artefatti Gate assenti. Fingerprint HEAD/status del checkout
operativo e dello staging V1 invariati. Report:
`docs/tactical-state-contract-v2-git-bundle-transfer-01.md`. Decisione: bundle e
staging **VALIDATO**; collection, Gate, integrazione e certificazione **BLOCCATO**.
Nessuna inferenza, Chroma/API, test E2E, servizio o checkout preesistente modificato.

## RD-TSC-V2-RUNTIME-PREREQUISITES-01 — collection/ambiente (2026-11-03)

Attivita: attestare collection candidata e compatibilita Python senza Gate. Metodo:
SQLite stdlib URI `mode=ro&immutable=1`, `PRAGMA query_only=ON`, schema osservato e
conteggio aggregato `collections → segments → embeddings`; nessun PersistentClient,
documento, embedding o retrieval letto. Risultato: collection
`dribbling_tactics_v5_multisource_drive11_figc5_candidate_v1`, dimensione 1024,
count logico 6410. Database invariato prima/dopo per SHA-256
`0d19fbea4df3c4f418e7b55c182c0e268862a53d4f903ddc6cd8a7fe8e74a35b`, size,
mtime e sidecar assenti. Python 3.12.3; chromadb 1.5.9,
llama-index-embeddings-ollama 0.10.0 e sentence-transformers 6.1.0 presenti;
sei file staging analizzati con AST senza import applicativi. Checkout invariati e
artefatti Gate assenti. Report:
`docs/tactical-state-contract-v2-runtime-prerequisites-01.md`. Decisione:
prerequisiti **VALIDATO**; Gate **DA FARE** previa autorizzazione, integrazione e
certificazione **BLOCCATO**. Nessuna inferenza, query semantica o servizio modificato.

## RD-TSC-V2-RUNTIME-GATE-01 — prima esecuzione controllata (2026-11-03)

Attivita: eseguire una sola volta il Gate V2 sulla candidata FIGC5 dopo preflight
positivo. Script: comando approvato con `--legacy-profile` e
`--tactical-state-contract-v2`; nessun retry/repair. Report:
`docs/tactical-state-contract-v2-runtime-gate-01.md`. Risultato: exit 1,
`overall_status=blocked`, `done_reason=stop`, una risposta Qwen osservata dal client,
raw 5015 caratteri, answer vuota. Preflight `ready` e question compatibility
`passed`; struttura V1/V2, operational coverage, blocchi canonici e audit non
superati. Motivi: `invalid_operational_term_identity`, requisito esplicito omesso,
blocco canonico divergente, prosa non canonica e audit fallito. Quattro artefatti
integri; count 6410/6410. Anomalia: stesso size e nessun sidecar, ma hash/mtime di
`chroma.sqlite3` cambiati fra pre e post; causa non determinata. Decisione: singola
esecuzione **ESEGUITO**, fail-closed **VALIDATO**, Gate complessivo/integrazione/
certificazione **BLOCCATO**. Nessun secondo tentativo, deploy o modifica correttiva.

## RD-TSC-V2-RUNTIME-GATE-FORENSIC-01 — revisione statica (2026-11-03)

Attivita: analizzare offline l'unico Gate V2 usando esclusivamente artefatti, codice
alla baseline e report esistenti. Script: nessuno eseguito; nessun test, inferenza o
accesso Chroma/API. Report:
`docs/tactical-state-contract-v2-runtime-gate-forensic-01.md`. Risultato: gli SHA-256
dei quattro artefatti coincidono prima/dopo; dimostrate violazioni generative
dell'identita dei termini e del blocco canonico. Il requisito esplicito e presente
nel raw ma la relazione invalida viene esclusa dall'indice di copertura: la successiva
etichetta `explicit_operational_requirement_omitted` e diagnostica fuorviante, pur
restando corretti fallimento della copertura e fail-closed. Audit negativo confermato;
ripartizione completa fra output e compatibilita col formato canonico non determinata.
La variazione hash di `chroma.sqlite3` non e attribuibile al Gate o a client
concorrenti e il count 6410 e solo un controllo logico. Decisione: revisione forense
**VALIDATO**; Gate, integrazione e certificazione **BLOCCATO**. Proposta, non
implementata: distinguere offline relazione omessa da presente-ma-invalida.

## RD-TSC-V2-AUDIT-CONTRACT-COMPATIBILITY-01 — revisione contrattuale (2026-11-03)

Attivita: ricostruire dal codice alla baseline `965d6b6` l'intersezione fra formato
canonico TSC V2 e `audit_answer()` V1. Script: nessuno eseguito; nessun test,
inferenza, retrieval o accesso runtime. Report:
`docs/tactical-state-contract-v2-audit-compatibility-01.md`. Risultato: intersezione
generale dimostrabilmente non vuota solo quando i source term autorizzati contengono
tutti i cue lessicali audit. Per il piano `tscv2gate01` l'intersezione e vuota: il
blocco canonico esatto non contiene i quattro dettagli obbligatori di transizione
negativa e non puo aggiungerli senza cambiare piano o produrre prosa non canonica.
Decisione: revisione **VALIDATO**; raccomandata Opzione D, piano canonico e spiegazione
documentale separata ma collegata, entrambi fail-closed. Decisione architetturale non
ancora approvata; nessuna implementazione. Gate, integrazione e certificazione
**BLOCCATO**.

## RD-TSC-V2-DUAL-OUTPUT-DESIGN-01 — specifica architetturale (2026-11-03)

Attivita: progettare la separazione fra piano canonico V2 e spiegazione documentale
senza modificare V1 o audit V1. Script: nessuno eseguito; nessun test, runtime o
modifica tecnica. Report: `docs/tactical-state-contract-v2-dual-output-design-01.md`.
Risultato: raccomandata D3 opt-in. Il sistema mantiene piano autorevole, fingerprint
e rendering; Qwen produce una explanation strutturata con relation, requirement ed
evidence refs e claim. Audit V1 riceve tramite adattatore soltanto la prosa; il suo
PASS e necessario ma non sufficiente. Riferimenti, copertura, polarita, citazioni,
supporto e coerenza hanno controlli separati; semantica non dimostrabile resta
`not_evaluable`, nessuna partial promotion. Decisione: specifica **VALIDATO**;
implementazione **DA FARE** e soggetta ad approvazione. Gate, integrazione e
certificazione **BLOCCATO**.

## RD-TSC-V2-DUAL-OUTPUT-IMPLEMENTATION-01 — implementazione offline (2026-11-03)

Attivita: implementare D3 opt-in senza cambiare V1, dominio V2, planner o audit V1.
Script: `scripts/v5_tactical_state_dual_output_v1.py`, integrazione isolata in
`scripts/smoke_test_rag_v5_e2e.py` e `scripts/run_rag_v5_query.py`; test:
`tests/test_v5_tactical_state_dual_output_v1.py`; commit tecnico `f544589`; report:
`docs/tactical-state-contract-v2-dual-output-implementation-01.md`. Risultato: piano,
fingerprint e rendering restano sistemici; Qwen puo produrre soltanto explanation con
refs e claim. Schema, cardinalita, copertura, sei dimensioni, polarita, citazioni,
anchor, audit e promozione sono fail-closed. Anchor presente non equivale a supporto:
senza assessment affidabile `not_evaluable`; bounded inference/uncertainty non sono
promossi. Nuovi differenziali 17/17 PASS e regressione V2 direttamente interessata
16/16 PASS; `git diff --check` PASS. Decisione: D3 **IMPLEMENTATO**, test **ESEGUITO**,
proprieta deterministiche **VALIDATO offline**. Supporto semantico automatico, Gate,
integrazione e certificazione **BLOCCATO**. Nessun runtime, Qwen, retrieval, Chroma,
API/pannello o deploy.

## RD-TSC-V2-D3-SEMANTIC-SUPPORT-DESIGN-01 — progettazione statica (2026-11-03)

Attivita: individuare il meccanismo minimo di support assessment indipendente dal
generatore. Script: nessuno eseguito; nessun test, modello, retrieval o runtime.
Report: `docs/tactical-state-contract-v2-semantic-support-design-01.md`. Risultato:
ID, anchor, bindings, polarita e audit esistenti non provano entailment; NLI shadow,
Gemini/Groq e Gold/human workflow sono riutilizzabili ma nessuno e oggi VALIDATO come
gate D3. Raccomandata S3 incrementale, prima fase S1-only: statement/span atomico,
assessment content-addressed prodotto fuori dal payload Qwen e supported automatico
solo per exact atomic quotation; parafrasi e bounded inference restano
`not_evaluable`, contraddizioni dimostrate `unsupported`. NLI/reviewer restano shadow,
S4 umano serve gold/adjudication. Decisione: design **VALIDATO**, implementazione
**DA FARE** previa approvazione. D3 semantic support, Gate, integrazione e
certificazione **BLOCCATO**.

## RD-TSC-V2-D3-SEMANTIC-SUPPORT-S1-IMPLEMENTATION-01 — checker offline (2026-11-03)

Attivita: sostituire l'assessment sintetico D3 con un produttore S1 deterministico e
content-addressed, limitato alla classe exact atomic. Script:
`scripts/v5_tactical_semantic_support_s1.py`; integrazione esclusiva nel percorso D3
opt-in e commit tecnico `de457a9`. Il claim richiede statement/span NFC semiaperto,
conditions e requirement refs; digest di piano, statement ed evidenze, allowlist e
config fingerprint sono ricalcolati prima del consumo. Il payload modello non puo
autocertificarsi. Supported richiede un'unica evidenza/anchor e l'identita dell'intera
unita documentale; casi fuori copertura restano `not_evaluable`. Nessuna regola
negativa affidabile era disponibile: `unsupported` non e stato inventato. Test S1/D3
29/29 e regressioni TSC V2 43/43, totale 72/72 PASS; diff check PASS. Report:
`docs/tactical-state-contract-v2-semantic-support-s1-implementation-01.md`.
Decisione: checker **IMPLEMENTATO**, test **ESEGUITO**, proprieta coperte **VALIDATO
offline**. S2, Gate, integrazione e certificazione **BLOCCATO**; nessuna inferenza,
NLI, retrieval, Chroma/API, pannello o deploy.

## RD-TSC-V2-D3-SEMANTIC-SUPPORT-S2-READINESS-01 — ricognizione statica (2026-11-03)

Attivita: valutare i candidati S2 esistenti senza eseguire modelli o test. Script:
nessuno eseguito; letti NLI diretto V2, alignment, Ragas Faithfulness, reviewer
Gemini/Groq, contratti Gold E/V e worksheet. Report:
`docs/tactical-state-contract-v2-semantic-support-s2-readiness-01.md`. Risultato:
NLI V2 ha contratto a tre label e dataset riutilizzabili, ma i report principali
sono solo registrati nel manifest content-addressed, non presenti nel ramo; il gold
non e indipendente, lo stesso Qwen del generatore riduce l'indipendenza e i controlli
atomic/contrastive/alignment documentano errori su scope, quantificatori e opposizioni.
Gemini/Groq non hanno calibrazione claim-level; Ragas e binario/due chiamate; Gold E/V
ha zero casi ed e relazionale, non Gold S2. Decisione **B**: NLI V2 riutilizzabile
soltanto in shadow; readiness **ESEGUITO**, nessuna promozione a **VALIDATO** per S2.
Recuperare prima i report storici verificandone gli hash, poi predisporre un Gold S2
indipendente con doppia review/adjudication/freeze; nessuna nuova inferenza implicita.
S2, Gold S2, Gate, integrazione e certificazione **BLOCCATO**.

## RD-TSC-V2-D3-S2-HISTORICAL-EVIDENCE-RECOVERY-01 — riconciliazione probatoria (2026-11-03)

Attivita: recuperare gli originali NLI/alignment gia eseguiti senza rigenerarli.
Script: nessun test o benchmark; sole ricerche nominali, letture e confronti metadata
in Git/storia, checkout locali, allegati e checkout operativo/staging V1/V2 sulla VPS.
Manifest: `evaluation/nli_historical_evidence_reconciliation_v1.json`; report:
`docs/tactical-state-contract-v2-s2-historical-evidence-recovery-01.md`. Risultato:
11 artefatti cercati, 0 verificati, 0 parzialmente verificati, 11 non reperiti e 0
con integrita divergente. Le directory archivio VPS esistono ma contengono soltanto
evidenze FIGC discovery/Drive11 non pertinenti; `evaluation/reports` operativo e
assente. Nessun hash osservato, predizione o matrice e stato ricostruito. Decisione:
ricognizione **VALIDATO** per completezza probatoria; recupero dei singoli originali
**BLOCCATO** fino a un backup/copia nominata e autorizzata. Metriche aggregate e
decisione readiness B invariati; Gold S2, S2, Gate, integrazione e certificazione
**BLOCCATO**. Nessuna inferenza, NLI, reviewer, test, Chroma o modifica runtime.

## RD-TSC-V2-D3-S2-INDEPENDENT-GOLD-DESIGN-01 — progettazione Gold S2 (2026-11-05)

Attivita: progettare senza popolare un Gold S2 claim-evidence indipendente. Script:
nessuno eseguito; sole letture statiche di TODO, registro, readiness/recovery S2,
design e implementazione S1, contratti Gold E/V, provenance, ledger, freeze,
worksheet e dataset/campagne claim-fidelity. Report:
`docs/tactical-state-contract-v2-s2-independent-gold-design-01.md`. Risultato: Gold
E/V e Gold S2 separati formalmente; definiti record a tre label, tassonomia con una
categoria primaria e proprieta trasversali, split raccomandato 606 e ridotto 390,
source/document disjointness, doppia review cieca A/B, adjudication C, QA D,
manifest content-addressed, freeze e protocollo shadow futuro. Nessun caso, label,
annotazione, test o modello prodotto. Decisione: design **VALIDATO**; il titolare deve
decidere volume, fonti/diritti, ruoli e indipendenza autore. Schema/validator e
inventario fonti **DA FARE**; raccolta, annotazione, adjudication, freeze, Gold S2,
S2, Gate, integrazione e certificazione **BLOCCATO** fino ad autorizzazioni separate.

## RD-TSC-V2-D3-S2-SPATIAL-RELATION-REMEDIATION-01 — offline (2026-11-05)

Attivita: implementare una versione NLI isolata per relazioni inverse dopo il
falso positivo `q3_04`. Script:
`scripts/shadow_nli_spatial_relations_v1_inference.py`; commit tecnico
`2934d234868a1f4c6e05e9571a76d7a642eb3b86`; report:
`docs/tactical-semantic-support-s2-spatial-relation-remediation-01.md`.
Risultato: contratto `nli_spatial_relations_v1` richiede identita di soggetto,
referente, condizioni e fase prima di classificare predicati direzionalmente
incompatibili; assenza di supporto resta `insufficient`. Riusa schema/parser V2
solo alla chiamata esplicita; nessun routing o default modificato. Test nuovi
6/6 PASS, compilazione e diff check PASS; V2 invariato per blob e fingerprint
dell'istruzione. Decisione: contratto **IMPLEMENTATO**, test **ESEGUITO**,
isolamento e proprieta statiche **VALIDATO** offline. Efficacia semantica,
integrazione, Gate e certificazione **BLOCCATO**. Nessuna inferenza o runtime.

## RD-TSC-V2-D3-S2-SPATIAL-RELATION-REVIEW-01 — revisione statica (2026-11-05)

Attivita: revisione indipendente del contratto opt-in e dei sei test gia
pubblicati, con confronto integrale contro V2, bridge S2, runner Fase B e report
forense `q3_04`. Script: nessuno eseguito; report:
`docs/tactical-semantic-support-s2-spatial-relation-review-01.md`. Risultato:
nessun rilievo bloccante o maggiore; regole semantiche, trasporto strutturato,
parsing, propagazione degli errori e confine S2 restano fail-closed. V2, bridge,
runner, S1, RAG, Chroma, API e panel invariati. L'esempio letterale vicino a
`q3_04` e un limite probatorio minore: il caso resta regressione nota e non prova
generalizzazione indipendente. Decisione: **REVISIONE FAVOREVOLE**, revisione
**ESEGUITO** e proprieta statiche coperte **VALIDATO**. Efficacia semantica,
Gate, integrazione e certificazione **BLOCCATO**; nessun runtime autorizzato.

## RD-TSC-V2-D3-S2-SPATIAL-RELATION-DIFFERENTIAL-01 — Fase A (2026-11-05)

Attivita: preparare senza inferenze un Gate diagnostico del contratto spatial.
Script:
`scripts/run_tactical_semantic_support_s2_spatial_relation_differential_v1.py`;
fixture:
`evaluation/tactical_semantic_support_s2_spatial_relation_differential_fixture_v1.json`;
commit tecnico `9aac9ea761ba29099332d95fbff7d0f2ee8bf9e8`; report:
`docs/tactical-semantic-support-s2-spatial-relation-differential-preparation-01.md`.
Risultato: selezionati `q3_04` come regressione nota, `q5_06` come controllo
inverso distinto ma correlato e `q5_02` come guardia `insufficient`; label e
contenuti umani invariati. Solo `q3_04` dispone di risultato V2 direttamente
attribuibile. Runner opt-in, massimo tre valutazioni al solo nuovo judge, zero
retry/repair/V2 implicito, output esclusivo, stop al primo `not_evaluable`, S1
invariato e `promotion_authorized=false`. Test differenziali nuovi 6/6 PASS,
compilazione e diff check PASS; nessuna suite storica o inferenza. Decisione:
runner/fixture **IMPLEMENTATO**, verifiche **ESEGUITO**, proprieta offline
coperte **VALIDATO**. Esecuzione reale, efficacia, confronto generale V2,
integrazione e certificazione **BLOCCATO** fino a nuova autorizzazione.

## RD-TSC-V2-D3-S2-SPATIAL-DIFFERENTIAL-FINAL-REVIEW-01 — statica (2026-11-05)

Attivita: chiudere valore probatorio di `q5_06` e tracciabilita runtime senza
inferenze. Script rettificato:
`scripts/run_tactical_semantic_support_s2_spatial_relation_differential_v1.py`;
commit tecnico `3e630a5e6aba2e402adeea01f3f8dc4cf4f6e419`; report:
`docs/tactical-semantic-support-s2-spatial-differential-final-review-01.md`.
Risultato: `q5_06` e controllo distinto ma correlato alla famiglia di inversioni,
non prova indipendente. Sostituito il contatore ambiguo con valutazioni pianificate,
tentate e completate; nessuna pretesa di contare HTTP. `run_complete=true` ed
exit 0 richiedono 3/3 valutazioni tecnicamente valide; errore intercettato produce
report parziale, `not_evaluable`, `run_complete=false` ed exit 2. Test interessati
6/6 PASS, compilazione e diff check PASS; nessuna inferenza. Decisione:
**REVISIONE FAVOREVOLE**, rettifica **IMPLEMENTATO**, revisione **ESEGUITO** e
proprieta coperte **VALIDATO** offline. Runtime, efficacia, integrazione e
certificazione **BLOCCATO** fino a distinta autorizzazione.

## RD-TSC-V2-D3-S2-SPATIAL-RELATION-DIFFERENTIAL-01 — Fase B (2026-11-05)

Attivita: unica esecuzione runtime autorizzata nello staging indipendente
`s2-spatial-differential-0d40719`. Script e configurazione congelati; artefatto:
`evaluation/tactical_semantic_support_s2_spatial_relation_differential_01.json`;
report:
`docs/tactical-semantic-support-s2-spatial-relation-differential-runtime-01.md`.
Risultato: preflight PASS, 66,35 s, exit 0, `planned/attempted/completed=3/3/3`,
`run_complete=true`, S1 invariato e non-promozione 3/3. Corrispondenza Gold 2/3:
`q5_06 contradicted`, `q5_02 insufficient`, ma `q3_04 supported` resta il falso
positivo storico. JSON 13.138 byte, SHA-256 `a06ba357...`; quattro artefatti
verificati. Nessun retry, repair o judge V2. Anomalia: il bridge riutilizzato
mantiene nome/rationale testuali V2 nei record annidati, mentre descriptor,
runtime config e import attestano il callable spatial. Decisione: esecuzione
**ESEGUITO**, completamento tecnico **VALIDATO** nel singolo run; corrispondenza
complessiva, affidabilita, integrazione e certificazione **BLOCCATO**. Nessun
rerun autorizzato; prossimo passo soltanto revisione offline indipendente.

## RD-TSC-V2-D3-S2-SPATIAL-DIFFERENTIAL-FORENSIC-01 — offline (2026-11-06)

Attivita: ricostruire senza modelli il falso positivo `q3_04` e verificare la
provenance del bridge. Script: nessun test/runtime; sole letture e calcoli
deterministici. Report:
`docs/tactical-semantic-support-s2-spatial-differential-forensic-01.md`.
Risultato: JSON 13.138 byte SHA-256 `a06ba357...`, fixture/Gold/fingerprint e tre
record conformi. Prompt ricostruito 2.386 byte SHA-256 `597088f1...`; nessuna
perdita, normalizzazione, inversione, troncamento o rimappatura dimostrata.
Routing al callable spatial e nessuna chiamata V2 dimostrati; il falso
`supported` e fortemente localizzato nel giudizio semantico, mentre il meccanismo
interno resta non determinabile per assenza di raw request/response e rationale.
Il bridge mantiene nome, `nli_contract` e rationale fissa V2: difetto dimostrato
di provenance strutturata, non di routing. Decisione: revisione **ESEGUITO**,
integrita/routing/ricostruzione **VALIDATO** offline; provenance autonoma,
semantica complessiva, affidabilita, integrazione e certificazione **BLOCCATO**.
Prossimo passo unico: rettifica offline minima della provenance, senza nuovo Gate.

## RD-TSC-V2-D3-S2-Q3-04-SEMANTIC-DESIGN-01 — design (2026-11-07)

Attivita: progettazione statica di una remediation semantica generalizzabile per
`q3_04`. Script/test: nessuno; report:
`docs/tactical-semantic-support-s2-q3-04-semantic-design-01.md`. Risultato:
Spatial V1 contiene già istruzioni relazionali ma restituisce soltanto la label;
altro prompt, regola lessicale e repair non aggiungono verifica sufficiente.
Raccomandato futuro contratto opt-in `nli_spatial_relations_v2` con relation
witness ancorato e validatore deterministico della coerenza label/witness. La
nuova proprietà è osservabilità/falsificabilità, non accuratezza già dimostrata;
`q3_04` da solo non prova generalizzazione. Decisione: **PROCEDERE CON SPECIFICA
OFFLINE VERSIONATA**; design **ESEGUITO**, specifica/implementazione **DA FARE**,
efficacia, Gate, integrazione e certificazione **BLOCCATO**; closeout provenance
V1 **VALIDATO**. Nessun test o inferenza.

## RD-TSC-V2-D3-S2-BRIDGE-PROVENANCE-CLOSEOUT-01 — closeout (2026-11-07)

Attivita: closeout documentale formale autorizzato dal titolare. Script/test:
nessuno eseguito; report:
`docs/tactical-semantic-support-s2-bridge-provenance-closeout-01.md`. Catena:
implementazione `33b5c7a`, review `40de750`, remediation `f953496`, approvazione
indipendente `93b88a3`. Risultato: provenance content-addressed, fail-closed,
immutabilità, binding AST, SHA storici e non-promozione **VALIDATO** offline;
test differenziali 14/14 già **ESEGUITO**, non ripetuti. Decisione:
**CLOSEOUT OFFLINE DELLA PROVENANCE SPATIAL V1 APPROVATO** e **VALIDATO**. Il
Gate storico resta 2/3 con `q3_04` errato; Gate semantico, integrazione e
certificazione **BLOCCATO**. Nessuna inferenza o modifica applicativa.

## RD-TSC-V2-D3-S2-BRIDGE-PROVENANCE-REMEDIATION-REVIEW-01 — review (2026-11-07)

Attivita: review statica conclusiva M1-M3. Script/test: nessuno eseguito;
report:
`docs/tactical-semantic-support-s2-bridge-provenance-remediation-review-01.md`.
Risultato: tipi originali verificati prima della canonicalizzazione; descriptor
interno conservato solo come JSON immutabile; AST collega import, closure,
Spatial judge e Spatial bridge; tre SHA congelati letti sui byte e verificati
con `hashlib`. Test pubblicati pertinenti e sufficienti; nessuna criticità
residua. Decisione: **REMEDIATION APPROVATA — CLOSEOUT OFFLINE AUTORIZZABILE**;
review **ESEGUITO**, remediation **IMPLEMENTATO**, proprietà offline
**VALIDATO**; closeout formale **DA FARE**, Gate, integrazione e certificazione
**BLOCCATO**. Nessun test, inferenza o modifica applicativa.

## RD-TSC-V2-D3-S2-BRIDGE-PROVENANCE-REMEDIATION-01 — offline (2026-11-07)

Attivita: remediation minima M1-M3. Script: solo bridge Spatial; test: bridge e
runner Spatial; report:
`docs/tactical-semantic-support-s2-bridge-provenance-remediation-01.md`.
Risultato: tipi originali del descriptor verificati prima della
canonicalizzazione; provenance interna memorizzata come JSON immutabile; call
graph closure/Spatial judge/Spatial bridge provato via AST; SHA di bridge V2,
runner V2 e JSON storico verificati sui byte con `hashlib`. Test differenziali
**14/14 PASS**. Runner Spatial, V2 e artefatti invariati. Decisione: rettifiche
**IMPLEMENTATO**, test **ESEGUITO**, proprietà offline **VALIDATO**; closeout
definitivo **DA FARE**, Gate, integrazione e certificazione **BLOCCATO**. Nessuna
inferenza o runtime.

## RD-TSC-V2-D3-S2-BRIDGE-PROVENANCE-IMPLEMENTATION-REVIEW-01 — review (2026-11-06)

Attivita: revisione statica indipendente dell'adattatore Spatial pubblicato.
Script/test: nessuno eseguito; report:
`docs/tactical-semantic-support-s2-bridge-provenance-implementation-review-01.md`.
Risultato: routing Spatial, assenza fallback, boundary S2, proiezione, rationale,
digest e hash storici confermati. Tre rettifiche maggiori: il tipo originale di
`labels` può essere normalizzato prima della validazione; il dict privato del
descriptor resta mutabile nonostante la dataclass frozen; i test non provano il
target della closure né gli SHA storici. Decisione: **IMPLEMENTAZIONE APPROVATA
CON RETTIFICHE**; review **ESEGUITO**, codice **IMPLEMENTATO**, closeout offline,
Gate, integrazione e certificazione **BLOCCATO**. Nessun test, inferenza o
modifica applicativa.

## RD-TSC-V2-D3-S2-BRIDGE-PROVENANCE-IMPLEMENTATION-01 — offline (2026-11-06)

Attivita: implementazione alternativa B con M1/M2. Script: nuovo
`scripts/v5_tactical_semantic_support_s2_spatial_v1_bridge.py` e solo
import/build del runner Spatial; test: nuovo bridge e runner Spatial. Report:
`docs/tactical-semantic-support-s2-bridge-provenance-implementation-01.md`.
Risultato: identità dichiarata distinta dal binding esplicito del runner;
descriptor/config a shape, tipi e valori esatti, validati fail-closed alla
costruzione; copie difensive, proiezione condivisa, label non rimappate e nota
tecnica non semantica. Test mirati **14/14 PASS**. Bridge e runner V2
byte-invariati; JSON storico SHA-256 `a06ba357...` invariato; digest config e
record sintetici verificati. Decisione: adapter **IMPLEMENTATO**, test
**ESEGUITO**, proprietà offline **VALIDATO**; Gate semantico, integrazione e
certificazione **BLOCCATO**. Nessuna inferenza o runtime.

## RD-TSC-V2-D3-S2-BRIDGE-PROVENANCE-DESIGN-REVIEW-01 — revisione (2026-11-06)

Attivita: revisione statica indipendente del design dell'adattatore Spatial.
Script/test: nessuno eseguito; report:
`docs/tactical-semantic-support-s2-bridge-provenance-design-review-01.md`.
Risultato: alternativa B confermata; nessun blocco architetturale. Due rettifiche
maggiori obbligatorie: il callable generico non può essere autenticato dal solo
bridge, quindi identità dichiarata e binding staticamente verificabile vanno
distinti; descriptor e config richiedono shape, tipi, valori e coerenza esatti,
validati fail-closed alla costruzione. Compatibilità S2/V2 e matrice digest
verificate; rationale tecnica e stabilità della proiezione classificate minori.
Decisione: **DESIGN APPROVATO CON RETTIFICHE**; revisione **ESEGUITO**, design
**VALIDATO** con rettifiche, implementazione **DA FARE**; Gate, integrazione e
certificazione **BLOCCATO**. Nessun codice, test, inferenza o runtime.

## RD-TSC-V2-D3-S2-BRIDGE-PROVENANCE-DESIGN-01 — design (2026-11-06)

Attivita: progettare senza implementare la rettifica della provenance del bridge
S2. Script: nessuno; report:
`docs/tactical-semantic-support-s2-bridge-provenance-design-01.md`. Risultato:
due chiamanti applicativi (`run_*first_controlled*` V2 e runner differenziale
Spatial), S2 richiede rationale non vuota e content-addressa descriptor/rationale.
Confrontate A parametrizzazione del bridge V2 e B adattatore Spatial dedicato;
raccomandata B per lasciare byte-invariati bridge, descriptor, test e runner V2.
Interfaccia proposta valida callable/config/contract descriptor; provenance
Spatial esplicita e avviso rationale adapter-generated senza reasoning. Contratto,
fixture, Gold, plan fingerprint e artefatti storici invariati; solo futuri judge
config/rationale/record hash Spatial cambiano legittimamente. Decisione: **DESIGN
APPROVABILE**, progettazione **ESEGUITO**, implementazione **DA FARE**; semantica,
Gate, integrazione e certificazione **BLOCCATO**. Nessun test, runtime o modifica
applicativa.

## RD-TSC-V2-D3-S2-Q3-04-FORENSIC-01 — analisi offline (2026-11-05)

Attivita: attribuire il falso positivo reale `q3_04` usando soltanto artefatto,
dataset e codice pubblicati. Script: nessuno eseguito; report:
`docs/tactical-semantic-support-s2-q3-04-forensic-01.md`. Risultato: SHA-256
artefatto `0768ca58...` conforme; claim/evidenza e digest riconciliati; input NLI
ricostruito integralmente. Fonte `toglie spazio` e claim `lascia molto spazio`
sono incompatibili sullo stesso soggetto e spazio. Ordine, serializzazione,
mapping, parsing e fail-closed corretti; nessun fallback o troncamento osservato.
Decisione: causa **B, errore semantico del judge**, con ragionamento interno non
determinabile per assenza di raw response/rationale; analisi **ESEGUITO** e
ricostruzione **VALIDATO** offline. Unica remediation proposta, non implementata:
contratto versionato che renda esplicito il controllo della direzione relazionale.
Correzione **DA FARE**; affidabilita, Gate, integrazione e certificazione
**BLOCCATO**. Nessuna inferenza, test o modifica applicativa.

## RD-TSC-V2-D3-S2-FIRST-CONTROLLED-RUNTIME-01 — Fase B (2026-11-05)

Attivita: eseguire una sola osservazione reale D3→S2→NLI V2→Qwen 3.5 9B nella
modalita shadow gia predisposta. Script e baseline invariati; artefatto:
`evaluation/tactical_semantic_support_s2_first_controlled_runtime_01.json`;
report: `docs/tactical-semantic-support-s2-first-controlled-runtime-01.md`.
Risultato: preflight PASS; run unico 52 s, exit 0, 3/3 inferenze, zero errori,
retry o repair. Valutazioni tecniche 3/3, S1 invariato e non-promozione 3/3;
corrispondenza semantica 2/3: `q3_04` falso positivo `supported` rispetto a
`contradicted`. Artefatto 11.639 byte, SHA-256 `0768ca58...`. Decisione: Fase B
**ESEGUITO**; funzionamento e isolamento **VALIDATO** per il solo tentativo;
affidabilita semantica, Gold S2, Gate, integrazione e certificazione **BLOCCATO**.
Nessun rerun autorizzato; prossimo passo possibile solo analisi offline distinta.

## RD-TSC-V2-D3-S2-FIRST-CONTROLLED-RUNTIME-01 — digest cross-platform (2026-11-05)

Attivita: correggere il solo mismatch CRLF/LF mantenendo la verifica byte-for-byte.
Script: runner invariato; `.gitattributes` limita `text eol=lf` al dataset;
fixture e aspettativa del test aggiornate al digest blob `8e3933f...`; commit
tecnico `596bc3c6808bbd2d6d9353a0ef8eff823883a605`; report:
`docs/tactical-semantic-support-s2-cross-platform-digest-remediation-01.md`.
Risultato: blob Git `4523eb7...`, 7.612 byte e JSON invariati; clone Windows
fresco con `core.autocrlf=true` materializza 139 LF, zero CRLF e digest conforme;
dataset Linux gia presente osservato con stessi byte/digest. Test mirati 4/4
PASS, incluso rifiuto di un digest alterato. Decisione: remediation
**IMPLEMENTATO**, verifiche **ESEGUITO**, proprieta coperte **VALIDATO** nel
perimetro dichiarato. Staging Linux non aggiornato; Fase B **DA FARE** e
**BLOCCATO** fino ad autorizzazione distinta. Nessuna inferenza o modifica VPS.

## RD-TSC-V2-D3-S2-FIRST-CONTROLLED-RUNTIME-01 — preparazione offline (2026-11-05)

Attivita: predisporre, senza inferenze, il primo esperimento reale controllato
D3→S2 Shadow Adapter→NLI V2 Bridge. Script:
`scripts/run_tactical_semantic_support_s2_first_controlled_runtime_v1.py`;
fixture content-addressed:
`evaluation/tactical_semantic_support_s2_first_controlled_runtime_fixture_v1.json`;
commit tecnico `c985a916b35f88633cb37778a7a429fca218c807`; report:
`docs/tactical-semantic-support-s2-first-controlled-runtime-preparation-01.md`.
Risultato: selezionati tre casi umani gia versionati, uno per label canonica;
massimo tre chiamate, zero retry/repair, arresto al primo `not_evaluable`, S1
invariato e `promotion_authorized=false`. Test offline nuovi e regressioni
direttamente interessate 20/20 PASS; guardia senza `--execute`, compilazione e
diff check PASS. Nessuna inferenza o artefatto runtime prodotto. Decisione:
runner/fixture **IMPLEMENTATO**, test **ESEGUITO**, isolamento e fail-closed
**VALIDATO** offline. Fase B **DA FARE** e **BLOCCATO** fino ad autorizzazione
separata e ambiente conforme; il Python locale corrente e privo di `pydantic`.
Accuratezza semantica, Gold S2, Gate, integrazione e certificazione **BLOCCATO**.

## RD-TSC-V2-D3-S2-GOLD-SCHEMA-VALIDATOR-01 — implementazione offline (2026-11-05)

Attivita: implementare esclusivamente schema, manifest e validatore Gold S2 V1.
Script: `scripts/validate_tactical_semantic_support_gold_s2_v1.py`; commit tecnico
`d0808df`; report:
`docs/tactical-state-contract-v2-s2-gold-schema-validator-01.md`. Risultato: nuovi
contratti separati da Gold E/V, template draft con zero casi, canonicalizzazione
RFC 8785/NFC versionata, digest di fonte/evidenza/claim/caso/dataset, riferimenti,
split contamination, review A/B/C, QA D, autorizzazione e manifest frozen verificati
fail-closed. I digest senza contenuto restano `unverifiable` e non possono sostenere
un frozen. Test differenziali esclusivamente sintetici 18/18 PASS; nessuna suite
storica ripetuta. Decisione: schema/validator **IMPLEMENTATO**, test **ESEGUITO** e
proprieta deterministiche coperte **VALIDATO offline**. Nessuna correttezza semantica
delle label e attestata; nessun caso reale, annotazione o freeze prodotto. Inventario
fonti **DA FARE**; Gold S2, raccolta, annotazione, adjudication, freeze reale, S2,
Gate, integrazione e certificazione **BLOCCATO**. D3/S1, Gold E/V e readiness B
invariati; nessun modello, benchmark, retrieval o runtime.

## RD-TSC-V2-D3-S2-SOURCE-INVENTORY-01 — ricognizione metadata-only (2026-11-05)

Attivita: inventariare esclusivamente fonti gia note e identificabili da evidenze
Git, senza leggere contenuti documentali o interrogare collection. Script: nessun
test/runtime; sole letture e riconciliazioni di JSON, manifest, report e registri.
Manifest: `evaluation/gold_s2_source_inventory_v1.json`; report:
`docs/tactical-state-contract-v2-s2-source-inventory-01.md`. Risultato: 34 fonti
individuali, tutte collegate a riferimenti esistenti; 5 metadata verified, 29
documented partial, 0 diritti verificati e 0 holdout attestati. I conteggi corpus
141/157 restano aggregati non scomponibili dal repository e non sono stati gonfiati
in record. Tutte le fonti hanno rischio di contaminazione alto per uso noto o storia
incompleta; `unknown` non e stato convertito in assenza di utilizzo. Decisione:
ricognizione **VALIDATO** nel perimetro effettivo; selezione e fattibilita 390/606
**BLOCCATO/non dimostrata**. Provenance/diritti reali **DA FARE** previa decisione;
raccolta, annotazione, adjudication, freeze, Gold S2, S2, Gate, integrazione e
certificazione **BLOCCATO**. Nessun download, scraping, modello, benchmark,
retrieval, Chroma o modifica ai contratti esistenti.

## RD-PANEL-RUNTIME-READINESS-AUDIT-01 — audit read-only (2026-11-05)

Attivita: riconciliare il pannello pubblico, il percorso applicativo e il runtime
VPS senza inferenze o modifiche. Script: nessuno eseguito; letture statiche del
repository e una sessione SSH read-only. Report:
`docs/panel-runtime-readiness-audit-01.md`. Risultato: panel HTTPS e health HTTP
200; API, worker, Nginx e Ollama attivi; queue depth 0; catalogo FIGC5 caricato a
6.410 chunk e 157 documenti; zero unita fallite, disco al 33% e circa 14 GiB RAM
disponibili. Il checkout operativo e detached a `1a80fe0c`, contiene artefatti non
tracciati ed e privo dei moduli TSC V1/V2, handoff V2 e S1; l'API pubblica non
passa flag TSC al runner. Decisione: audit **ESEGUITO**; raccomandato stabilizzare
prima il percorso legacy con deploy riproducibile, smoke singola e rollback, poi
valutare TSC in canale opt-in separato. Piano operativo **DA FARE** previa
autorizzazione; nessuna nuova integrazione o certificazione attribuita.

## RD-TSC-V2-D3-S2-CORPUS-METADATA-ENRICHMENT-01 — metadata-only (2026-11-05)

Attivita: riconciliare esclusivamente da manifest e report Git la linea corpus
141→152→157 senza leggere documenti o interrogare runtime. Script: nessuno;
manifest `evaluation/gold_s2_corpus_metadata_enrichment_v1.json`; report:
`docs/tactical-state-contract-v2-s2-corpus-metadata-enrichment-01.md`. Risultato:
costruzione aggregata documentata come 141 baseline + 11 Drive11 + 5 FIGC5; le
16 aggiunte individuali erano gia incluse nelle 34 fonti precedenti. I file
storici con l'elenco dei 141 non sono presenti in Git: zero nuove identita, zero
mappature individuali aggiuntive, 5 metadata verified/29 partial, diritti 0 e
holdout 0. Decisione: arricchimento **ESEGUITO**, ma fattibilita 390/606 non
dimostrata; provenienza/diritti **DA FARE**, selezione, Gold S2, S2, Gate,
integrazione e certificazione **BLOCCATO**. Nessun download, contenuto, Chroma,
retrieval, modello, benchmark, caso, label o freeze.

## RD-TSC-V2-D3-S2-CATALOG-METADATA-EXPORT-01 — export API (2026-11-05)

Attivita: usare come nuova evidenza il catalogo FIGC5 gia caricato, tramite soli
GET autenticati non generativi e proiezione locale dei campi ammessi. Script:
nessun file operativo; endpoint `/v1/metrics`, `/v1/knowledge/stats` e due pagine
di `/v1/knowledge/documents`. Manifest:
`evaluation/gold_s2_catalog_metadata_export_v1.json`; report:
`docs/tactical-state-contract-v2-s2-catalog-metadata-export-01.md`. Risultato:
157 record unici, somma 6.410 chunk, provenienza operativa completa 157/157,
25 match verificati con le 34 fonti precedenti e 132 identita catalogo nuove.
Esclusi testi, chunk, embedding, percorsi privati e credenziali; Chroma/SQLite non
aperti direttamente. Autore/organizzazione/edizione/lingua/digest/diritti 0/157;
holdout 0. Decisione: export **ESEGUITO**, identita operative **VALIDATO** nel
perimetro API; fattibilita 390/606, selezione, Gold S2 e S2 **BLOCCATO**. Nessun
servizio, checkout, collection o database modificato.

## RD-TSC-V2-D3-S2-INDEPENDENT-SOURCE-ACQUISITION-PLAN-01 — piano (2026-11-05)

Attivita: definire senza acquisizioni un percorso verificabile per nuove fonti
indipendenti Gold S2. Script: nessuno; report:
`docs/tactical-state-contract-v2-s2-independent-source-acquisition-plan-01.md`.
Risultato: politica obbligatoria per identita/versione/provenienza/digest/diritti,
sette canali valutati, screening source-document-version-author disjoint, schema
del registro candidati vuoto, ruoli A/B/C/D separati, roadmap a cancelli e modello
di carico. Nessuna fonte reale, candidato, annotazione o split assegnato. Decisione:
piano **ESEGUITO**; scelta 390/606 rinviata a fonti e pilot misurato (A+B derivati:
130–195 h per 390, 202–303 h per 606, overhead esclusi). Policy/ruoli/registro e
acquisizione **DA FARE** con autorizzazioni distinte; selezione, annotazione,
freeze, Gold S2 e S2 **BLOCCATO**. Nessun download, scraping, contenuto, modello,
benchmark, Gate, VPS o modifica ai contratti.

## RD-S2-CANDIDATE-REGISTRY-V1-01 — implementazione offline (2026-11-05)

Attivita: implementare lo strato preliminare di registrazione e qualificazione
delle fonti candidate Gold S2. Script:
`scripts/validate_gold_s2_source_candidate_registry_v1.py`; commit tecnico
`a49d0ee096a4d0592fb87d893aa1cdd2c5e6d1a9`; report:
`docs/tactical-state-contract-v2-s2-candidate-registry-v1-01.md`. Risultato:
schema Draft 2020-12, template draft vuoto, validatore fail-closed e 17 test
sintetici nuovi, **17/17 PASS**. Verificati ID/riferimenti, digest dichiarato vs
byte-verificato, diritti separati, retention, exposure ledger, indipendenza,
cluster, policy e attribuzione della decisione. Il validatore Gold S2 esistente
resta invariato e nessun candidato/caso/split reale e stato creato. Decisione:
infrastruttura **IMPLEMENTATO**, test **ESEGUITO**, proprieta deterministiche
**VALIDATO offline**; policy e acquisizione **DA FARE**; candidati reali, Gold S2,
freeze e S2 **BLOCCATO**. Nessuna attivita runtime o VPS.

## RD-S2-FIRST-REAL-SOURCE-CANDIDATE-01 — registrazione (2026-11-05)

Attivita: qualificare la sola fonte Frontiers autorizzata, DOI
`10.3389/fspor.2022.1019990`, senza creare casi o split. Script: validatore
Candidate Registry V1 esistente; record:
`evaluation/gold_s2_source_candidate_registry_v1.json`; commit record
`ac7dfe8b2f13dbd72412022d4f8e6f55ae3b1bcd`; report:
`docs/gold-s2-first-real-source-candidate-01.md`. Risultato: pagina/PDF ufficiali
confermano identita, autori, data, DOI e CC BY dichiarata; PDF temporaneo 654208
byte e SHA-256 `8742bfaa21170df3a63ad53c7486ee62e6b39ceef168d6c3bdeab29fdb04bc31`,
match esatto col dato utente. Zero match esatti per DOI/titolo/autori negli
inventari 34/157; questo non prova indipendenza. Validazione mirata `STATUS VALID`,
errori 0. Decisione: registrazione **ESEGUITO**, struttura/digest **VALIDATO**;
candidato `blocked_unknown`, nessuno split; diritti operativi, exposure,
indipendenza, selezione, Gold e S2 **BLOCCATO**. Nessuna attivita VPS/runtime.

## RD-TSC-V2-D3-SEMANTIC-SUPPORT-S2-SHADOW-ADAPTER-01 — offline (2026-11-05)

Attivita: collegare claim D3 ed evidenze a un judge semantico iniettato senza
alterare l'autorita S1. Script: nuovo
`scripts/v5_tactical_semantic_support_s2.py`, hook opt-in in
`scripts/v5_tactical_state_dual_output_v1.py`; commit tecnico
`8aa248957a9c6500861a049c6621ea71aa02bc61`; report:
`docs/tactical-state-contract-v2-d3-semantic-support-s2-shadow-adapter-01.md`.
Risultato: record shadow content-addressed con digest attempt/piano/claim/S1/
evidenze/config, binding autorevoli, label+rationale, aggregazione conservativa,
`promotion_authorized=false`; errori e output malformati `not_evaluable`.
Test nuovi 8/8, regressioni S1 12/12 e dual 17/17 PASS; compilazione e diff check
PASS. Decisione: adapter **IMPLEMENTATO**, test **ESEGUITO**, orchestrazione,
isolamento e fail-closed **VALIDATO offline**. Affidabilita semantica, Gold S2,
Gate, integrazione e certificazione **BLOCCATO**. Nessuna inferenza o runtime.

## RD-TSC-V2-D3-S2-NLI-JUDGE-BRIDGE-01 — offline (2026-11-05)

Attivita: collegare il contratto del judge iniettato S2 al callable storico NLI
V2 senza eseguire modelli e senza modificare l'autorita D3/S1. Script: nuovo
`scripts/v5_tactical_semantic_support_s2_nli_v2_bridge.py`; commit tecnico
`a07b34ff36ccf9a7cc10b10f8d18638aaf7cadc5`; report:
`docs/tactical-state-contract-v2-d3-s2-nli-judge-bridge-01.md`. Risultato:
proiezione deterministica e fail-closed di statement, condizioni, polarita,
binding ed evidenza verso `(claim, evidence)`; mapping limitato alle tre label
canoniche, rationale storica esplicitamente non disponibile, rationale estesa
preservata quando presente, configurazione/provenance content-addressed e nessuna
chiamata implicita. Test mock nuovi 8/8, regressioni S2 8/8 e dual 17/17 PASS;
compilazione e diff check PASS. Decisione: bridge **IMPLEMENTATO**, test
**ESEGUITO**, contratto, isolamento e fail-closed **VALIDATO offline**.
Accuratezza semantica reale, Gold S2, Gate, integrazione e certificazione
**BLOCCATO**. Nessuna inferenza, retrieval, Chroma, API, pannello o runtime.

## RD-S2-FRONTIERS-POLICY-SCREENING-01 — documentale (2026-11-05)

Attivita: predisporre una policy minima non approvata e completare lo screening
documentale della fonte Frontiers DOI `10.3389/fspor.2022.1019990` usando soltanto
evidenze gia registrate e termini ufficiali pubblici. Script: nessuno; report:
`docs/gold-s2-frontiers-policy-screening-01.md`. Risultato: identita, version of
record, digest e dichiarazione CC BY restano verificati; CC BY consente in linea
tecnica riproduzione e adattamento con attribuzione, indicazione delle modifiche
e nessuna restrizione aggiuntiva, ma la decisione operativa umana non e stata
assunta. Zero match esatti nei registri 34/157 non dimostrano disjointness;
esposizione storica, version cluster e author cluster restano `unknown`.
Candidate Registry invariato e validatore non rieseguito. Decisione: screening
**ESEGUITO**; policy e nomina custode **DA FARE**; candidato `blocked_unknown`,
annotazione, split, freeze, Gold S2 e accuratezza S2 **BLOCCATO**. Nessun download,
scraping, annotazione, test, modello, benchmark, runtime o VPS.
