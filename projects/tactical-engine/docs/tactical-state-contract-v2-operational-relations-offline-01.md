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
