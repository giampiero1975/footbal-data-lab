# V5-HEADING-ROUTING-INTEGRATION-01 — differential VPS result

**State: ESEGUITO; validation NOT achieved.**

Activity: generic heading-aware retrieval and generation, without the benchmark-specific `--targeted-coverage` flag.

Script: `scripts/v5_heading_routing_v1.py`, `scripts/smoke_test_rag_v5_e2e.py`, `scripts/run_rag_v5_locked_candidate_v2.py`. Implementation commits: 0476123, 52499ca, d69d4b7, 8392e6c.

Report: VPS `evaluation/v5_heading_routing_generic_fresh03_v1.json`, supplied by operator and reviewed 2026-10-24.

Result: one `fresh_03` generation, `heading_routing_enabled=true`, `targeted_coverage_enabled=false`, `retrieval_only=false`, elapsed 148.3s; eight evidence chunks, zero invalid citation IDs, Chroma 5319 before/after and `index_unchanged=true`. No retrieved evidence belongs to `FOOTBALL_DATA_LAB_Transizioni_Offensive_e_Difensive_Manuale`; none of the four module headings (4-3-3, 4-4-2, 3-5-2, 3-4-2-1) is in top8. The answer emphasizes contextual adaptation but does not explicitly separate descriptive statements from comparative causal proof and does not enumerate the four formations. Unlike the prior scoped VALIDATO run, generic retrieval does not reserve the relevant source passages.

Decision: **ESEGUITO**, not VALIDATO, INTEGRATO or CERTIFICATO. Keep PR #2 draft and official benchmark 5/10 unchanged. A further run is allowed only after documenting and implementing a technical change to source selection and top8 promotion. Do not rerun the same candidate.

Diagnosis from code: `expand()` gathers heading candidates but the generic path still applies the global reranker and top8 without reserved slots for matched heading evidence; if there are more than eight candidate headings per source and no explicit formation in the question, it skips the source entirely. Need source-aware and query-relevance-controlled heading selection, not hardcoded benchmark IDs or gold formations.
