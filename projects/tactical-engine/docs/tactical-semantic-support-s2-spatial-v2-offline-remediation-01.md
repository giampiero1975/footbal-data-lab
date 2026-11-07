# RD-TSC-V2-D3-S2-SPATIAL-V2-OFFLINE-REMEDIATION-01

## Baseline e riconciliazione

Remediation offline mirata sulla baseline GitHub
`128f01404d59030a2567b5aab519688ec55e2d5a`, branch
`codex/tactical-state-contract-v1`. HEAD locale/remoto conformi e working tree
pulito prima delle modifiche. Sono stati riconciliati TODO, registro, specifica
2.0.0, remediation documentale e report della prima implementazione. I due
difetti non risultavano corretti da commit successivi.

Nessuna inferenza, rete reale, Gate, benchmark o suite storica è stata eseguita.

## R1 — incompatibilità dei valori

### Difetto e causa

Sulla baseline, `_expected_comparison()` restituiva
`{"different", "incompatible"}` per valori diversi. `_comparison_errors()`
restringeva correttamente alle coppie presenti in `INCOMPATIBLE_VALUES`, ma per
le altre coppie lasciava intatto l'insieme permissivo. Un witness sintetico
`abundant/neutral` o `scarce/neutral` con comparison `incompatible` poteva quindi
essere accettato e derivare erroneamente `contradicted`.

### Correzione

Per due valori espliciti:

1. assi diversi consentono soltanto `different`;
2. assi uguali e valori uguali consentono soltanto `same`;
3. assi uguali e coppia nella matrice consentono soltanto `incompatible`;
4. ogni altra coppia diversa consente soltanto `different`;
5. `unknown`/`ambiguous` conservano la precedenza delle sentinelle.

Un comparison contrario produce `E_COMPARISON_INCONSISTENT` e
`not_evaluable`. Il vocabolario non è stato ampliato.

## R2 — errori operativi del judge

### Difetto e causa

Sulla baseline, timeout/eccezioni di trasporto uscivano da `judge_pair()`;
risposta incompleta, contenuto mancante e JSON malformato sollevavano
`RuntimeError`. Non esisteva un envelope strutturato standalone per questi
fallimenti.

### Correzione

Il boundary del judge restituisce ora sempre, per gli errori operativi previsti:

```json
{
  "evaluation_status": "not_evaluable",
  "label": null,
  "witness": null,
  "validation": {
    "technical_status": "not_evaluable",
    "error_codes": ["E_JUDGE_TIMEOUT"]
  },
  "promotion_authorized": false
}
```

Codici minimi:

| Condizione | Codice |
|---|---|
| `TimeoutError` | `E_JUDGE_TIMEOUT` |
| `ConnectionError`, `URLError`, `OSError` | `E_JUDGE_TRANSPORT` |
| envelope non dict o `done_reason != stop` | `E_JUDGE_RESPONSE_INCOMPLETE` |
| message/content assente | `E_JUDGE_RESPONSE_MISSING` |
| JSON malformato | `E_JUDGE_JSON_INVALID` |
| witness parseabile ma invalido | codici del validatore esistente |

Il trasporto viene chiamato una sola volta. Non esistono retry, repair, fallback
o correzione del JSON. Errori di programmazione non classificati, verificati con
`TypeError` del trasporto iniettato, rimangono eccezioni e non vengono mascherati.

## Differenze tecniche dei test

I test precedenti verificavano una coppia normativa e gli assi diversi, ma non
le coppie diverse non incompatibili. Inoltre richiedevano esplicitamente che
timeout e JSON malformato sollevassero eccezioni.

Nuove verifiche:

- `abundant/scarce` accetta `incompatible`;
- `abundant/neutral` e `scarce/neutral` rifiutano `incompatible`;
- valori uguali richiedono `same`;
- assi differenti rifiutano `incompatible`;
- timeout, trasporto, incomplete, missing content e JSON invalido restituiscono
  codici distinti;
- ogni errore operativo mantiene esattamente una chiamata;
- witness invalido resta non promotabile;
- `TypeError` di programmazione resta eccezione.

## Matrice test prima/dopo

| Esecuzione | Esito | Nota |
|---|---:|---|
| Baseline pubblicata | 16/16 PASS | non copriva R1; R2 attendeva eccezioni |
| Primo run remediation | 16/18 PASS, 2 FAIL | R1 sovrascriveva sentinelle evidence con `different` |
| Run finale | **18/18 PASS** | sentinelle valutate prima della matrice esplicita |

Il primo run della remediation ha quindi rilevato una regressione locale
introdotta dalla correzione; è stata risolta senza ampliare il perimetro.

## Comando ed exit code

```text
python -m unittest tests.test_v5_tactical_semantic_support_s2_spatial_v2 -v
```

Run finale: exit code `0`, 18 PASS, 0 FAIL, 0 errori.

## Isolamento

- solo moduli Spatial V2 e relativa suite modificati;
- judge ancora inerte all'importazione e opt-in;
- trasporti esclusivamente mock;
- nessuna chiamata Ollama/Qwen o rete;
- contratto `2.0.0`, `compatible` shadow e non-promozione invariati;
- NLI V2, Spatial V1, bridge, S1/S2, retrieval, Gold, fixture, pipeline, API,
  RAG, Chroma e panel invariati.

## Limiti residui

- la matrice prova coerenza del witness, non correttezza semantica;
- coreferenza `compatible` non verificata;
- `q3_04` non è stato inferito né risolto;
- judge non integrato nel boundary S2;
- validazione indipendente della remediation ancora **DA FARE**.

## Matrice probatoria A/B/C

| Conclusione | Livello |
|---|---|
| R1 riproducibile sulla logica baseline | A — codice/test sintetico |
| R1 rifiutato dopo correzione | A — test |
| R2 propagava eccezioni operative | A — codice/test storico |
| R2 produce envelope e una chiamata | A — test mock |
| Nessuna inferenza reale | A — perimetro comandi/mock |
| Accuratezza semantica migliorata | non dimostrato |
| `q3_04` corretto | non dimostrato |

## Decisione finale

R1 e R2 sono **IMPLEMENTATO** e i nuovi test differenziali sono **ESEGUITO**.
Il run finale dimostra le proprietà offline coperte, ma la remediation non viene
promossa a **VALIDATO** prima della revisione indipendente richiesta.

## Stati ufficiali

| Componente | Stato |
|---|---|
| Specifica/remediation documentale Spatial V2 | **ESEGUITO** |
| Revisione documentale R1–R5 | **VALIDATO** |
| Prima implementazione offline | **IMPLEMENTATO** |
| Test precedenti | **ESEGUITO** |
| Remediation R1/R2 | **IMPLEMENTATO** |
| Nuovi test differenziali | **ESEGUITO** |
| Validazione indipendente remediation | **DA FARE** |
| Validazione complessiva validatore | **BLOCCATO** |
| Efficacia semantica | **BLOCCATO** |
| Gate runtime, integrazione, certificazione | **BLOCCATO** |
| Provenance Spatial V1 | **VALIDATO** |

Unico prossimo passo: revisione indipendente della remediation, dei 18 test e
del presente report. Nessuna inferenza o integrazione.
