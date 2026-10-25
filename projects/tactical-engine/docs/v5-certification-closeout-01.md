# V5-CERTIFICATION-CLOSEOUT-01

Data: 2026-10-24. Stato: CERTIFICATO.

> Nota di lettura successiva al closeout: questo documento certifica soltanto
> manifest locked, runtime congelato e wrapper CLI descritti sotto. Gli sviluppi
> applicativi e di corpus successivi hanno evidenze e stati separati nella
> sintesi `docs/current-status-summary-01.md`; non ampliano retroattivamente
> questa certificazione.

## Attività

Chiudere il ciclo `VALIDATO → INTEGRATO → CERTIFICATO` del RAG V5 locked e
dell'entry point CLI autorevole, preservando evidenze storiche e rollback.

## Evidenze

- Qualità: regressione integrata V2 10/10, SHA-256
  `f2d54944085b1586067679ac76fb6e2696e5ab24d36d40e84cd3ffb2d4f76a55`.
- Confronto V4/V5: V4 0/10 casi eleggibili per assenza fonti gold; V5 10/10,
  SHA-256 `7e16980a7ef014b991e4c92905e85a490163bf19420368dbbb7109566fa38f56`.
- Freeze runtime post-promozione: SHA-256
  `f5718a39978495894964f79c4a9b5f4be42277affde88fe692b5382cb7c6cca9`.
- Promozione default: commit `040c6a5`; rollback `--legacy-profile`.
- Smoke post-promozione: SHA-256
  `81481332bac25ab6cfdac60f72060e1dcb4f2cdff93fe95c402c69989deee472`;
  output/evidenze identici al caso validato, indici invariati.

## Riconciliazione degli stati

| Componente | Evidenza isolata | Stato corrente |
|---|---|---|
| Source-aware e coerenza autore | VALIDATO | INTEGRATO nel default |
| Exercise candidate | VALIDATO | INTEGRATO nel default |
| Priorità riferimenti esatti | VALIDATO | INTEGRATO nel default |
| Heading routing V4 | VALIDATO | INTEGRATO nel default |
| Coperture concettuali | VALIDATO | INTEGRATO nel default |
| Filtri post-perdita e consolidamento | VALIDATO | INTEGRATO nel default |
| Guida qualitativo/comparativo | VALIDATO | INTEGRATO nel default |
| Profilo completo | 10/10 VALIDATO | INTEGRATO e CERTIFICATO |

I report storici conservano lo stato raggiunto nel singolo esperimento; questa
tabella è la fonte corrente che attesta la successiva integrazione.

## Ambito e decisione

`CERTIFICATO` per il manifest locked, il runtime congelato e il wrapper CLI
predefinito. Non esiste un servizio applicativo RAG attivo sulla VPS: eventuale
esposizione HTTP/UI, monitoraggio operativo o deployment applicativo è un
progetto successivo e non è implicitamente certificato da questo closeout.
Non ripetere benchmark, confronto o fingerprint senza una modifica tecnica.
