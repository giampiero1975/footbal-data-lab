# V5 external Drive11 holdout 01

Data: 2026-10-25. Stato: VALIDATO 6/6; non CERTIFICATO universalmente.

## Differenza tecnica

Il benchmark locked 10/10 usa dieci casi e la collection storica. Questo holdout contiene sei domande nuove ricavate esclusivamente da fonti Drive11 assenti dalla collection certificata 5319. Domande, fonti, pagine, ID evidenza e claim obbligatori/vietati sono congelati prima della prima generazione.

Manifest: `evaluation/rag_v5_external_drive11_holdout_v1.json`, SHA-256 `ef3acb4f3499553e1f525d0c09f40bc69eff1a78f6f9990c0ca36d1dbe83c651`.

Fonti: Vincenzo Italiano, Contran, Andrea Maldera, Lorenzon, Luciano Vulcano e Francesco Baldini. Il runner `run_rag_v5_external_holdout_v1.py` richiede l'hash atteso, almeno cinque casi completi, output nuovo, collection/count espliciti e invarianti dell'indice. Non modifica il wrapper locked né attribuisce automaticamente una certificazione.

## Gate

1. verificare sulla VPS che ogni evidence ID appartenga alla fonte/pagina congelata;
2. dry-run hash del runner;
3. una sola esecuzione generativa dei sei casi;
4. adjudication claim-level mandatory/forbidden, citazioni e integrità indice;
5. aggiornare TODO e registro senza trasformare il risultato in certificazione universale.

## Risultato

Preflight: 6/6 evidence ID presenti nella fonte e pagina congelata, zero errori. Unica esecuzione: `COMPLETE 6/6`, 668,43 secondi complessivi, zero citazioni invalide, collection 6196→6196. SHA-256 report `e7cbcfcaaf1e069c45551c8a9e7fcfd3deb08fa31e310acc263af3c035b6f04a`.

Adjudication interna claim-level: 6/6 PASS. Ogni risposta contiene tutti i mandatory claim, nessun forbidden claim e usa come F1 l'evidence ID congelato con fonte e pagina corrette. Il risultato dimostra generalizzazione sulle sei nuove fonti Drive11; non certifica tutte le domande arbitrarie né sostituisce il locked 10/10.

Attività: benchmark esterno Drive11. Script: runner e manifest sopra. Commit implementazione `21eaada`. Report runtime: `evaluation/runtime-archive/rag_v5_external_drive11_holdout_v1.json`. Risultato: 6/6 PASS. Decisione: VALIDARE l'estensione fuori locked; non ripetere il test e usare i sei casi come regressione. Stato: VALIDATO.
