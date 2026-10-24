# V5-FRESH03-MANUAL-INVENTORY-01

Data: 2026-10-24. Stato: ESEGUITO.

Attività: ispezione read-only della fonte interna per fresh_03, distinta dai test di retrieval e generazione.
Script: `scripts/inspect_v5_fresh03_manual_v1.py`.
Commit script: `dc28977`.
Report: `evaluation/v5_fresh03_manual_inventory_v1.json` fornito dall'operatore; presente documento.

Risultato: 62 chunk nella fonte `FOOTBALL_DATA_LAB_Transizioni_Offensive_e_Difensive_Manuale`. Chroma prima/dopo 5319, `index_unchanged=true`. Nessun chunk contiene letteralmente `4-3-3`, `4-4-2`, `3-5-2`, `3-4-2-1` o `modulo`. Pagina 4: chunk `d7ced9a0` (vertice basso), `c4559848` (due punte), `c1ab686a` (quinti), `4a924438` (due trequartisti); descrizioni tattiche compatibili con una sezione dedicata ai sistemi, ma prive di etichette esplicite nel testo indicizzato. Pagina 6 chunk `2a425cff`: confrontare situazioni simili per zona, punteggio, avversario e numero di giocatori; conteggi grezzi non dimostrano qualità del sistema. Non emerge prova causale sul rischio di cambiare modulo in partita.

Decisione: diagnosi ESEGUITA; la precedente promozione lessicale di fresh_03 non poteva selezionare etichette assenti dai chunk. Non attribuire con certezza i quattro moduli ai chunk senza riconciliazione con il documento sorgente e le intestazioni originali. Prossima attività distinta: esaminare segmentazione e conservazione delle intestazioni nel processo di estrazione, poi progettare un eventuale recupero contestuale read-only; non reindicizzare Chroma frozen e non ripetere benchmark equivalente. V5 locked 5/10 invariato, nessuna validazione/integrrazione/certificazione.

Stato: ESEGUITO.
