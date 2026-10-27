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

## Chiusura differenziale V10.1/V10.2

I casi 5, 6 e 8 sono stati rigenerati e hanno superato il gate. Il caso 10 è
stato rigenerato con una trasformazione esplicita e coerente: ala fuori,
centrale dentro, linea a tre, terzini quinti, ala residua seconda punta e
centrocampo invariato. Il primo gate ha rilevato correttamente numeri/ruoli
incompatibili; la prova finale li ha eliminati. L'unico FAIL residuo era un
falso negativo lessicale: l'audit accettava `comando/segnale` ma non i plurali
`comandi/segnali`, presenti nella risposta. Dopo la correzione e il re-audit
deterministico, il set logico finale è **10/10 PASS**, senza nuove inferenze.

Stato conclusivo: terzo giro **ESEGUITO e VALIDATO tecnicamente** sui dieci
casi; voto esterno medio >=28/30 ancora **DA VALIDARE** su almeno dieci domande
inedite con Gemini valutatore e risposta RAG invariata.
