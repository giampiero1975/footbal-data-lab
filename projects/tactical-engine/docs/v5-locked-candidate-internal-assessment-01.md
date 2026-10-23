# V5-LOCKED-CANDIDATE-INTERNAL-ASSESSMENT-01

Data: 2026-10-23. Stato: ESEGUITO (audit interno documentato; non certificazione).
Input: report VPS `rag_v5_combined_candidate_v1.json` fornito dall'operatore; manifest locked `evaluation/rag_v5_independent_candidate_v2.json`, rubriche `mandatory_claims` e `forbidden_claims`; estratti `evidence` F1–F8 del report. Nessuna nuova esecuzione VPS o modifica degli indici. Modello riportato: qwen3.5:9b; modalità source-aware + priority-exact + exercise-candidate.

## Criterio
PASS solo se tutti i claim obbligatori sono presenti, nessun claim vietato è introdotto e il ragionamento resta sostenuto dalle evidenze citate. Un ID di citazione formalmente valido non dimostra supporto semantico. Esiti binari prudenziali, valutazione interna non indipendente.

| ID | Esito | Motivazione e riscontri |
|---|---|---|
| fresh_01 | FAIL | Riporta correttamente esercitazioni 8/9/10, 10v0→10v10, zona centrale e bassa, e giudizio qualitativo di Ussia (F1,F2,F5). Tuttavia non chiarisce esplicitamente che **mancano misure comparative/percentuali**; sostituisce il limite epistemico richiesto con una tesi non dimostrata secondo cui la validità del giudizio sarebbe limitata al percorso didattico. |
| fresh_02 | PASS | Reazione immediata di chi perde palla: raggiungere l'altro spazio e impedire sei passaggi (Ussia 2/B, F1,F2). Ruoli non invertiti. |
| fresh_03 | FAIL | Non menziona l'elenco obbligatorio dei sistemi 4-3-3, 4-4-2, 3-5-2, 3-4-2-1; non esplicita l'assenza di misure causali sul rischio del **cambio modulo in gara**. La risposta devia su principi generali e altre fonti (F3,F4,F7,F8). |
| fresh_04 | PASS | 5 secondi dopo riconquista e vincolo didattico 8v8 + 2 portieri, non statistica di gara; Ussia 4/A F1,F2. |
| fresh_05 | PASS | Lato debole libero fuori ma protetto dentro, cambio gioco per 1v1/cross preparato/mezzo spazio; non promette successo universale. Manuale ampiezza F1,F6. Alcune digressioni non necessarie non alterano il nucleo richiesto. |
| fresh_06 | PASS | 11v0, aggiunta progressiva 1–2 avversari, arrivo a 10v10 e attenzione alle coperture, Ussia 11/A F1. Nessuna trasformazione in obbligo di gara. |
| fresh_07 | FAIL | Identifica pressione a invito e perdita pericolosa dai laterali (Foscarini F1), ma **confonde la zona B di Foscarini** con la zona B definita da Indiani per la difesa del calcio d'angolo (F4), importando l'«80% delle reti» da una fonte e tassonomia estranee. Affermazione attribuita a Foscarini non supportata; contaminazione semantica significativa. |
| fresh_08 | PASS | Centrocampo come fulcro e zone C/D per gestione/ripartenze (Foscarini F1,F2); playmaker braccati con poco spazio e tempo in B (F1). Nessuna affermazione che B sia sempre sicura. |
| fresh_09 | FAIL | Cita recuperatore pressato e sostegni mancanti (manuale F3) e avversario organizzato; omette la condizione esplicita del **controllo imperfetto** e soprattutto il trade-off richiesto: consolidare riduce il rischio di nuova perdita **ma concede tempo all'avversario**. Mescola in modo improprio scelte di consolidamento offensivo con ripiegamento/pressione difensiva (F5,F8). |
| fresh_10 | FAIL | Riporta correttamente le condizioni del manuale per riaggressione (F5) e i limiti di universalità, ma non soddisfa il claim obbligatorio su Ussia: adattamento al sistema e alla **pressione individuale e collettiva**; usa invece una nota bibliografica del manuale (F1) e Ussia F7 sulla perdita, senza documentare la specifica parte richiesta dell'esercitazione a p.17. |

## Risultato e decisione
**5/10 PASS** (fresh_02, fresh_04, fresh_05, fresh_06, fresh_08); **5/10 FAIL** (fresh_01, fresh_03, fresh_07, fresh_09, fresh_10). Soglia **9/10 NON raggiunta**. Risultato della sola configurazione combinata opt-in sul candidato locked; non è confronto controllato di prestazioni con altri assetti. Nessuna promozione al default, integrazione o certificazione.

Diagnosi prioritaria senza ripetere test equivalenti: (1) controllo coerenza semantica di fonte/tassonomia per omonimie «zona B»; (2) verifica copertura di tutti i mandatory claims e delle astensioni, in particolare confronto qualitativo vs statistico; (3) verifica pertinenza delle evidenze per domanda e fonte richiesta, soprattutto fresh_03 e fresh_10. Ogni nuovo esperimento richiede differenza tecnica documentata e registrazione preventiva.
