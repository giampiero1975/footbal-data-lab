# RAG V5 Dual Blocker — singola esecuzione runtime-04

Attività: `RD-RAG-V5-DUAL-BLOCKER-RUNTIME04-EXECUTION-01`.
Data: 2026-11-10, Europe/Rome.

## Attività

Eseguita una sola invocazione autorizzata del launcher approvato sul caso
`q3_04`. Il risultato è **B: not_evaluable**, per incoerenza semantica
dell'extraction prima del locator. Il completamento generativo e il corretto
fail-closed non dimostrano accuratezza delle contraddizioni.

TODO ufficiale, Experiment Register, preparazione locale, staging,
trasferimento/preflight e runtime-03 riconciliati prima delle operazioni.
HEAD iniziale locale/GitHub
`c699639e78b992c09858963d4e76137d66be0b5e`, branch
`codex/tactical-state-contract-v1`, working tree locale pulito. Nessuna voce
runtime-04 già eseguita; directory artefatti assente prima dell'invocazione.

Differenza tecnica già documentata: handoff/schema extraction della patch
dual-blocker, precontrollo semantico e nuovo ramo diagnostico nel verificatore.
Nessuna campagna, suite precedente o prova forense è stata ripetuta.

## Script e identità

Wrapper remoto approvato:
`/home/football/.local/share/football-data-lab/runtime-wrappers/spatial-v2-extraction-locator-q3-04-runtime-04.sh`.
Dimensione 47.755 byte, SHA-256
`abf6db3060b68cbc1e5d9e1c28ea13e2cb3dbce09f2ae2b5c00f8ec1e7f55f17`.

Staging:
`/home/football/.local/share/football-data-lab/staging/spatial-v2-dual-blocker-13814c2`.
HEAD obbligatorio e osservato:
`13814c20d80bca4d9cb4cb08a288b6e7b31dac0d`.

Modello `qwen3.5:9b`, digest
`56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`.

## Preflight immediato

Snapshot alle `2026-11-10T13:44:51.528298+00:00`. Solo prerequisiti volatili:

- wrapper remoto regolare, proprietario corrente, modo `0600`, hash e
  dimensione conformi; byte riletti identici alla copia locale;
- staging detached alla baseline esatta e status vuoto, tracked e untracked;
- directory artefatti runtime-04 assente, nessun tentativo preesistente;
- nessun processo runtime pertinente osservato, zero cmdline non leggibili;
- sole GET tags/ps: digest modello esatto e nessun modello caricato;
- lock esistente regolare, inode verificato, sondato con flock esclusivo
  non bloccante e subito rilasciato, senza scrivere dati. Il wrapper ha poi
  effettuato la propria acquisizione prevista; nessun lock sostitutivo.

Nessuna correzione automatica, suite o nuova validazione storica dello staging.

## Unica invocazione

Il file completo contiene il launcher `ssh football-vps 'bash -s'` e il corpo
remoto delimitato. Dopo confronto integrale con il file remoto verificato,
è stata eseguita una sola volta la copia locale identica, con Git Bash:

```text
C:\Program Files\Git\bin\bash.exe projects/tactical-engine/operations/runtime-wrappers/spatial-v2-extraction-locator-q3-04-runtime-04.sh
```

Nessun byte del launcher/corpo è stato modificato, estratto per eseguire un
percorso alternativo o sostituito. Nessun timeout esterno aggiunto al processo.
La supervisione è quella già incorporata nel wrapper.

Parametri effettivi conservati negli artefatti: temperatura 0, contesto 4.096,
2.048 token massimi, think false, HTTP 360 s, supervisore 450 s, kill-after
15 s, extraction locator opt-in e `promotion_authorized=false`.

| Dimensione | Esito osservato |
|---|---|
| Invocazioni launcher | 1 |
| Chiamate di trasporto | 1 |
| Generazioni complete | 1 |
| Risposta | ricevuta, JSON valido, `done=true`, `done_reason=stop` |
| Token | prompt_eval_count 592, eval_count 846 |
| Durata monotona registrata | 132,5378359660972 s |
| Processo generativo supervisionato | exit 0 |
| Launcher/wrapper | exit 80 |
| Stato finale | `completed_fail_closed` |
| Retry, repair, fallback | 0 |

Le letture di avanzamento hanno monitorato lo stesso processo; non erano
invocazioni del wrapper né chiamate aggiuntive al modello. I timestamp locali
del launcher e remoti del generatore restano separati negli originali; per la
durata si usa il contatore monotono del generatore.

## Risultato e confronto con Gold

Boundary autorevole: `E_EXTRACTION_SEMANTIC_INCONSISTENT`.
Dettaglio runtime:

```json
{"code": "E_EXTRACTION_COMPARISON_INCONSISTENT", "path": "comparison"}
```

Classificazione del verificatore: `fail_closed_extraction_semantic`.
Il parsing/shape dell'extraction è superato; il precontrollo la respinge prima
del locator e prima della materializzazione/validazione del witness.

