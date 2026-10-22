# RAG V5 shadow NLI V2 — adversarial result (2026-10-22)

Source: user-supplied `rag_v5_shadow_adversarial_20261022.json`; 11 curated controls, 9 matching expected labels, 0 inference errors.

Mismatches:
- `low_block_wrong` (q3/F1): expected `contradicted`, actual `insufficient`. Source recommends width against low blocks rather than vertical play; inspect semantic contradiction threshold.
- `all_systems` (q5/F1): expected `insufficient`, actual `contradicted`. Source discusses three systems, not all possible systems; avoid treating lack of universal support as explicit contradiction.

Other nine cases matched their curated expectations. This 9/11 score is not population accuracy and does not supersede the baseline 20/20 `supported` classifications. Keep production RAG, Chroma, and canonical NLI V2 instruction unchanged while comparing prompt variants on the same fixed controls. Any improvement should be tested for regressions on positive and negative cases before adoption.
