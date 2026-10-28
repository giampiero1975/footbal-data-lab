# Runtime Coverciano remediation V8

Data: 2026-10-27. Ramo: `codex/rag-coverciano-remediation`.

## Perimetro

Riesecuzione RAG-only delle dieci domande congelate, con spalla esterna
disabilitata, sei evidenze, contesto 8.192 e gate tattico fail-closed. Indice
VPS invariato a 6.410 chunk; nessuna chiamata Gemini o OpenRouter.

## Risultato

- 10/10 JSON conservati; zero citazioni fuori intervallo e zero troncamenti;
- tempo medio 254,05 s per caso;
- gate superato: casi 1, 2 e 5; respinto: 3, 4, 6, 7, 8, 9 e 10;
- rispetto a V7 i troncamenti sono scesi da due a zero, ma la completezza resta
  3/10: il target 26/30 non è dimostrato.

| Caso | Esito V8 | Diagnosi deterministica |
|---|---|---|
| 1 | PASS | copertura completa |
| 2 | PASS | risposta sostanzialmente completa; il ricalcolo segnala un falso negativo sul perché |
| 3 | FAIL | audit richiedeva impropriamente ruoli offensivi dell'area in una domanda di difesa del cross; motivazioni poco esplicite |
| 4 | FAIL | requisiti `tempo di volo` e azione post-ricezione attivati da parole generiche, non dalla domanda |
| 5 | PASS | risposta completa; falso negativo lessicale sul perché |
| 6 | FAIL | la risposta contiene “palla è considerata scoperta”, non riconosciuto dal match esatto |
| 7 | FAIL | ricezione tra le linee e azione successiva ancora troppo generiche |
| 8 | FAIL | contaminazione reale: introduce difesa del cross in una domanda offensiva; numeri di maglia non richiesti |
| 9 | FAIL | principio palla coperta/scoperta corretto, ma numeri di maglia inventati |
| 10 | FAIL | trasformazione applicativa fragile e comunicazione rilevata in modo incoerente |

## Decisione

V8 è **ESEGUITA, NON VALIDATA**. Il gate ha finalmente impedito che errori
semantici passassero come risposte valide, ma ha anche mostrato tre falsi
negativi strutturali. V9 introduce una differenza tecnica documentata:
requisiti di dettaglio condizionati alla domanda, matching relazionale della
palla coperta/scoperta, riconoscimento più robusto della motivazione, divieto
dei numeri non presenti nella traccia e repair espresso in istruzioni tattiche
leggibili anziché etichette interne. Segue nuovo rerun delle stesse dieci
domande; non è un benchmark nuovo.
