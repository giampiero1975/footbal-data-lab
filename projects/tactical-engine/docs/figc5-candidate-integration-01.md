# FIGC5 candidate integration 01

## Pipeline

Cinque PDF approvati sono stati copiati in un'area isolata, elaborati con Docling e verificati 5/5 senza errori. Figure estratte: 60/60, 67/67, 72/72, 38/38 e 12/12.

Il dry-run ha prodotto 214 chunk. La collection candidata è stata costruita copiando la baseline Drive11 6196 e aggiungendo i 214 chunk: totale 6410, 157 fonti. La collection 6196 è rimasta invariata come rollback.

## Gate

- domanda nuova Soncin: fonte Soncin presente in F1-F4, risposta completa, `stop`, citazioni valide, 139,2 s;
- regressione locked candidata: prima esecuzione 9/10 per falso routing di `conclusione` verso `costruzione_conclusione_343`;
- fix generico: un token singolo identifica una fonte solo se è un nome proprio esplicito;
- differenziale `fresh_04`: solo `Transizioni.Ussia`, 5 secondi e limite statistico corretti, citazioni valide;
- regressione locked iniziale salvata in `evaluation/runtime-archive/rag_v5_figc5_locked_v1.json`, SHA-256 `3663a392506937da5bc0d989fd3ffa5cfb4578818e7815b2d2590bd4f689784d`;
- verifica differenziale salvata in `evaluation/runtime-archive/rag_v5_figc5_fresh04_routing_fix_v1.json`;
- regressione composita finale 10/10: nove risultati invariati più il solo caso `fresh_04` corretto, indice 6410 invariato.

## Decisione

Collection promossa nell'API locale; health/readiness 200, 6410 chunk e 157 fonti. Baseline 6196 conservata. Stato: **VALIDATO e INTEGRATO**; non nuova certificazione universale.
