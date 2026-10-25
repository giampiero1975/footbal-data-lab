# Stato consolidato corrente — 2026-10-25

Questa pagina è il punto di ingresso per lo stato attuale. La cronologia completa
resta in `docs/experiment-register.md`; gli stati storici non sono cancellati e
non prevalgono sugli stati correnti qui riconciliati.

## Stato corrente verificato

| Ambito | Stato corrente | Evidenza e limite |
|---|---|---|
| Pipeline V5 locked e wrapper CLI | **CERTIFICATO** | Regressione 10/10, confronto di eleggibilità V4/V5, freeze runtime, default e rollback in `docs/v5-certification-closeout-01.md`; commit di promozione `040c6a5`, closeout `e2c093a`. La certificazione vale soltanto per manifest locked, runtime congelato e wrapper CLI verificato. |
| API HTTP locale e pannello | **INTEGRATO** | Contratto e deployment in `docs/rag-v5-http-api-validation-01.md`; pannello, feedback privo di contenuti, fonti espandibili ed export in `docs/knowledge-panel-api-v1.md` e `docs/knowledge-panel-feedback-export-01.md`; commit principali `9472564`, `60bf7b2`, `77a69df`, `e9dda93`. Servizio vincolato a localhost; non è certificato dal closeout locked. |
| Osservabilità e manutenzione | **INTEGRATO** | Metriche e vista qualità in `docs/rag-v5-api-observability-01.md`; manutenzione settimanale in `docs/rag-v5-runtime-maintenance-01.md`; commit `fbf4162`, `a48b516`, `5b877cb`, `1e9f167`. |
| Holdout esterno Drive11 | **VALIDATO** | 6/6, zero citazioni invalide, report e hash in `docs/v5-external-drive11-holdout-01.md`; commit `21eaada`, validazione `31ff5ad`. Non estende la certificazione locked alla collection Drive11 o a domande arbitrarie. |
| Benchmark applicativo generico | **VALIDATO** | Breve, medio e complesso 3/3; cronologia del fallimento intermedio e risultato finale in `docs/rag-v5-api-profile-benchmark-01.md`; correzioni `37d3ee0`–`3a0af91`, riconciliazione `936b4c4`. Non è certificazione universale. |
| Corpus FIGC5 | **VALIDATO e INTEGRATO** | Cinque PDF elaborati, 214 chunk aggiunti, API su 6410 chunk/157 fonti; gate Soncin e regressione composita 10/10 in `docs/figc5-candidate-integration-01.md`; commit di riconciliazione `936b4c4`. La collection 6196 resta rollback. |

## Perimetro della certificazione

`CERTIFICATO` si applica esclusivamente al manifest locked, al runtime congelato
e al wrapper CLI predefinito descritti nel closeout. Non certifica:

- tutte le domande tattiche possibili;
- l'intera collection Drive11 da 6196 chunk;
- la collection operativa FIGC5 da 6410 chunk;
- API HTTP, pannello, monitor o futuri consumer esterni.

Questi ambiti possiedono evidenze separate e i loro stati sono `VALIDATO` o
`INTEGRATO` secondo la tabella, non `CERTIFICATO`.

## Attività tecniche realmente aperte

- **DA FARE:** osservazione prolungata del servizio. Il reboot completo
  dell'host, il riavvio della sola unità e il
  recovery systemd sono VALIDATI e non vanno ripetuti senza una modifica tecnica;
  evidenza reboot in `docs/rag-v5-full-reboot-validation-01.md`.
- **IMPLEMENTATO:** Nginx, Certbot e configurazioni per
  `https://footballlab.byoursite.com`; bootstrap espone soltanto la challenge
  ACME. Certificato e collaudo: **BLOCCATO** finché il record DNS `A` non risolve
  verso `163.5.26.155`; 8088 resta locale.

## Decisioni facoltative, non debiti tecnici

- Collegare `api/rag_v5_client.py` a un consumer esterno quando tale applicazione
  esisterà; il repository non contiene oggi quel consumer.
- Valutare inferenze parallele soltanto con risorse dedicate e un benchmark di
  capacità; il worker seriale è una scelta operativa valida.
- Avviare una nuova certificazione su Drive11, FIGC5 o domande arbitrarie solo con
  un nuovo perimetro, gold congelato e criteri espliciti. Le validazioni correnti
  non rendono obbligatoria questa estensione.

## Regola di lettura della cronologia

Le righe `IMPLEMENTATO`, `ESEGUITO` o `VALIDATO` più vecchie descrivono lo stato
raggiunto da quello specifico esperimento nel momento in cui fu registrato. Non
sono attività automaticamente aperte quando una voce successiva, sostenuta da
nuove evidenze, registra `VALIDATO`, `INTEGRATO` o `CERTIFICATO`. Le attività
aperte correnti sono esclusivamente quelle elencate sopra e nel blocco iniziale
del TODO.
