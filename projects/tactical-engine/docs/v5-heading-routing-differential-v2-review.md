V5-HEADING-ROUTING-INTEGRATION-02 — VPS differential v2

Attività: verifica del routing generico con riserva di heading. Script: run_rag_v5_locked_candidate_v2.py --execute --heading-routing --only-ids fresh_03. Commit: 2e42ac4, f86df6c, 8260c62. Report VPS: evaluation/v5_heading_routing_generic_fresh03_v2.json, fornito dall'operatore.

Risultato: ESEGUITO; heading_reserved_ids=4, fonte riservata FOOTBALL_DATA_LAB_Attacco_della_Profondita_Manuale, intestazioni 3-4-2-1, 3-5-2, 4-2-3-1, 4-3-3. Fonte pertinente Transizioni Offensive e Difensive non selezionata; manca 4-4-2. Risposta con limite comparativo ma senza copertura completa. Citazioni invalide 0; Chroma 5319 prima e dopo, invariato; elapsed 133.88 s.

Decisione: non VALIDATO, non INTEGRATO né CERTIFICATO. La riserva heading funziona ma il ranking della fonte basato su overlap del nome e numerosità heading sceglie il manuale sbagliato. Prossimo test ammesso solo dopo modifica documentata alla pertinenza della fonte. Benchmark locked 5/10 invariato. Stato: ESEGUITO.
