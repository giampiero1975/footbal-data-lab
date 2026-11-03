# TSC V2 dual-output D3 — implementazione offline

## Identità

- Attività: `RD-TSC-V2-DUAL-OUTPUT-IMPLEMENTATION-01`
- Baseline documentale iniziale: `5b3836a803fcfe85572f86ac5de7aace0b5f8221`
- Baseline tecnica storica di confronto: `965d6b60b84d56c86fdc64c9c82583bfd2b1da2f`
- Commit tecnico: `f544589`
- Specifica: `docs/tactical-state-contract-v2-dual-output-design-01.md`
- Perimetro: implementazione e test offline; nessuna inferenza, retrieval, Chroma,
  API, pannello, deploy o Gate runtime.

## Delta tecnico

| File | Delta |
|---|---|
| `scripts/v5_tactical_state_dual_output_v1.py` | Nuovo modulo D3 isolato: preflight, fingerprint, renderer, schema documentale, parser, controlli e diagnostica fail-closed |
| `scripts/smoke_test_rag_v5_e2e.py` | Nuova funzione one-call e flag opt-in; report diagnostico separato |
| `scripts/run_rag_v5_query.py` | Propagazione e validazione del nuovo flag, senza cambiare default |
| `tests/test_v5_tactical_state_dual_output_v1.py` | 17 verifiche differenziali con fixture e trasporto mock |

TSC V1, modulo del dominio V2, generazione V2 precedente, planner, audit V1,
retrieval, collection, API e pannello non sono stati modificati.

## Schema e autorità

Il flag nuovo è:

`--tactical-state-contract-v2-dual-output`

È mutuamente esclusivo con `--tactical-plan`, `--tactical-state-contract` e
`--tactical-state-contract-v2`; non appartiene a `DEFAULT_PROFILE_FLAGS`.

Il transport model-authored è `tactical_state_documentary_explanation_v1` e contiene
soltanto fingerprint e `documentary_explanation`. Non ammette `applied_plan` o
`canonical_relations`. Il risultato sistemico è
`tactical_state_dual_output_diagnostic_v1`.

`prepare_dual_output_request()` riusa il preflight V2, conserva il piano autorevole,
calcola SHA-256 sul canonical JSON e rende deterministicamente le relazioni.
`chat_tactical_state_v2_dual_output_once()` effettua al massimo una chiamata, senza
retry o repair. Raw, piano, rendering, explanation e controlli rimangono separati.

## Controlli implementati

- schema e proprietà esatte;
- fingerprint del piano;
- cardinalità e dimensioni approvate;
- ID unici di sezioni e claim;
- relation, requirement ed evidence ref risolvibili;
- copertura di relazioni e requisiti;
- bindings esatti per attore, compito, spazio, trigger, finalità e fase;
- polarità negata bloccante e polarità incerta non valutabile;
- evidence anchor esatto con sola normalizzazione NFC/newline;
- distinzione tra anchor presente e supporto semantico;
- audit V1 applicato alla sola prosa documentale;
- nessuna promozione parziale;
- troncamento e transport error non valutabili;
- precedenza delle violazioni dimostrate su scope non valutabili.

Una relazione citata ma non conclusivamente coperta è distinta da una relazione
omessa. Questa distinzione è locale alla copertura documentale D3 e non modifica la
remediation separata `explicit_operational_requirement_omitted` nel dominio V2.

## Supporto documentale e limite intenzionale

La presenza di un citation ID e di un anchor esatto non viene promossa a supporto
semantico. `documentary_diagnostic()` accetta un assessment sistemico separato:

- `supported`: consente al controllo direct di proseguire;
- `unsupported`: produce `blocked`;
- assente: produce `not_evaluable`.

`bounded_inference` e `uncertainty` non sono automaticamente promuovibili. Il wrapper
runtime non fornisce assessment: pertanto, nella prima implementazione, una risposta
con claim documentali non può ottenere un PASS completo solo grazie ad anchor o
keyword. Questo è un limite fail-closed deliberato, non un test mancante.

Il test positivo offline usa un assessment sintetico esplicito per verificare la
macchina degli stati; non rappresenta un revisore semantico implementato.

## Verifiche eseguite

Motivazione: i 17 casi sono nuovi e coprono il nuovo schema D3. La regressione V2 è
limitata alla suite che importa i due wrapper modificati; nessun'altra campagna
storica è stata ripetuta.

| Comando | Risultato |
|---|---|
| `python -m unittest projects/tactical-engine/tests/test_v5_tactical_state_dual_output_v1.py -v` | 17/17 PASS |
| `python -m unittest projects/tactical-engine/tests/test_v5_tactical_state_generation_v2.py -v` | 16/16 PASS |
| `git diff --check` | PASS |

Copertura nuova: fingerprint/rendering, assenza del piano dal transport, direct con
assessment, anchor senza promozione, bounded inference, fingerprint errato, JSON
malformato/troncato, cardinalità, refs, ID duplicati, sei mismatch dimensionali,
polarità, citazioni/anchor, omissione, audit negativo, one-call/no-repair e isolamento
del flag/report.

Il primo ciclo differenziale ha scoperto una conflazione tra relazione incerta e
omessa. È stata corretta distinguendo `not_conclusively_covered` da `omitted`. Un
secondo rilievo riguardava la fixture, che citava una relazione invece di ometterla;
la fixture è stata corretta. Il ciclo finale è interamente positivo.

## Compatibilità

- percorso V1: invariato;
- percorso V2 precedente: invariato e regressione 16/16 PASS;
- profilo legacy/default: il nuovo flag non è attivo;
- planner e audit V1: importati e riusati senza modifica;
- API/pannello: nessun collegamento;
- runtime reale: non eseguito;
- promozione automatica con supporto incerto: impossibile.

## Decisione e stati

- modulo e percorso D3 opt-in: **IMPLEMENTATO**;
- verifiche differenziali: **ESEGUITO**;
- proprietà deterministiche e fail-closed coperte: **VALIDATO** offline;
- supporto semantico automatico end-to-end: **BLOCCATO** / non implementato;
- Gate runtime D3: **BLOCCATO**;
- integrazione runtime: **BLOCCATO**;
- certificazione: **BLOCCATO**.

La validazione offline riguarda struttura, isolamento e comportamento fail-closed.
Non certifica qualità generativa, supporto semantico reale o integrazione runtime.
