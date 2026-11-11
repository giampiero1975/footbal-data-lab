# Remediation A/R1 — singolo caso Qwen tramite API ufficiale

Data: 2026-11-11. Attività:
`RD-RAG-V5-REMEDIATION-A-OFFICIAL-API-SINGLE-CASE-01`.

## Risultato

**POST inviate: 1. Generazioni completate: 1. Nessun retry, repair o fallback.**

| Livello | Evidenza | Risultato nel perimetro |
|---|---|---|
| Tecnico API | HTTP 200; done=true; done_reason=stop; SSH exit 0; 188,649 s | **VALIDATO** solo per l'elaborazione osservata di questo payload e controllo strutturale locale |
| Extraction | JSON interpretabile; shape_errors=[]; precontrollo semantico superato prima del locator | Struttura accettata, non prova di correttezza rispetto ai testi |
| Witness/semantica | not_evaluable, E_EXTRACTION_LOCALIZATION_NOT_UNIQUE; witness=null; validation=null | Ipotesi di accuratezza sul caso non validata; **BLOCCATO** |
| Label/Gold | proposta supported; label osservata null; Gold contradicted; semantic_match=null | Nessun confronto positivo col Gold; proposta discordante non promossa a label valida |
| Evidenze | 18 file del manifest originale verificati; raw, chunk, extraction e ledger coerenti; finalizzazione completa | Custodia della raccolta **VALIDATO** nel perimetro documentato |

`promotion_authorized=false`. La chiamata è **ESEGUITO**; il sistema non è
**INTEGRATO** o **CERTIFICATO**. Compatibilità completa del decoder, accuratezza
generativa delle contraddizioni, Gate, integrazione e certificazione restano
**BLOCCATO**. Nessuna seconda generazione.

## Attività → Script → Commit

Riconciliati TODO ed Experiment Register ufficiali a
`2b235a6db692bab0ed097482e9fac8cc04a0ca15` tramite raw GitHub e blob locali,
report decisionale `rag-v5-operational-unblocking-decision-01.md`, branch
`codex/tactical-state-contract-v1`, remote atteso e HEAD locale/remoto uguali.
Working tree iniziale pulito. Nessun tentativo precedente della nuova attività
nelle evidenze versionate o nella sua destinazione locale; il driver rifiuta
qualsiasi esistenza della directory di destinazione, anche esito ambiguo.

Differenza tecnica registrata prima dei controlli: nuovo schema/handoff
remediation A/R1 rispetto alla baseline 13814c2 del runtime-04. Non ripetute
suite 37/13/16/5, gate storici, ricognizione, ABI, H1-G2 o audit fonti.

Script locale: [`operations/official_api_single_case_01.py`](../operations/official_api_single_case_01.py).
Verifica statica:
[`operations/official_api_single_case_01.static-review.json`](../operations/official_api_single_case_01.static-review.json).
Commit tecnico congelato prima dell'esecuzione:
**`9fcc212fc92c77ef6601a5b61ca40b1831cab0d9`**.

Analisi AST locale/remota, unico call site POST fuori da cicli, nessun redirect
o retry, lock esistente O_RDONLY/O_NOFOLLOW e flock esclusivo non bloccante,
handshake con ledger fsync prima di GO, conservazione incrementale della risposta,
controllo parent/process group del supervisore. Nessun test applicativo o
invocazione del remoto prima del singolo avvio. Un'asserzione del raccoglitore
statico iniziale presumeva due soli literal bytes; corretta per includere il
separatore vuoto dei chunk, senza eseguire driver o POST in quella fase.
Identità di 237 file Python applicativi confrontate coi byte congelati a
`cec94e57ce11903460bc9314de2c699aa83b0193`; nessun file applicativo modificato.
Hash e blob esatti del driver e dei file sono in `identity.json` e nella
verifica statica, non dedotti dal solo nome di versione.

## Preflight immediato e singola invocazione

