# Shadow NLI V2 vs experimental V3 — 2026-10-22

Evidence: user-provided `rag_v5_shadow_adversarial_20261022.json` (V2) and `rag_v5_shadow_adversarial_v3_20261022.json` (V3). Both used the same 11 curated cases and model qwen3.5:9b; only the instruction changed.

| Version | Matches expected | Mismatches | Inference errors |
|---|---:|---:|---:|
| V2 | 9/11 | 2 | 0 |
| V3 | 7/11 | 4 | 0 |

V3 mismatches: `low_block_wrong` expected contradicted, got supported (V2 insufficient); `offside_always` expected insufficient, got contradicted (V2 correct); `all_systems` expected insufficient, got contradicted (same as V2); `jolly_match` expected insufficient, got contradicted (V2 correct). No mismatches were resolved by V3.

**Decision:** reject experimental V3; retain V2 as shadow reference. Do not change canonical V2, production RAG, or Chroma. These curated expected labels are review hypotheses, not population accuracy estimates.

Next investigation: inspect full cited excerpts and manually adjudicate borderline expectations; then evaluate more granular atomic claims and additional held-out counterexamples, avoiding prompt overfitting to eleven cases.
