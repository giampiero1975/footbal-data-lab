# RAG V5 — diagnosi differenziale su report E2E esistente

Data: 2026-10-23. Stato: ESEGUITO.

## Input immutati
- Report: rag_v5_candidate_v2_runtime_report.json (10 risposte gia generate; allegato al progetto).
- Gold candidato: evaluation/rag_v5_independent_candidate_v2.json; SHA256 c160a8a2128e05eda50842230c5f4aad2bf9a8085f4240c8ee893ed2e3a3fa71.
- Pipeline report: dense24 -> mMARCO CPU -> exact-alias collapse -> top8; collection 5319 invariata.
- Nessuna nuova generazione, nessuna modifica al gold o a Chroma.

## Analisi per caso
| Caso | Evidenza nel report | Difetto / decisione |
| --- | --- | --- |
| fresh_01 | Ussia pp21-23 F1-F3 | Fonte primaria presente; risposta non riporta giudizio qualitativo zona alta e dettagli di ripartenza. Revisione di completezza/fedelta. |
| fresh_02 | Ussia pp10-11 F1 | Risposta centrata su spostamento e sei passaggi. |
| fresh_03 | Manuale transizioni sezione moduli non nei top8 | Recupera fonti generiche, non enumera i quattro moduli richiesti. Retrieval source-aware da studiare. |
| fresh_04 | Ussia p48 F5 e' indice, non testo 4/A | Manca regola cinque secondi; recuperare il chunk effettivo prima di modificare il prompt. |
| fresh_05 | Manuale ampiezza pp3-4 F1/F6 | Risposta contiene lato debole e finalita cambio gioco. |
| fresh_06 | Ussia pp23-25 F1/F3 | Progressione 11v0, oppositori e coperture citate; digressioni non necessarie. |
| fresh_07 | Foscarini p22 non nei top8 | Confusione tra laterali (giocatori) e rimessa laterale; difetto di retrieval e disambiguazione. |
| fresh_08 | Foscarini pp2-3 F1 | Risposta copre centrocampo, playmaker e zona B; verificare digressioni. |
| fresh_09 | Manuale transizioni F3/F4 | Condizioni parziali, omette costo del consolidamento: tempo concesso all'avversario. |
| fresh_10 | Manuale transizioni F1 bibliografia, F5 condizioni | Mancano i passaggi tattici originali di Ussia e la distinzione esplicita fra pressione alta e riaggressione. |

## Decisione e prevenzione duplicati
- Non ripetere i test shadow source-aware gia VALIDATI (V5-REF-05).
- Differenza tecnica ammissibile per lavoro successivo: integrazione source-aware nel runner effettivo e verifica delle evidenze mancanti, non nuovo replay equivalente.
- Non ottimizzare il prompt sulle stesse 10 domande e poi chiamarle holdout indipendente.
- La soglia ufficiale richiede almeno 9 domande PASS con rubric 0-10, vincoli di fedelta e coerenza, revisione e dataset separato. Il precedente 4/10 e' una riconciliazione binaria preliminare sui mandatory, non un punteggio rubric indipendente.
- Nessun nuovo test VPS eseguito in questa sessione: accesso remoto alla VPS non disponibile da questo connettore.
