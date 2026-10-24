# V5 heading routing integration — implementation review

**Activity:** V5-HEADING-ROUTING-INTEGRATION-01. **State: IMPLEMENTATO** (not executed/validated/integrated).

**Technical difference from completed fresh_03 shadow:** New opt-in `--heading-routing` is question-driven rather than keyed to `fresh_03`; metadata heading discovery can find manual sources beyond dense top24; generic generation guidance replaces benchmark-specific formation enumeration. The locked manifest and Chroma remain untouched by code changes. Default runner remains unchanged.

**Scripts:** `scripts/v5_heading_routing_v1.py`, `scripts/smoke_test_rag_v5_e2e.py`, `scripts/run_rag_v5_locked_candidate_v2.py`.
**Commits:** 0476123, 52499ca, d69d4b7, 8392e6c.
**Report:** This implementation review, no VPS runtime report yet.
**Result:** Source-only code review; no claim of successful runtime behavior.
**Decision:** Run one new differential validation, not the already completed targeted coverage test. First py_compile; then execute `--heading-routing --only-ids fresh_03` without `--targeted-coverage` to isolate the generic routing. Inspect evidence, citations, causal caveat, index count, and compare with the prior validated shadow. Do not rerun full locked suite yet.
**Status:** IMPLEMENTATO. No pipeline integration or certification.

Command (VPS, after synchronizing branch):
```bash
cd /opt/football-data-lab
git fetch origin
git merge --ff-only origin/codex/v5-heading-routing-integration
projects/tactical-engine/.venv/bin/python -m py_compile projects/tactical-engine/scripts/v5_heading_routing_v1.py projects/tactical-engine/scripts/smoke_test_rag_v5_e2e.py projects/tactical-engine/scripts/run_rag_v5_locked_candidate_v2.py
projects/tactical-engine/.venv/bin/python projects/tactical-engine/scripts/run_rag_v5_locked_candidate_v2.py --execute --heading-routing --only-ids fresh_03 --output projects/tactical-engine/evaluation/v5_heading_routing_generic_fresh03_v1.json
```
