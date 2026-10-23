# V5-EXERCISE-BOUNDARY-ANOMALY-REVIEW-01

Stato: ESEGUITO (revisione delle evidenze, non validazione).

Attivita: riesaminare le anomalie nel report exercise_body_context_v1.json.
Script: inspect_exercise_body_context_v1.py, nessuna nuova esecuzione.
Commit: questo documento.
Report: questa revisione su 22 candidati.

Risultati:
- Allegati #/texts/468 (esercitazione 16): zero elementi prima di #/texts/469; contenuto e confine non determinabili.
- Smarcamento #/texts/115 e #/texts/122: intestazioni n. 1 ripetute, descrizioni iniziali simili (4+4 e campo 32x32); riferimenti distinti non dimostrano esercizi distinti. Il titolo collettivo #/texts/108 contiene anche #/texts/109, testo Esercitazione n. 1.
- Gritti #/texts/286: figure 18 e 19 sotto un titolo; non separare automaticamente per figura.
- Allegati #/texts/442 (esercitazione 11): 19 elementi, inclusi descrizioni 10vs6 e partita a tre squadre 4vs4; possibile accorpamento, non dimostrato.
- Smarcamento #/texts/93 e #/texts/100: titoli collettivi, con piu list_item; non considerarli singole esercitazioni per il solo titolo.

Decisione: mantenere review_required; non validare confini, non deduplicare o suddividere automaticamente. Prima di ulteriori controlli riconciliare gli elementi intermedi mancanti nelle evidenze, limitandosi ai riferimenti ambigui. Nessun replay Ussia, nessuna modifica V2, pipeline o Chroma.
