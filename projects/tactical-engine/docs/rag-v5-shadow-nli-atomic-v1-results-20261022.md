# Atomic V1 — results and next gate (2026-10-22)

Result supplied from VPS: 13/15 (86.7%), 0 inference errors, shadow only.

| Case | Expected | Actual | Interpretation |
|---|---|---|---|
| low_block_reverse | contradicted | supported | Reversed tactical preference between width and vertical play; semantic comparison failure |
| methodist_every | insufficient | contradicted | Unsupported universal generalized from three systems; absence of proof confused with refutation |

All other 13 cases passed, including offside_universal and jolly_official (both insufficient), and vertical_always (contradicted).

Previous adversarial V2: 9/11; V3: 7/11. Do **not** interpret the increase to 13/15 as model improvement: the cases differ, and V2 itself was unchanged. Atomic V1 diagnoses failure modes but cannot establish production accuracy.

Decision: keep V2 shadow baseline; reject V3. Next reversible test: targeted contrastive controls with same evidence, varying only comparative wording and universal quantifiers, to determine stability of the two failures. No changes to RAG V5, Chroma or canonical NLI V2.

Provenance: user-provided `rag_v5_shadow_atomic_v1_20261022.json`, original source PDFs Bonacini, Pane and Tesser checked separately.