| Campo | Valore |
|---|---|
| `evaluation_status` | `not_evaluable` |
| Label proposta nel raw/extraction | `supported` |
| Label osservata autorevole | null |
| Gold | `contradicted` |
| Semantic match autorevole | null |
| Witness | assente, valore null e file non prodotto |
| Validation | assente, valore null e file non prodotto |
| Provenance | diagnostica, `not_evaluable`, `records=[]` |
| Promozione | `promotion_authorized=false` |

Non è il caso C (witness valido con label supported): non esiste un witness
validato. Non è il caso A e non dimostra la contraddizione richiesta dal Gold.
La label grezza è conservata senza correzioni e non viene promossa.

### Lettura diagnostica del nuovo output

L'extraction propone `comparison=same` in tutte le dimensioni, ma assegna
`status=unknown` agli slot di entrambe le relazioni e alle condizioni; gli
item delle condizioni sono ambiguous. Questa combinazione è incoerente con
le regole versionate: `_expected_comparison()` richiede unknown quando gli
slot sono unknown. Il reason code runtime è aggregato su `comparison` e non
elenca le singole dimensioni; questa spiegazione è una lettura statica del
raw e delle regole esistenti, non una nuova esecuzione del validatore.

Entrambi i valori spaziali proposti sono `abundant`, senza rappresentare
l'opposizione fra molto spazio nel claim e riduzione dello spazio nella fonte.
La presenza di frammenti nel JSON non prova localizzazione: il locator non è
stato raggiunto e nessun confronto con i 10/11 frammenti runtime-03 dimostra
un miglioramento. La causa cognitiva interna del modello non è determinabile.

## Commit → Report → Evidenze e finalizzazione

Il commit documentale di questa attività pubblica questo report, gli originali,
metadati, TODO e registro nella stessa sessione; è identificabile dalla storia
del report. Nessun commit applicativo prodotto.

Directory VPS originale:
`/home/football/.local/share/football-data-lab/runtime-artifacts/spatial-v2-extraction-locator-q3-04-runtime-04`.

Evidenze pubblicate in `evaluation/runtime04_execution_01/`:

- `artifacts/`: tutti i 27 file originali, inclusi prompt, payload/schema,
  raw response, extraction, result, provenance, decision, log e inventari;
- `metadata/`: preflight, singola invocazione locale e verifica di raccolta;
- `summary.json`: riepilogo derivato, distinto dagli originali;
- README con comandi di verifica hash senza eseguire il runtime.

Ogni file è stato riletto dalla VPS e confrontato con il suo hash; gli
attributi Git preservano esattamente i byte. Nessun artefatto originale è
stato corretto, normalizzato o riscritto per la pubblicazione.

| Inventario | Entry verificate | SHA-256 inventario |
|---|---:|---|
| `hashes.sha256` | 23 | `fa494a948b1da963bf3bc270b3806b1559948c0b3acc0d219c17daa9546083a7` |
| `attempt_state.sha256` | 1 | `49034faf3a70ea6972d19181404bb6f712bfe483d29243181e4b0dcd60167659` |
| `hashes.sha256.digest` | 1 | `12ee4055a2caad18608e98efa726eacea0b0be4ee77306fc7040e97105763484` |

Tutte le entry conformi, zero errori. `finalization_complete=true`, nessun
`finalization_errors.log`. Stato finale SHA-256
`79ec318be27abd5df685d2a294aac4325136c58191b3b6d7587ce4af1bdb78b8`.
Raw response SHA-256
`15aae8e9a6d71619f1a5d26e42e922c75adc5eb66a9027d6d3dd7fa5fa46a9eb`.

Staging dopo il tentativo ancora alla baseline esatta e pulito. Hash dei wrapper
runtime-04 e runtime-03 invariati. Nessuna operazione sul checkout operativo,
Chroma, corpus, indici, servizi o panel; nessun altro caso, merge o deploy.

## Decisione → Stato

Unico tentativo autorizzato **ESEGUITO**, autorizzazione consumata. Completamento
tecnico, finalizzazione e fail-closed semantico del singolo caso **VALIDATO**.
Localizzazione e witness non valutati; obiettivo generativo `contradicted`
non dimostrato. Accuratezza delle contraddizioni, ulteriore runtime, Gate,
integrazione e certificazione restano **BLOCCATO**.

Decisione motivata: non ripetere un runtime invariato. Prossimo passo proposto,
non eseguito: revisione offline mirata della nuova raw response e dell'handoff
di status/comparison, prima di decidere qualunque patch o nuovo test. La nuova
evidenza `unknown` con comparison `same` è distinta da quella runtime-03 e va
trattata senza riaprire le analisi già concluse. Nessuna revisione aggiuntiva,
modifica, inferenza o campagna è autorizzata implicitamente. STOP dopo
pubblicazione e verifica delle evidenze.
