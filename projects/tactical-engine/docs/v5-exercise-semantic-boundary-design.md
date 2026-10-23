# V5-EXERCISE-SEMANTIC-BOUNDARY-DESIGN-01

Stato: ESEGUITO (progettazione, non implementazione).

Attivita: definire regole candidate di segmentazione semantica sulla base delle quattro finestre gia ispezionate.
Script: nessun nuovo script o test.
Commit: questo documento.
Report: questo disegno, fondato su docs/v5-exercise-boundary-windows-findings.md.

## Regole candidate
1. Valutare titolo e contenuto indipendentemente da label Docling: section_header, text e caption possono contenere un inizio esercitazione.
2. Un titolo numerato con forma "Esercitazione 12." (Allegati #/texts/446), "Esercitazione 13." (#/texts/452) o "Esercitazione 14 ..." (#/texts/457) e un candidato exercise_start; preservare source, self_ref e pagine.
3. Il titolo descrittivo "Partita 11vs11 a tre settori" (#/texts/469) segue "Esercitazione 16" (#/texts/468): proporre associazione titolo principale + sottotitolo, non esercitazione vuota. Il corpo candidato inizia a #/texts/470.
4. "Regole e scopo del gioco" (Smarcamento #/texts/112) e "Descrizione" (Allegati #/texts/465) sono sottosezioni, non nuovi esercizi per il solo label section_header.
5. Un titolo descrittivo "Esercitazione per il tiro in porta da distanza ravvicinata" (Gritti #/texts/289, label text) e candidato exercise_start distinto dal titolo #/texts/286. Le figure 18 e 19 non costituiscono da sole identificatori di esercizio.
6. Titoli ripetuti "Esercitazione n. 1" (Smarcamento #/texts/109, #/texts/115, #/texts/122) non vanno deduplicati o separati automaticamente: il riferimento a "esercizio precedente" in #/texts/118 impone review_required.
7. I titoli plurali o di raccolta sono section_boundary candidati; non diventano exercise_start senza evidenza di un'unita operativa.

## Procedura di decisione
Per ogni candidato raccogliere source, self_ref, label, pagina, testo titolo, titoli adiacenti e corpo. Distinguere exercise_start, section_boundary, non_exercise e review_required come etichette di revisione, non stati del progetto. In presenza di ambiguita usare review_required; nessuna assegnazione automatica definitiva.

## Criteri di accettazione
Applicare gli otto criteri di docs/v5-exercise-heading-acceptance-plan.md; evitare collisioni di numerazione, confondere rapporti di giocatori con ID o trasformare automaticamente una figura in esercitazione. Prima di ogni eventuale prototipo: nuova riconciliazione di TODO, registro e script, con differenza tecnica documentata rispetto ai test precedenti.

## Decisione
Progettazione conclusa. Successiva attivita consentita: prototipo offline read-only di classificazione candidate sulle sole evidenze disponibili, con revisione manuale; non modificare estrattore V2, Chroma, benchmark o pipeline. Nessuna integrazione o certificazione.
