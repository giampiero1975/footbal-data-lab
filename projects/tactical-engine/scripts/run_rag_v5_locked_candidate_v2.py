#!/usr/bin/env python3
"""Read-only V5 locked-candidate execution with internal evidence-based assessment."""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SHA256 = "c160a8a2128e05eda50842230c5f4aad2bf9a8085f4240c8ee893ed2e3a3fa71"
DEFAULT_MANIFEST = ROOT / "evaluation/rag_v5_independent_candidate_v2.json"
DEFAULT_OUTPUT = ROOT / "evaluation/rag_v5_candidate_v2_runtime_report.json"

def select_runtime():
    """Use an existing interpreter with V5 deps; never install or mutate envs."""
    check = ("import chromadb; "
             "from llama_index.embeddings.ollama import OllamaEmbedding; "
             "from sentence_transformers import CrossEncoder")
    candidates = [Path(sys.executable)]
    # Validated on VPS (docs/todo.md): tactical-engine/.venv imports all V5 modules.
    candidates.insert(0, ROOT / '.venv/bin/python')
    candidates.insert(1, Path("/opt/football-data-lab/projects/tactical-engine/.venv/bin/python"))
    for root in (ROOT, ROOT.parent.parent):
        candidates.extend(sorted(root.glob('.venv*/bin/python')))
        candidates.extend(sorted(root.glob('venv*/bin/python')))
    seen = set()
    for py in candidates:
        key = str(py.absolute())
        if key in seen or not py.exists():
            continue
        seen.add(key)
        result = subprocess.run([str(py), '-c', check], capture_output=True, text=True)
        if result.returncode == 0:
            if key != str(Path(sys.executable).absolute()):
                print(f'V5_RUNTIME {py} (switching from {sys.executable})', flush=True)
                os.execv(str(py), [str(py), *sys.argv])
            print(f'V5_RUNTIME {sys.executable}', flush=True)
            return
    raise SystemExit("NO_V5_RUNTIME: no interpreter passed actual imports for chromadb, OllamaEmbedding and CrossEncoder; check existing venvs; no changes made")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    p.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    p.add_argument("--execute", action="store_true")
    p.add_argument("--source-aware", action="store_true", help="Opt-in author-filtered retrieval")
    p.add_argument("--exercise-candidate", action="store_true", help="Opt-in isolated Ussia exercise candidate")
    p.add_argument("--priority-exact", action="store_true", help="Opt-in exact reference priority; default unchanged")
    p.add_argument("--targeted-coverage",action="store_true",help="Opt-in two-case diagnostic; default unchanged")
    p.add_argument("--heading-routing",action="store_true",help="Opt-in generic heading metadata routing; default unchanged")
    p.add_argument("--source-ranking-trace",action="store_true",help="Record source semantic scores; requires heading routing and retrieval-only")
    p.add_argument("--retrieval-only",action="store_true",help="Skip generation for targeted diagnostic")
    p.add_argument("--only-ids",nargs="+",choices=[f"fresh_{i:02d}" for i in range(1,11)],help="Restrict diagnostic to specified locked cases")
    args = p.parse_args()
    data = args.manifest.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        p.error(f"Manifest hash mismatch: {digest}; expected {EXPECTED_SHA256}")
    manifest = json.loads(data)
    rows = manifest["questions"]
    if len(rows) != 10 or len({x["id"] for x in rows}) != 10:
        p.error("Exactly ten distinct questions required")
    if args.output.exists():
        p.error(f"Output exists; refusing overwrite: {args.output}")
    print(f"LOCK_OK sha256={digest} questions={len(rows)} mode=internal_evidence_assessment", flush=True)
    if not args.execute:
        print("READY: pass --execute to generate the read-only diagnostic report", flush=True)
        return
    select_runtime()
    import smoke_test_rag_v5_e2e as v5
    v5.QUESTIONS = [(x["id"], x["question"]) for x in rows if not args.only_ids or x["id"] in args.only_ids]
    # --limit refers to retrieved evidence count, not the number of questions.
    sys.argv = [v5.__file__, "--limit", "8", "--output", str(args.output)]
    if args.priority_exact:
        sys.argv.append("--priority-exact")
    if args.targeted_coverage:
        sys.argv.append("--targeted-coverage")
    if args.heading_routing:
        sys.argv.append("--heading-routing")
    if args.source_ranking_trace:
        sys.argv.append("--source-ranking-trace")
    if args.retrieval_only:
        sys.argv.append("--retrieval-only")
    if args.source_aware:
        sys.argv.append("--source-aware")
    if args.exercise_candidate:
        sys.argv.append("--exercise-candidate")
    v5.main()
    report = json.loads(args.output.read_text(encoding="utf-8"))
    expected = len(v5.QUESTIONS)
    if len(report.get("questions", [])) != expected or report.get("error") or not report.get("index_unchanged"):
        raise SystemExit("INCOMPLETE: inspect report, do not claim certification")
    print(f"V5 COMPLETE: {expected}/{expected}; retrieval_only={args.retrieval_only}; no certification", flush=True)

if __name__ == "__main__":
    main()
