# Espansione corpus tattico Drive11 — candidato V5

Stato: IMPLEMENTATO; esecuzione e validazione DA FARE.

## Motivazione e isolamento

Il titolare ha autorizzato il 2026-10-24 l'acquisizione degli 11 PDF calcistici censiti in `V5-TACTICAL-CORPUS-RECONCILIATION-01`, dopo la chiusura dei test sul corpus certificato. Il file privato/non calcistico resta escluso da download e ingestion.

La prova è tecnicamente nuova perché aggiunge documenti al corpus. Le fonti sono collocate in `knowledge/candidates/drive11`, l'output Docling avrà una directory candidata separata e l'indice sarà `dribbling_tactics_v5_multisource_drive11_candidate_v1`. La collection certificata `dribbling_tactics_v5_multisource` (5319 chunk) non deve essere scritta.

## Gate

1. verificare 11 PDF, dimensioni e hash;
2. completare Docling senza errori e controllare output/meta;
3. creare una collection isolata contenente baseline più Drive11;
4. verificare conteggi, provenienza e immutabilità della baseline;
5. eseguire il benchmark locked attraverso il runner parametrizzato;
6. promuovere solo in assenza di regressioni e con evidenze registrate.

Flusso: Attività = espansione corpus; Script = pipeline V5 parametrizzata; Commit = DA FARE; Report = questo documento; Risultato = IMPLEMENTATO; Decisione = esecuzione candidata isolata; Stato = IMPLEMENTATO.
