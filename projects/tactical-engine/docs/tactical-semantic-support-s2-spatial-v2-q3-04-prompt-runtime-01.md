# RD-TSC-V2-D3-S2-SPATIAL-V2-Q3-04-PROMPT-RUNTIME-01

## Baseline, autorizzazione e ambiente

Singolo runtime differenziale autorizzato dopo la remediation del prompt
Spatial V2, confrontato con il precedente tentativo a 360 secondi.

- baseline e staging: `41d50fa042b88aaa357a19e2c2d5de52a4910728`;
- baseline di confronto: `69ec127cddbba114d8c37f3eefde5dba9200520c`;
- staging indipendente:
  `/home/football/.local/share/football-data-lab/staging/spatial-v2-q3-04-prompt-runtime-41d50fa`;
- artefatti:
  `/home/football/.local/share/football-data-lab/evaluation/spatial-v2-q3-04-prompt-runtime-01`;
- checkout operativo preservato a
  `1a80fe0c6261b10f748a36c2b4fd96e8e2253971`;
- modello `qwen3.5:9b`, digest
  `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`;
- Python 3.12.3;
- dataset SHA-256 Linux
  `8e3933f5539a6c1d77dae84b7dbdb445c7193992ebd0be44e8c818abbdfecf4c`.

Il preflight immediato ha verificato staging detached e pulito, caso e dataset
identici al confronto, validatore identico, nuova istruzione presente, modello
e digest conformi, artefatti assenti, nessun modello caricato e nessun processo
diagnostico concorrente osservato. Lo snapshot non garantisce esclusività
futura. Il bundle usato per lo staging era 2.375.721 byte, SHA-256
`62da58ddd7ec3ce3ac3ca8df139693103877feeb34f69e7a2db7b609c4bbd2a9`,
verificato e rimosso dopo il checkout conforme.

## Configurazione ed esecuzione

Il wrapper esterno al repository ha invocato una sola volta:

```python
judge_pair(
    claim, evidence, model="qwen3.5:9b", timeout=180,
    max_tokens=2048, transport=transport,
    q3_04_timeout_360=True,
)
```

Il trasporto iniettato ha contato la chiamata, conservato il payload e delegato
direttamente a `_default_transport()`. Timeout HTTP effettivo 360 s;
supervisione esterna:

```text
/usr/bin/time -v timeout --signal=TERM --kill-after=15s 450s /usr/bin/python3 wrapper.py
```

Modello, schema, temperatura 0, contesto 4096, `num_predict=2048`,
`stream=false`, `think=false`, dataset e validatore sono invariati. L'unico
delta funzionale è l'istruzione normativa del prompt. Una richiesta effettiva,
zero retry, repair e fallback.

## Risultato tecnico

- exit code wrapper/supervisore: `0`;
- durata wrapper: `247,240718` s; wall clock `/usr/bin/time`: `4:07,30`;
- risposta completa: `done_reason=stop`;
- durata Ollama: `247,211554` s;
- caricamento: `9,130861` s;
- prompt: 462 token in `15,636750` s;
- generazione: 1.803 token in `222,432006` s, circa `8,11 token/s`;
- timeout esterno non intervenuto;
- payload, prompt, risposta grezza e configurazione preservati.

Il tentativo precedente aveva durata wrapper `236,003188` s, 188 token prompt,
1.771 token generati e circa 8,04 token/s. La nuova istruzione ha aumentato il
prompt di 274 token; la durata complessiva è aumentata di circa 11,24 s, senza
evidenza di regressione o miglioramento prestazionale generalizzabile.

## Confronto strutturale del witness

Il modello ha nuovamente proposto `supported`, ma il validatore ha restituito:

- `evaluation_status=not_evaluable`;
- `technical_status=not_evaluable`;
- `E_ANCHOR_INVALID`;
- `E_STATUS_VALUE_INCONSISTENT`;
- `derived_label=null`;
- `comparison_verified=false`;
- `semantic_compatibility_verified=false`;
- `promotion_authorized=false`.

Il delta strutturale è circoscritto:

| Controllo | Prima | Dopo | Esito |
|---|---:|---:|---|
| quantificatori conformi | 0/2 | 2/2 | miglioramento dimostrato |
| anchor validi | 0/16 | 0/14 | nessun miglioramento |
| anchor invalidi | 16/16 | 14/14 | invalidità ancora 100% |
| codici errore | 2 | 2 | invariati |

Entrambi i quantificatori sono ora correttamente
`implicit/none/null/[]`; il divieto `explicit/absent/[]` è quindi rispettato.
Tutti i 14 anchor rimasti sono però invalidi. Gli intervalli dichiarati non
selezionano gli `exact_span`; inoltre l'anchor del soggetto del claim dichiara
`source=evidence`, incompatibile con il lato del campo. Esempi: claim
`[24,30)` restituisce `"olto s"`, non `"molto"`; evidence `[165,171)`
restituisce `"o avan"`, non `"spazio"`.

Resta anche una seconda incoerenza normativa, già presente nel witness
precedente ma non isolata come causa concorrente nel closeout storico: entrambe
le polarità sono `status=explicit`, `value=affirmed`, con anchor. Il contratto
ammette `affirmed` come implicito senza anchor e riserva `explicit` al valore
`negated`; pertanto `E_STATUS_VALUE_INCONSISTENT` permane anche dopo la
correzione dei quantificatori. Questa precisazione non altera il risultato
storico, ma impedisce di attribuire quel codice esclusivamente ai
quantificatori.

La correzione del prompt ha dunque prodotto un miglioramento strutturale
parziale e verificabile, ma non un witness strutturalmente valido. La semantica
proposta non è valutabile e non può essere promossa.

## Artefatti e integrità

Sono conservati caso, configurazione, prompt, payload, risposta grezza,
risultato, manifest, stdout, stderr/time, exit code, snapshot modello,
preflight, digest di dataset/validatore e stati Git prima/dopo. L'inventario
contiene 24 file verificati senza discrepanze. SHA-256 di `hashes.sha256`:
`078418c795e67018933fc658b99ec87117a566b1aea9d0ea2d0bc971e7ae2143`.

HEAD e working tree del checkout operativo e dello staging sono invariati
prima/dopo. Nessuna modifica volontaria a collection, servizi, pipeline o
staging precedente.

## Decisione e stati

Flusso: Attività = runtime differenziale post-remediation; Script = wrapper
esterno e judge Spatial V2; Commit = commit documentale; Report = questo
documento; Risultato = completamento tecnico con correzione dei quantificatori
ma witness ancora non valutabile; Decisione = nessun rilancio e nessuna
promozione.

| Componente | Stato |
|---|---|
| Singolo tentativo runtime autorizzato | **ESEGUITO** |
| Completamento tecnico e singola chiamata | **VALIDATO** nel singolo caso |
| Fail-closed e non-promozione | **VALIDATO** nel singolo caso |
| Correzione runtime dei quantificatori | **VALIDATO** nel singolo caso |
| Validità complessiva del witness e semantica `q3_04` | **BLOCCATO** |
| Promozione, Gate, integrazione e certificazione | **BLOCCATO** |

L'autorizzazione runtime è consumata. Non sono autorizzati ulteriori tentativi.
