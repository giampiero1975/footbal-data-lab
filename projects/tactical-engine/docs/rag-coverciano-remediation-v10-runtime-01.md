# Terzo giro Coverciano — V10

Data: 2026-10-27. Ramo: `codex/rag-coverciano-remediation`.

## Perimetro ed esito

Terzo rerun RAG-only delle dieci domande congelate, senza spalla e senza nuove
chiamate Gemini. Sei evidenze, contesto 8.192, limite 900 token; indice invariato
a 6.410 chunk.

- 10/10 risultati conservati; zero citazioni invalide e zero troncamenti;
- tempo medio 224,95 s;
- gate runtime PASS 8/10; casi 5 e 6 respinti;
- caso 5: risposta autocontraddittoria (“scivola all'indietro traslando
  lateralmente”);
- caso 6: etichetta interna `field_zone` ancora esposta.

L'audit umano successivo ha inoltre respinto due falsi PASS del gate:

- caso 8: numeri di maglia introdotti come esempi pur non presenti nella
  domanda;
- caso 10: due esterni difensivi trasformati genericamente in centrocampisti
  centrali, senza una geometria coerente della linea a tre e dei quinti.

## Decisione

V10 è **ESEGUITA, NON VALIDATA**: il gate più severo ha impedito due risposte
inadeguate ma non ha ancora coperto tutte le relazioni. V10.1 aggiunge
sanificazione puramente sottrattiva per etichette/locuzione contraddittoria,
rilevamento dei numeri introdotti con “es.” e controllo della trasformazione
dei ruoli. Per evitare test duplicati vengono ripetuti soltanto i casi 5, 6, 8
e 10; gli altri sei risultati restano congelati.
