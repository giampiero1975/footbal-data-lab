# V5-EXERCISE-BOUNDARY-WINDOWS-OFFLINE-01

Stato: ESEGUITO (analisi, non validazione dei confini).

Attivita: revisione del report exercise_boundary_windows_v1.json fornito dall'operatore.
Script: scripts/inspect_exercise_boundary_windows_v1.py.
Commit script: bb02c68.
Report: questo documento e il JSON fornito dall'operatore.

Risultato: quattro finestre esaminate.
- Allegati 468: l'intestazione successiva 469 e il titolo Partita 11vs11 a tre settori; il testo 470 contiene la descrizione. Il corpo non e assente: il criterio basato sulla prossima section_header lo tronca.
- Allegati 442: gli elementi 446 e 452 sono titoli Esercitazione 12 e 13 etichettati text; 457 introduce Esercitazione 14 ed e etichettato caption. Il segmento attribuito a 11 contiene piu esercitazioni.
- Smarcamento 108-124: il testo 118 richiama l'esercizio precedente; le intestazioni n. 1 sono ripetute. Non deduplicare automaticamente.
- Gritti 286-292: l'elemento 289 e un titolo di esercitazione etichettato text, tra figure 18 e 19. Il titolo 286 non basta a rappresentare entrambe.

Decisione: classificare i confini basati solo su section_header come insufficienti per questi casi. Progettare regole candidate sensibili al contenuto e alla provenance, con revisione manuale; nessuna modifica all'estrattore V2 o a Chroma. Nessun test ripetuto.
