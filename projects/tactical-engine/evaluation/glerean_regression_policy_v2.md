# DRIBBLING — Glerean regression policy (offline)

The production Qwen V4 remains unchanged. This is a separate offline validation step for frozen benchmark reports.

Run:
```bash
python3 projects/tactical-engine/scripts/validate_glerean_report_v2.py projects/tactical-engine/benchmark_glerean_enriched_v1.json --output /tmp/glerean_lint_results_v2.json
```

The tool is read-only with respect to the benchmark and production; `--output` writes a separate audit JSON. It detects selected role contradictions and citation anomalies, **not** all semantic errors. Any finding must be checked against the original PDF.

Source facts for regression: n.7 and n.11 are wide forwards, n.6 and n.8 are midfielders, n.4 is the midfield ball carrier in Fig.20, and Fig.13 refers to movement behind the opposing **midfielder**, not defenders.

Do not use a lint PASS as a green light for production deployment. Use stable `GLEREAN-C###` citations and figure numbers as `Fig. N` in future prompts.
