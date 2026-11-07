# RD-TSC-V2-D3-S2-SPATIAL-V2-Q3-04-RUNTIME-360-01

## Baseline, autorizzazione e ambiente

Singolo tentativo runtime diagnostico Spatial V2 `q3_04` con timeout opt-in di
360 secondi.

- HEAD GitHub e staging: `69ec127cddbba114d8c37f3eefde5dba9200520c`;
- staging indipendente:
  `/home/football/.local/share/football-data-lab/staging/spatial-v2-q3-04-360-69ec127`;
- checkout operativo preservato a
  `1a80fe0c6261b10f748a36c2b4fd96e8e2253971`;
- modello `qwen3.5:9b`, digest
  `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`;
- Python 3.12.3;
- dataset SHA-256 Linux
  `8e3933f5539a6c1d77dae84b7dbdb445c7193992ebd0be44e8c818abbdfecf4c`.

Il preflight ha verificato staging pulito, caso canonico, modulo opt-in,
costanti 180/360, descrittore single-generation, modello/digest, nessun modello
caricato e nessun processo diagnostico concorrente osservato. Lo snapshot non
costituisce garanzia di esclusività futura.

## Configurazione e comando

Il wrapper esterno al repository ha invocato una sola volta:

```python
judge_pair(
    claim, evidence, model="qwen3.5:9b", timeout=180,
    max_tokens=2048, transport=transport,
    q3_04_timeout_360=True,
)
```

Il trasporto iniettato ha conservato il payload e delegato direttamente a
`_default_transport()`. Timeout HTTP effettivo 360 s. Supervisione esterna:

```text
/usr/bin/time -v timeout --signal=TERM --kill-after=15s 450s /usr/bin/python3 wrapper.py
```

Modello, prompt, schema, temperatura 0, contesto 4096, `num_predict=2048`,
`stream=false` e `think=false` sono rimasti invariati. Una chiamata effettiva,
zero retry, repair e fallback.

## Risultato tecnico e metriche

- exit code wrapper/supervisore: `0`;
- durata wrapper: `236,003188` s; wall clock `/usr/bin/time`: `3:56,06`;
- risposta HTTP completa: `done_reason=stop`;
- durata Ollama: `235,975903` s;
- caricamento: `9,140688` s;
- prompt: 188 token in `6,465667` s;
- generazione: 1.771 token in `220,358612` s, circa `8,04 token/s`;
- timeout esterno non intervenuto;
- risposta grezza, payload, prompt e configurazione preservati.

Il timeout 360 ha quindi consentito il completamento tecnico di questo singolo
tentativo. Non dimostra prestazioni generali né correttezza semantica.

## Validazione strutturale e semantica

Il modello ha proposto la label `supported`, ma il witness non ha superato il
validatore deterministico:

- `technical_status=not_evaluable`;
- `E_ANCHOR_INVALID`;
- `E_STATUS_VALUE_INCONSISTENT`;
- `derived_label=null`;
- `comparison_verified=false`;
- `semantic_compatibility_verified=false`;
- `promotion_authorized=false`.

Tutti gli anchor testuali dichiarati nel witness hanno intervalli che non
corrispondono agli `exact_span`. Esempi: nel claim `[0,12]` produce
`"La difesa ba"`, non `"La difesa bassa"`; gli offset evidence 208–319
eccedono o puntano a porzioni diverse del testo disponibile. Inoltre il
quantificatore è dichiarato `status=explicit`, `value=absent`, con anchor vuoti,
combinazione vietata dal contratto.

La proposta semantica del modello non viene quindi valutata o promossa. Il
valore `abundant` è associato dal witness a `"togliendo però spazio"`, ma il
fallimento strutturale impedisce di trattare questa osservazione come verdetto
semantico contrattuale.

## Artefatti e integrità

Directory VPS:
`/home/football/.local/share/football-data-lab/evaluation/spatial-v2-q3-04-runtime-360-01`.

Sono conservati caso, configurazione, prompt, payload, risposta grezza,
risultato, manifest, stdout, stderr/time, exit code, snapshot modello,
preflight e stati Git prima/dopo. L'inventario contiene 22 file verificati senza
discrepanze. SHA-256 di `hashes.sha256`:
`4c98996be698a45c400360643fc575b5e970d04822ec74a24f029a313570bace`.

HEAD e working tree del checkout operativo sono identici prima/dopo; lo staging
resta pulito. Nessuna modifica volontaria a collection, servizi o pipeline.

## Decisione e stati

Flusso: Attività = runtime 360 `q3_04`; Script = wrapper esterno e judge Spatial
V2; Commit = commit documentale; Report = questo documento; Risultato =
completamento tecnico con witness non valutabile; Decisione = nessun rilancio,
presentare alla revisione indipendente.

| Componente | Stato |
|---|---|
| Singolo tentativo runtime 360 | **ESEGUITO** |
| Completamento tecnico nel singolo caso | **VALIDATO** |
| Fail-closed e non-promozione | **VALIDATO** |
| Validità strutturale e semantica `q3_04` | **BLOCCATO** |
| Promozione, Gate, integrazione e certificazione | **BLOCCATO** |

L'autorizzazione runtime è consumata. Non sono autorizzati ulteriori tentativi.
