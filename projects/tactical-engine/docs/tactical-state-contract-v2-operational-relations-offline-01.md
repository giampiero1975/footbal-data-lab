# Tactical State Contract V2 — operational relations offline 01

Data: 2026-11-03
Attivita: `RD-TSC-OPERATIONAL-RELATIONS-CONTRACT-V2-01`
Baseline: `db174b5651cec4b3439b650442900473f3b1773e`
Commit tecnico: `4cf91d6ae0c189d75d52ed52c7dda17e74d18274`

## Attivita e perimetro

Implementazione esclusivamente offline dell'estensione versionata
`tactical_state_contract_v2`. TSC V1 non e stato modificato. Il nuovo modulo
aggiunge soltanto proiezione deterministica dei requisiti relazionali,
fingerprint content-addressed, struttura `operational_relations` e controllo
domanda-piano. Runner, generazione, retrieval, API e pannello restano invariati.

File tecnici:

- `scripts/v5_tactical_state_contract_v2.py`;
- `tests/test_v5_tactical_state_contract_v2.py`.

## Decisioni tecniche congelate

- normalizzazione termini: Unicode NFC, apostrofi ASCII, whitespace compresso,
  trim e `casefold()`;
- `term_id`: SHA-256 UTF-8 del termine normalizzato;
- `requirement_fingerprint`: SHA-256 della serializzazione JSON UTF-8 con chiavi
  ordinate, separatori compatti e insieme chiuso di campi della proiezione;
- rule ID ammessi: `relation_requirement_projection:v1`, `phase_term_map:v1`,
  `position_term_exact_match:v1`;
- fase: tabella chiusa verso gli enum V1;
- `position_ref`: richiesto dal confronto soltanto quando la proiezione lo
  risolve in modo univoco per uguaglianza esatta con label o ID di uno slot.

Solo `explicit_representable` diventa obbligo. Requisiti `underspecified`,
`inferred`, `ambiguous`, non rappresentabili o non valutabili restano fuori
dalla promozione positiva e sono esposti in `unassessed_scope`. Il solo ID del
requisito non basta: fingerprint, attore, componenti obbligatori, fase e
riferimenti devono coincidere.

## Risultati

- test differenziali V2: 13/13 PASS;
- regressioni mirate V1, generazione e planner/audit: 125/125 PASS;
- compilazione in memoria: 2/2 PASS;
- `git diff --check`: PASS.

I casi nuovi coprono fingerprint stabile e sensibile al contenuto, relazione
esplicita valida, omissione, task/fingerprint/trigger divergenti, requisito
open, ambiguo e inferito, attore/fase errati, copertura duplicata e riferimento
a requisito inesistente.

Il tentativo iniziale di `py_compile` su disco non ha potuto creare il file
temporaneo nella directory `__pycache__` per permessi locali; non ha modificato
file tracciati. La compilazione equivalente in memoria ha superato entrambi i
file.

## Limiti

- il modulo non e collegato al prompt o al runner;
- non esiste ancora un flag generativo V2;
- nessuna inferenza dimostra la capacita di Qwen di produrre le relazioni;
- nessun Gold indipendente dimostra la generalita dell'estrazione;
- il controllo strutturale non certifica correttezza tattica o supporto
  documentale;
- API e pannello non consumano TSC V2.

## Tracciamento

**Attivita**: dominio operativo TSC V2 offline.
**Script**: nuovo modulo V2 isolato; V1 invariato.
**Commit**: `4cf91d6ae0c189d75d52ed52c7dda17e74d18274`.
**Report**: questo documento.
**Risultato**: contratto e controlli deterministici coperti offline.
**Decisione**: mantenere separato il futuro handoff generativo, subordinato a
revisione indipendente e autorizzazione distinta.
**Stato**: codice **IMPLEMENTATO**; test **ESEGUITO**; controlli differenziali
**VALIDATO offline**. Handoff generativo V2, runtime, API e pannello **DA FARE**;
integrazione e certificazione runtime **BLOCCATO**.

Nessun test runtime, inferenza, retry, repair, accesso Ollama/Chroma/API,
modifica al retrieval, deploy o merge e stato eseguito.

## Remediation fail-closed conclusiva

Commit tecnico: `fa56b8b`.

La revisione indipendente del primo consolidamento ha rilevato che lo schema
di `operational_relations` era esposto ma non applicato integralmente dal
validatore. La remediation applica una validazione strutturale deterministica
senza dipendenze aggiuntive e senza duplicare i controlli tattici o
documentali. Sono ora bloccanti campi mancanti o inattesi, tipi e riferimenti
non validi, cardinalita, provenienza/rule ID incoerenti, ID requisito mancanti
o duplicati e fingerprint non corrispondenti.

I riferimenti ad attore, fase e posizione sono risolti per ogni relazione,
anche quando il requisito non e promuovibile. Una proiezione assente o
incompleta resta `not_assessable`; un input malformato o una violazione
dimostrata e `failed`; soltanto una lista esplicitamente vuota costituisce
evidenza verificata dell'assenza di requisiti espliciti. La risoluzione della
fase rifiuta combinazioni di termini noti e sconosciuti. La provenienza di
estrazione e inclusa nel fingerprint perche concorre all'identita e alla
classificazione dell'obbligo.

Test eseguiti esclusivamente sul delta: otto casi differenziali nuovi e una
regressione positiva direttamente interessata, 9/9 PASS in 0,019 s. Non sono
state ripetute automaticamente le campagne 13/13 o 125/125 gia concluse.
`git diff --check` PASS. TSC V1, planner V1, retrieval, runner, prompt, API e
pannello sono invariati.

Risultato: remediation **IMPLEMENTATO**; test mirati **ESEGUITO**; proprieta
fail-closed corrette **VALIDATO offline** nel solo perimetro differenziale.
Handoff generativo, runtime, API e pannello restano **DA FARE**; integrazione e
certificazione runtime restano **BLOCCATO**.
