V5-HEADING-ROUTING-INTEGRATION-02

Stato: IMPLEMENTATO. Script: v5_heading_routing_v1.py, v5_heading_reservation_v2.py, smoke_test_rag_v5_e2e.py. Commit: 2e42ac4, f86df6c, 8260c62.

Attività: correggere la perdita di heading nella top8 osservata nel differenziale v1. Risultato: rimosso il salto di manuali con più di otto heading; introdotta riserva di evidenze per gruppi di formazioni dello stesso manuale. Nessuna nuova esecuzione VPS. Decisione: nuovo test differenziale tecnicamente distinto, controllando manuale selezionato, heading_reserved_ids, risposta e Chroma. Benchmark 5/10 invariato; non VALIDATO, INTEGRATO o CERTIFICATO.