SSH tramite alias `football-vps`, BatchMode, StrictHostKeyChecking=yes,
UpdateHostKeys=no, host key ssh-ed25519 e KEX già autorizzato. Fingerprint
known_hosts confrontato con la precedente identità autorizzata:
`SHA256:4KTDWZD9P2eq8vug3ZSUErbRkQdwTUnnlcSP2AzYFks`.
Nessuna accettazione automatica di chiavi nuove o modificate.

Il solo processo remoto supervisionato ha letto GET `/api/version`, `/api/tags`
e `/api/ps`, più stato processi per concorrenza. Risultati conservati nell'evento
ready: Ollama 0.40.5; qwen3.5:9b con digest
`56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`;
models=[] e nessun runtime concorrente osservabile corrispondente ai criteri.
Il lock condiviso esistente è aperto read-only, acquisito senza attesa e tenuto
per tutta la richiesta. Nessuna creazione/chmod/scrittura del lock o directory
remota. Dev/inode/UID/mode/size/mtime del lock identici alla chiusura.

Supervisore remoto verificato con argv e process group:
`timeout --signal=TERM --kill-after=15s 450s`, PID/PGID 179384;
Python remoto PID 179385 nello stesso gruppo. Il limite agisce sul processo
remoto, non soltanto sul client SSH. Non è un meccanismo di arresto del servizio
Ollama: non si deduce cancellazione del suo lavoro in caso di disconnessione.
In questa esecuzione non si è verificato timeout o disconnessione.

Il caller `judge_pair(extraction_locator=True, q3_04_timeout_360=True,
max_tokens=2048)` locale invariato costruisce il payload e fa post-processing.
Trasporto remoto via stdin/argv, una sola POST loopback `/api/chat` usando
HTTPConnection, nessun redirect o ulteriore POST. Parametri immutati:
temperature=0, num_ctx=4096, num_predict=2048, think=false, stream=false,
HTTP timeout 360 s; supervisione 450 s e kill-after 15 s.
Claim/evidence originali del caso q3_04 riusati byte-per-byte dall'input
storico; il Gold non è nei messaggi inviati. Nessuna esecuzione del wrapper,
staging, compilazione C++, linking o loading di librerie da parte del client.

Eventi remoti: ready `16:13:45.182186Z`, post_started
`16:13:45.223797Z`, risposta `16:16:53.872837Z`, finished
`16:16:53.872922Z`. Ledger locale persistito prima dell'invio GO; i timestamp
dei due host non sono usati come prova di sincronizzazione degli orologi:
l'ordine è garantito dal protocollo fsync → GO → POST. Un solo avvio del driver.

## Evidenze generative e boundary

Il servizio riporta prompt_eval_count=1657, prompt_eval_cached_count=0,
eval_count=1001; quest'ultimo è un numero di token, non di generazioni.
load_duration circa 8,887 s; prompt_eval_duration circa 55,656 s;
eval_duration circa 124,058 s. I contatori sono osservazioni della richiesta
processata, non conteggio pre-troncamento, prova di conservazione integrale
del contesto o assenza di context shift. Nessuna conversione byte/token.

La risposta grezza propone label supported. Le due relation sono identiche
come oggetti JSON. Il locator registra 16 frammenti: tutti gli 8 del claim
localizzati; fra gli 8 assegnati a evidence, solo il referente è localizzato,
7 hanno occurrence_count=0 e result=missing. Esempi: `La difesa bassa`,
`lascia molto spazio`, `molto spazio` sono proposti sul lato evidence ma
non vi compaiono letteralmente. Il reason code aggregato
E_EXTRACTION_LOCALIZATION_NOT_UNIQUE include quindi il caso di zero occorrenze,
non soltanto duplicati. I record completi restano in `result.json`.

Questa osservazione è già nel raw, senza riscrittura nell'handoff o nel
post-processing. Non dimostra un meccanismo interno del modello. Il
precontrollo semantico è stato superato per questo output, ma il grounding
side-bound lo arresta prima di produrre witness o raggiungere il validatore
finale. Non si attribuisce un errore a quest'ultimo; il locator conserva
il comportamento fail-closed richiesto. Nessuna correzione di frammenti,
comparison, polarity o label per ottenere un esito favorevole.

