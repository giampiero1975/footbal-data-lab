# Analisi benchmark Glerean V4 a due assi — 2026-10-19

## Evidenza sperimentale
Report utente: `projects/tactical-engine/benchmark_ruoli_tattici_due_assi_v4.json`. Modello: `qwen3.5:9b`; fonte: GLEREAN-C018; 10 frasi sintetiche.

- **Fedeltà**: 10/10 concordanze con etichette predefinite.
- **Completezza**: 7/10 concordanze.
- **T03**: riconosciuto come `contraddittorio`; nel test precedente era stato giudicato `coerente`.
- **T08**: `coerente` per fedeltà e `parziale` per completezza.
- Disaccordi sulla completezza: T01, T02, T07, tutti classificati `parziale` anziché `completo`.

## Revisione qualitativa delle discrepanze
- **T01**: il giudice considera la parafrasi «si preparano a riceverla» incompleta rispetto a «si mettono nella condizione di ricevere», benché le due espressioni siano compatibili. Inoltre sostiene che manca «in linea con i difensori avversari», mentre la frase dice «sulla linea dei difensori avversari». Evidenza di penalizzazione ingiustificata della parafrasi.
- **T02**: inversione dei compiti dei reparti rilevata correttamente; il giudizio `parziale` sulla completezza è ambiguo, perché una frase può coprire tutti gli elementi strutturali e attribuirli erroneamente. Separare copertura degli slot e correttezza dei valori.
- **T07**: «rendersi disponibili» vs «mettersi nella condizione di ricevere» e «in corrispondenza della linea difensiva avversaria» vs «in linea con i difensori avversari» sono parafrasi plausibili; giudizio `parziale` da verificare con rubrica esplicita.

## Problema strutturale emerso nell'estrazione
In diversi casi il giudice associa `spazi laterali e centrali` anche a difensori e centrocampisti, mentre il brano li collega alla preparazione alla ricezione degli attaccanti. In T10 la motivazione parla erroneamente di «ricevimento ... a un gruppo misto». Quindi **10/10 sul verdetto finale non implica che tutte le relazioni estratte siano corrette**. Prima di uso automatico, verificare anche le relazioni intermedie.

## Decisioni
1. Non modificare il benchmark storico né le etichette in retrospettiva.
2. Mantenere separati fedeltà e copertura semantica; completezza non deve penalizzare sinonimi.
3. Valutare con esempi indipendenti e fonti differenti, controllando anche gli slot intermedi.
4. Nessuna promozione in produzione del verificatore; Chroma V4 invariato.

## Documentazione ufficiale di riferimento
- https://docs.ollama.com/capabilities/structured-outputs
- https://docs.ollama.com/api/chat
