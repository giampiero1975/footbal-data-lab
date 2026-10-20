# DRIBBLING — Glerean enriched benchmark audit v1

Benchmark: 12/12 runs completed, same prompt SHA per case/mode across models; 3 questions x 2 citation modes x 2 models. num_ctx=8192; num_predict=1536; temperature=0.1. All comparable_context=true (capacity check, not factual accuracy).

| Metric | Qwen 3.5 9B | Gemma 3 12B |
|---|---:|---:|
| Successful runs | 6/6 | 6/6 |
| Total wall seconds | 1219.76 | 1432.22 |
| Mean seconds | 203.29 | 238.70 |
| Generated tokens | 6827 | 4344 |
| Runs with recognized source citations | 5/6 | 6/6 |
| Runs without invalid source refs | 6/6 | 5/6 |

## Gold claims: preliminary manual content audit

S = explicitly covered; P = partial/implicit. Not a verified PDF page-by-page score.

| Claim | Qwen numeric | Qwen stable | Gemma numeric | Gemma stable |
|---|---|---|---|---|
| P1 secure possession and shielding | S | S | S | S |
| P2 teammates assist; fast attacking exception | S | S | S | S |
| P3 preset movements for space/1v1/support | P | P | P | P |
| U1 1v1 constant reference in possession | S | S | P | S |
| U2 goalkeeper long pass and flick-on | S | S | S | S |
| U3 defenders/midfield manage; forwards receive in spaces | S | S | P | S |
| V1 verticality forwards and backwards | S | S | S | S |
| V2 defenders retreat to support | S | S | S | S |
| V3 midfield waits for secure possession then short vertical runs | S | S | S | S |
| V4 wide forwards depth/width; central depth; diagonal runs | S | S | S | P |

## Confirmed answer-level defects

- Qwen possession numeric: incorrectly calls n.7 and n.11 wide midfielders; sidecar maps them as wide forwards.
- Gemma 1v1 numeric: says n.6 and n.8 run behind opposing defenders; Fig.13 describes movement behind opposing midfielder.
- Gemma possession numeric: invalid [11] reference; [3, 11, 12] mixes document source IDs and figure numbers.
- Qwen verticality numeric: no machine-recognized source refs despite Fig.20 and Fig.21 mentions.
- Qwen verticality stable: confusingly refers to a defender carrying the ball in Fig.20, which describes midfielder n.4 carrying.
- Gemma verticality stable: fails to explicitly distinguish wide forwards' depth+width from central forwards' depth.
- Possession answers occasionally introduce defensive pressing principles irrelevant to after-ball-recovery question.

## Operational findings

Gemma llama-server process was killed by Linux global OOM after 11th test (anon RSS approximately 14.5 GiB on a 15 GiB RAM VPS); resumed final test without repeating 11 saved runs. Gemma removed from Ollama at user's request. Preserve Qwen production V4 unchanged.

## Immediate development gates

1. Citation output contract: use [GLEREAN-C###] only for document sources; label figures as Fig. N without bare numeric bracket notation.
2. Deterministic tactical role/figure checks for n.7/11 forwards, n.6/8 midfielders, n.4 midfield ball carrier, Fig.13 opposing midfielder.
3. Validate citations against retrieved chunks and source page labels before user-facing answer.
4. Test changes on frozen cases and separate holdout; no V4 replacement without improvement.

Evidence: completed `benchmark_glerean_enriched_v1.json` provided in conversation; figure audit `evaluation/audit_figure_glerean_v1.md`. This audit is preliminary and does not replace PDF-by-PDF source verification.
