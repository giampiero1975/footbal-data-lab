# RD-TSC-V2-D3-S2-SPATIAL-V2-Q3-04-TIMEOUT-OPTIN-360-01

## Baseline e scopo

Implementazione offline della variante diagnostica Spatial V2 `q3_04` con
timeout client opt-in di 360 secondi.

- baseline GitHub iniziale:
  `a8edbb691d23fb634aee4d7daade936f5da51391`;
- branch: `codex/tactical-state-contract-v1`;
- causa storica già validata: generazione CPU a circa 8,13 token/s oltre il
  timeout client di 180 s;
- nessuna riapertura della diagnosi, esportazione log o esecuzione runtime.

## Differenza tecnica

`scripts/shadow_nli_spatial_relations_v2_inference.py` conserva
`DEFAULT_TIMEOUT_SECONDS=180` e aggiunge
`Q3_04_DIAGNOSTIC_TIMEOUT_SECONDS=360`. `judge_pair()` espone il solo keyword
opt-in `q3_04_timeout_360=False`. Quando è `True`, `effective_timeout` vale 360
ed è passato direttamente all'unica invocazione del trasporto; in assenza
dell'opt-in continua a essere usato il parametro `timeout`, il cui default è
180.

Non sono stati modificati modello, endpoint, prompt, schema, temperatura,
contesto, `num_predict=2048`, gestione della risposta o validazione. Il payload
Ollama è identico tra default e opt-in; cambia esclusivamente il timeout del
client HTTP.

## Test offline mirati

Eseguiti con Python 3.13 e trasporto mock, senza rete:

1. `test_18_q3_04_timeout_optin_propagates_360_without_payload_changes`;
2. `test_19_q3_04_timeout_optin_remains_fail_closed_without_retry`.

Risultato: **2/2 PASS**. Il primo prova la sequenza 180/360, payload identico,
modello `qwen3.5:9b` e 2.048 token. Il secondo prova una sola chiamata, timeout
360 e risultato `not_evaluable` con `E_JUDGE_TIMEOUT` e
`promotion_authorized=false`.

I test storici su errore di trasporto, risposta incompleta/mancante, JSON
invalido e assenza di retry non sono stati ripetuti: i relativi rami non sono
stati modificati. La nuova prova timeout attraversa comunque lo stesso envelope
fail-closed con l'opt-in attivo.

## Invarianti e limiti

- default 180 s invariato;
- opt-in esplicito e disattivato per default;
- 360 s propagati al trasporto HTTP senza override successivi;
- una sola chiamata, zero retry, repair e fallback;
- nessuna risposta parziale promossa;
- comportamento legacy e altre modalità invariati;
- nessuna inferenza Qwen/Ollama, VPS, SSH, sudo, Gate o benchmark.

Il timeout 360 è un budget sperimentale: la validazione offline non dimostra che
il modello completerà il witness, né la sua correttezza semantica o le
prestazioni runtime.

## Decisione e stato

Flusso: Attività = opt-in timeout 360; Script = judge Spatial V2 e test mock;
Commit = commit della presente attività; Report = questo documento; Risultato =
2/2 PASS; Decisione = variante pronta per revisione, nessun runtime autorizzato.

| Componente | Stato |
|---|---|
| Variante timeout 360 | **IMPLEMENTATO** |
| Test differenziali offline | **ESEGUITO** |
| Propagazione e invarianti interessati | **VALIDATO** offline |
| Prima esecuzione con 360 s | **DA FARE** con autorizzazione distinta |
| Semantica `q3_04`, Gate, integrazione e certificazione | **BLOCCATO** |
