# Benchmark live Coverciano 100 — protocollo RAG/Groq/Gemini Cloud

Data avvio: 2026-10-26. Stato: **ESEGUITO 1/100**, campagna in corso.

## Protocollo

Gemini Cloud formula una domanda alla volta e valuta la risposta; il pannello
pubblico esegue retrieval, bozza RAG e copilot Groq. Ogni caso conserva domanda,
bozza, evidenze, esito Groq, tempi, voto e giudizio esterno. Un caso con copilot
non disponibile resta nel campione come errore di pipeline e non viene presentato
come risposta assistita.

## Caso 001 — 4-3-3 sotto 1-0 contro 5-4-1 basso

- Job: `7c9d0148`.
- Esito pannello: `succeeded` con 6 evidenze, ma copilot non disponibile.
- Tempo totale pannello: 193 s; generazione RAG riportata: 159,82 s, 510 token.
- Groq: circa 11 s tra gli eventi start/finish; errore
  `GROQ_PASS2_UNKNOWN_OR_DUPLICATE_FINDING`.
- Evidenze recuperate: `Manuale_Diagonali_Difensive` p.47;
  `FOOTBALL_DATA_LAB_Scalate_Difensive_Manuale` p.24;
  `Allegati_14112014151551` p.5; `catene_laterali_442_Pioli` pp.3-4;
  `Allegati_179201015532` pp.10-13; `Allegati_184201114337` pp.25-27.
- Valutazione Gemini Cloud della bozza RAG: **18/30**.
- Criticità tattica principale: la bozza interpreta il terzino destro ammonito
  come proprio e propone di sostituirlo, mentre la traccia lo identifica come
  avversario. Seguono incoerenza nel passaggio al 3-4-3, mancato isolamento
  dell'ala sinistra contro l'ammonito e gestione troppo prudente del finale.
- Decisione: non moltiplicare 99 volte lo stesso errore. Correggere prima il
  contratto meccanico PASS2, preservando i gate semantici e documentali, quindi
  ripartire dalla domanda 2 già formulata da Gemini.

## Correzione differenziale dopo il caso 001

Il response schema PASS2 viene derivato dagli ID reali di caso e finding prodotti
dal PASS1. Gli ID sono vincolati con enum nello schema inviato a Groq; il
validatore locale continua a imporre copertura esatta, associazione caso/finding,
etichette esistenti, citazioni valide e applicazione dei soli finding supportati.
Nessuna correzione tattica viene inventata o normalizzata localmente.

Verifica offline: test copilot 12/12; suite Groq combinata 22/22. Chiamate API
durante la correzione: zero. Smoke live successiva necessaria tramite domanda 2.

