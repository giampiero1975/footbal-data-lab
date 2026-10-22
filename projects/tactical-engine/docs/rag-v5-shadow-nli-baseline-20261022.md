# RAG V5 shadow NLI V2 — baseline 2026-10-22

## Provenance
- VPS input: `projects/tactical-engine/evaluation/reports/rag_v5_shadow_baseline_20261022.json` (5 questions).
- Runner: `projects/tactical-engine/scripts/run_rag_v5_shadow_nli_baseline.py`.
- VPS result supplied by user: `projects/tactical-engine/evaluation/reports/rag_v5_shadow_nli_results_20261022.json`.
- Model contract: `qwen3.5:9b`, V2 instruction, structured JSON, `think=false`.
- This record is based on inspection of the user-supplied result, not a direct remote VPS read.

## Observed
- 15 annotated claims; 20 claim–cited-evidence pairs.
- Attempted 20; completed 20; errors 0.
- All 20 pair labels: `supported`; all 15 claim statuses: `supported_by_cited_evidence`.
- Sum of per-pair elapsed seconds: 302.084 (~5m02s); not a total wall-clock benchmark.
- Source report and production Chroma/RAG were not mutated by the shadow runner.

## Manual review / limitations
- **q3_c02** is marked `supported`, but its claim says verticalization is preferable against low defensive blocks *or* space behind the defense. Its cited F1 says the opposite for deep blocks: use width and crossing, while verticalize when space exists behind. This is a likely NLI false positive and an answer-generation factual inconsistency. Requires independent review; do not treat 20/20 as verified factual correctness.
- **q3_c01** cites F1 for examples (heavy pitches, time disadvantage) which are not present in that truncated excerpt. This is another possible false positive due to partially supported composite claims.
- **q5** largely enumerates static system-specific pros/cons, not the decision and consequences of changing formation *during a match*. Pairwise citation support does not measure question relevance.
- **q5_c03** says the metodista advantage applies `indipendentemente dal sistema adottato`, while F1/F2 explicitly discuss three particular systems; beware unsupported generalization.
- **q2_c01** describes a training exercise with a neutral `jolly`, not necessarily a tactical match mechanism.
- **q5_c04** combines statements sourced from different excerpts. Pairwise judging of composite claims may label each excerpt supported even though no individual excerpt supports the entire composite claim.

## Decision
- Technical shadow inference smoke: **PASS** (20/20 complete, zero errors).
- NLI accuracy / factual faithfulness / question relevance: **NOT VALIDATED**.
- Next: add adversarial/negative and partial-support controls; split composite claims into atomic claims; review q3_c02 and q5 relevance independently. Keep RAG V5 unchanged until controlled regression tests.