Non è provata compatibilità universale delle keyword o assenza di vincoli
ignorati dal decoder. L'assenza del precedente boundary unknown/same in
questo singolo raw non dimostra che l'errore generativo sia risolto.

## Inventari e verifica di conservazione

Destinazione locale distinta:
[`evaluation/remediation_a_official_api_single_case_01/`](../evaluation/remediation_a_official_api_single_case_01/).

| Artefatto | Contenuto verificabile |
|---|---|
| identity.json, invocation.json, remote-program.txt | Commit/blob/hash e comando remoto congelati |
| input.json, request_payload.json, schema.json | Input storico, messaggi e schema effettivamente inviati |
| ledger-created.json, ledger-commit-to-send.json, ledger-post-started.json | Prenotazione persistente e unico invio autorizzato |
| ssh-stdout.jsonl, ssh-stderr.txt, remote-events.json, http-headers.json | Eventi, stderr vuoto, esito HTTP e preflight |
| response-body.bin, raw_response.json, extraction.json | Byte HTTP originali, copia esatta e JSON estratto senza repair |
| result.json, summary.json | Boundary, provenance, contatori e distinzione label proposta/osservata |
| manifest.json | Manifest originale della finalizzazione del driver: 18 file |
| collection-verification.json | Verifica offline di quei 18 hash/dimensioni, chunk/raw, schema/payload, estrazione e conteggi |
| publication-inventory.json | Inventario aggiuntivo con manifest originale, verifica e .gitattributes; esclude soltanto se stesso |

Payload: 24.574 byte, SHA-256
`0852b5ad08557195c76a784b632d5b30e44657802b40b712b4de507629d8d16d`.
Risposta HTTP: 3.957 byte, SHA-256
`dab16c58e6df124355630743b898926ce49d83e5336796ca3081f88155b24147`.
`schema.json` è una copia JSON con indentazione (41.356 byte), uguale come
oggetto al campo format: la dimensione diversa dalla serializzazione storica
non è un cambiamento del contratto. I byte effettivamente inviati sono nel
payload, non nella copia pretty-printed dello schema.

Verifiche di raccolta nuove, non replay del judge/materializer o suite storiche:
hash/dimensioni 18/18, eventi stdout uguali al JSON raccolto, un solo
post_started, chunk/body/raw identici, extraction uguale al content del raw,
schema uguale a format, Gold assente dai messaggi, esito remoto 0 e lock
metadata preservati. I file originali del driver non sono riscritti per
aggiungere la verifica: inventario di pubblicazione separato. Attributo -text
locale alla raccolta per conservare i byte anche nei blob Git.

## Report → Risultato → Decisione → Stato

Commit documentale finale: report, raccolta e inventari con TODO e Experiment
Register contestuali; identificabile tramite la storia di questo file dopo
pubblicazione. Il commit tecnico e quello documentale sono pubblicati nella
stessa sessione e confrontati con GitHub; working tree finale verificato.

**Decisione sul prossimo passo, senza eseguirlo:** una futura analisi offline
del nuovo raw e della sua assegnazione claim/evidence, concentrata sui sette
frammenti evidence assenti, prima di qualsiasi modifica o nuova generazione.
È un problema osservato sul nuovo output e distinto da unknown/same del
runtime-04; non riapre ABI/H1-G2 né richiede un altro esperimento sul modello.
Nessuna analisi causale estesa, patch o nuova inferenza avviata automaticamente.

Attività **ESEGUITO**; elaborazione API del singolo payload e integrità delle
evidenze **VALIDATO** nei limiti sopra esplicitati. Esito semantico
not_evaluable, label osservata nulla; accuratezza, ABI, compatibilità backend
completa, Gate, integrazione e certificazione **BLOCCATO**.
Nessun servizio/configurazione, checkout operativo, staging, Chroma, indice,
corpus o panel modificato. Caricamento Qwen autorizzato; nessun warm-up,
unload o cambiamento keep_alive aggiunto al payload. Nessuna ulteriore
connessione diagnostica, POST, runtime-05, wrapper, merge o deploy. STOP.
