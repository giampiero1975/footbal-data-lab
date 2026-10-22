# RAG V5 — Esito giudice shadow di pertinenza, 2026-10-22

## Provenienza
Report `rag_v5_alignment_judge_results_v1.json` caricato dall'utente e ispezionato; risultato di esecuzione VPS riportato nel file, non accesso diretto al runtime. Script: `scripts/judge_rag_v5_alignment_controls_v1.py`. Modello `qwen3.5:9b`. Modalità `shadow_only`. Riferimento `provisional_not_gold`.

## Fonti ufficiali per contratto tecnico
- https://docs.ollama.com/api/chat
- https://docs.ollama.com/capabilities/structured-outputs
- https://docs.pydantic.dev/latest/concepts/models/

I contratti JSON strutturati consentono validazione sintattica/strutturale; non garantiscono qualità semantica. Le versioni effettive del runtime VPS non sono state rilette in questa fase.

## Risultati osservati
- 10/10 tentati, 10/10 completati, zero errori.
- 6/10 accordi con etichette provvisorie; **non** equivale a 60% di accuratezza validata.
- NLI: 4/5 accordi; pertinenza: 2/5 accordi.
- `negative_scope_q5`: expected insufficient, predicted supported. Fonte circoscritta a tre sistemi, claim universalizzato a qualsiasi sistema; motivazione del giudice non giustifica il salto di quantificatore.
- `negative_pass`: expected off_target, predicted direct. Fonte sulle linee di passaggio nel corso di una singola azione, non sulle conseguenze del cambio di modulo in gara.
- `context_defense3`: expected contextual, predicted direct. Fonte sui rischi del 3-4-1-2, non sulla transizione verso tale modulo durante la partita.
- `context_counterattack`: expected contextual, predicted direct. Fonte sul dare campo per ripartire in due sistemi, non sugli effetti della variazione in gara.
- Controlli concordi: `positive_q4_diag_01`, `positive_q4_diag_04`, `positive_q5_diag_01`, `positive_q5_diag_04`, `negative_zone`, `positive_triangles`.

## Diagnosi e decisione
L'inferenza strutturata funziona. Il giudice mostra difficoltà nel preservare lo scope (tre sistemi vs qualsiasi sistema) e nel distinguere proprietà statiche di un modulo dalle conseguenze del cambiarlo in partita. Le etichette attese sono ancora ipotesi manuali: richiedono adjudication indipendente, controlli ulteriori e separazione tra tuning e holdout.

**Decisione:** nessuna modifica a Chroma, retrieval, prompt RAG di produzione o modello. Prossimo esperimento suggerito: variante di prompt shadow con regole di quantificatore e causalità temporale esplicite, confrontata sui medesimi controlli; interpretare come diagnostica, non come stima generalizzabile.
