# Inventario VPS tactical-engine — 22 ottobre 2026

## Fonte e perimetro
Inventario di 207 percorsi di file fornito dall'utente dalla VPS, comando `find ... -maxdepth 3 -type f`. Confronto con l'albero tracciato GitHub e documentazione `docs/script-inventory.md`, `experiments/README.md`. La lista non include file oltre profondità 3, perciò **non dimostra che `evaluation/reports/` sia vuota**; i report in quella directory sono a profondità 4.

## Conteggi per percorso
- Radice `tactical-engine/`: 12 JSON, tutti con nomi di audit/benchmark.
- `eval/`: 8 JSON, di cui 7 tracciati su GitHub; `claim_fidelity_results_v1.json` risulta solo nella lista VPS.
- `evaluation/`: 4 JSON tracciati su GitHub, più documentazione Markdown.
- `experiments/`: README del registro.
- `scripts/`: 146 script Python.
- `docs/`: 17 Markdown.
- `tests/`: 1 script Python.
- `evaluation/reports/`: directory confermata dall'utente, contenuto non censito per limite di profondità.

## Dodici JSON nella radice — classificazione prudenziale
Tutti da **conservare temporaneamente** fino a verifica dei riferimenti e confronto con documentazione; non sono gold noti e appaiono output storici:
1. audit_two_stage_tactical_nli_v1.json
2. benchmark_direct_three_label_external_v1.json
3. benchmark_direct_three_label_fresh_v1.json
4. benchmark_direct_three_label_v2_fresh_v1.json
5. benchmark_minimal_verdict_external_v1.json
6. benchmark_strict_tactical_adversarial_v1.json
7. benchmark_strict_tactical_nli_v1.json
8. benchmark_tactical_nli_source_disjoint_30_v2.json
9. benchmark_tactical_nli_stress_100_v2.json
10. benchmark_transition_independent_v2.json
11. benchmark_two_stage_external_holdout_v1.json
12. benchmark_two_stage_tactical_nli_v1.json

**Aggiornamento 2026-10-24:** questi dodici file e altri tre output JSON
successivamente comparsi nella radice sono stati riconciliati e spostati in
`evaluation/runtime-archive/`. La radice `tactical-engine/` non contiene più
JSON. Manifest corrente: `evaluation/runtime_evidence_manifest_v1.json`.

## Dataset da proteggere
`eval/`: claim_fidelity_adversarial_v1.json, claim_fidelity_external_sources_holdout_v1.json, claim_fidelity_fresh_sources_holdout_v1.json, claim_fidelity_gold_v1.json, tactical_nli_source_disjoint_30_v1.json, tactical_nli_stress_100_v1.json, tactical_transition_independent_v1.json. `claim_fidelity_results_v1.json` sembra invece un risultato, da verificare.

`evaluation/`: glerean_figure_evidence_v2.json, gold_glerean_ampiezza_v1.json, gold_glerean_principi_v1.json, h10_multisource_football_pilot.json. Da conservare.

## Errore metodologico accertato
I nuovi script shadow NLI usano path relativi predefiniti `evaluation/reports/`, creano directory con `mkdir(parents=True, exist_ok=True)` e richiedono un baseline locale che l'utente ha cancellato. Non hanno verificato prima il layout esistente. Il baseline non può essere sostituito dai soli report aggregati.

## Prossime azioni sicure
1. Non eliminare alcun file sulla base dei soli nomi.
2. Per `evaluation/reports/` usare un inventario mirato con profondità adeguata: il precedente `find -maxdepth 3` non elenca i file a profondità 4.
3. Esaminare dipendenze degli script dai JSON in radice e distinguere output storici da input riproducibili.
4. Formalizzare una sola destinazione dei report; non spostare gli output storici finché non si verificano dipendenze.
5. Correggere i runner shadow per validare input e destinazione prima di generare file; evitare creazione silenziosa di directory.
6. Mantenere invariati RAG V5, Chroma, modello e prompt canonico.

Stato: audit statico, nessuna cancellazione o spostamento; utilizzo runtime non accertato.
