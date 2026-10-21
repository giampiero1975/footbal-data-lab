# Piano di regressione RAG V5 — dopo benchmark prompt A/B

## Evidenze verificate dal report `benchmark_rag_v5_prompt_ab.json`
- Collection `dribbling_tactics_v5_multisource`, 5319 chunk prima e dopo.
- 5 domande, 8 evidenze per domanda, stessi candidati per baseline e strict.
- Tempo complessivo generazione baseline: 324.47 s; strict: 1000.72 s (~3.08x).
- Q3 baseline: suggerisce erroneamente verticalizzazione contro difese basse, mentre la fonte Bonacini dice di privilegiare manovre aggiranti/ampiezza.
- Q5: confusione fra proprietà dei singoli sistemi e conseguenze di cambiare sistema durante la gara.
- Q4: fonti Trombetta `Dislocazione a triangoli...` e `triangoli_20_squad_20_Trombetta` contengono estratti identici o quasi-identici e sono recuperate entrambe.

## Prossimi passi (read-only prima di qualsiasi modifica)
1. Congelare prompt baseline e set di 5 domande come riferimento.
2. Scrivere un audit deterministico del JSON che segnali: citazioni fuori range, copertura delle fonti, duplicati esatti/normalizzati e tempi; non confondere la validità sintattica delle citazioni con la fedeltà fattuale.
3. Definire test di regressione mirati:
   - Q3: contro difesa alta -> profondità possibile; contro difesa bassa -> preferire ampiezza; non invertirli.
   - Q5: esplicitare quando le evidenze trattano solo vantaggi/svantaggi di moduli isolati e non l'effetto di un cambio in gara.
   - Q4: alias/duplicati cross-source non devono consumare slot di evidenza.
4. Validare il comportamento di deduplicazione prima in simulazione, senza scritture a Chroma.
5. Provare una modifica alla volta (retrieval/alias, selezione evidenze o prompt breve), comparando gli stessi quesiti e controllando le regressioni.
6. Nessun deploy di prompt strict; nessuna reingestione o alterazione V5 finché i controlli non passano.

## Nota
Questa è pianificazione tecnica basata sul report; i test di regressione aggiuntivi non sono ancora eseguiti.
