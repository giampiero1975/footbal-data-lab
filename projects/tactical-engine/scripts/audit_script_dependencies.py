#!/usr/bin/env python3
"""Static inventory of tactical-engine scripts; no imports/execution of target scripts.

Run from any cwd; outputs JSON to stdout. Uses only Python standard library.
The graph is syntactic and cannot prove that scripts are active in systemd/cron.
"""
from __future__ import annotations

import ast
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
MODEL_TOKENS = (
    "qwen3-embedding", "nomic-embed-text", "qwen3.5", "qwen3:4b",
    "BAAI/bge-reranker", "cross-encoder/mmarco",
)
COLLECTION_PATTERN = re.compile(r"dribbling_tactics_[a-zA-Z0-9_]+")

OPERATIONAL_CORE = {
    "run_rag_v5_locked_candidate_v2.py",
    "smoke_test_rag_v5_e2e.py",
    "v5_heading_reservation_v2.py",
    "v5_heading_routing_v1.py",
    "v5_source_hybrid_rank_v4.py",
    "v5_source_semantic_rank_v3.py",
    "v5_targeted_coverage_v1.py",
}


def classify(name: str) -> tuple[str, str]:
    """Return lifecycle class and repository action; never declares deletion."""
    if name in OPERATIONAL_CORE:
        return "operational_core", "keep"
    if name in {
        "fingerprint_v5_integrated_runtime.py",
        "compare_v4_v5_locked_source_coverage.py",
        "audit_script_dependencies.py",
        "inventory_runtime_evidence.py",
    }:
        return "maintenance_and_freeze", "keep"
    if name.startswith(("build_rag_index", "ingest_", "extract_figures")):
        return "ingestion_or_index_builder", "keep_guarded"
    if name.startswith(("test_", "smoke_test_")):
        return "test_or_regression", "keep"
    if name.startswith(("benchmark_", "compare_", "confronta_", "ablazione_")):
        return "benchmark_or_experiment", "archive_in_place"
    if "gemini" in name:
        return "external_review_optional", "archive_in_place"
    if name.startswith("run_rag_v5_") or (
        (name.startswith("rag_v5_") or name.startswith("v5_"))
        and "shadow" in name
    ):
        return "historical_rag_runner", "archive_in_place"
    if name.startswith((
        "audit_", "diagnose_", "diagnosi_", "diagnostica_", "inspect_",
        "probe_", "trace_", "verifica_", "validate_", "evaluate_",
    )):
        return "diagnostic_or_validator", "archive_in_place"
    if name in {"ask_dribbling.py", "prova_risposta_dribbling.py", "valida_bge.py"}:
        return "legacy_entrypoint_or_probe", "archive_in_place"
    if name.startswith((
        "build_", "confronto_", "extract_exercise_", "gate_", "judge_",
        "link_", "lint_", "list_", "pilot_", "prepara_", "prepare_",
        "propose_", "shadow_", "simulate_", "smoke_ragas_", "valutazione_",
        "verify_",
    )):
        return "historical_support_tool", "archive_in_place"
    return "support_or_unclassified", "review"


def scan(path: Path):
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    imports, references, calls, writes = set(), set(), set(), []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)
        elif isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute):
                calls.add(func.attr)
                if func.attr in {"write_text", "write_bytes", "unlink", "mkdir", "add", "upsert", "delete", "create_collection", "get_or_create_collection", "to_json", "save"}:
                    writes.append({"line": node.lineno, "call": func.attr})
            elif isinstance(func, ast.Name):
                calls.add(func.id)
                if func.id in {"open"}:
                    writes.append({"line": node.lineno, "call": "open (mode requires review)"})
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            value = node.value
            for name in MODEL_TOKENS:
                if name in value:
                    references.add(name)
    lifecycle_class, repository_action = classify(path.name)
    return {
        "script": path.name,
        "lifecycle_class": lifecycle_class,
        "repository_action": repository_action,
        "imports": sorted(imports),
        "model_mentions": sorted(references),
        "collection_mentions": sorted(set(COLLECTION_PATTERN.findall(source))),
        "possible_mutations": writes,
        "uses_private_llamaindex_api": any(
            attr in source for attr in (
                "._create_citation_nodes", "._response_synthesizer",
                "._make_compact_text_chunks", "._prompt_helper"
            )
        ),
        "syntax_valid": True,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    results, failures = [], []
    for path in sorted(ROOT.glob("*.py")):
        try:
            results.append(scan(path))
        except (SyntaxError, UnicodeError) as exc:
            failures.append({"script": path.name, "error": str(exc)})
    local = {p.stem: p.name for p in ROOT.glob("*.py")}
    imported_by = defaultdict(list)
    for item in results:
        for name in item["imports"]:
            root_name = name.split(".")[0]
            if root_name in local and local[root_name] != item["script"]:
                imported_by[local[root_name]].append(item["script"])
        item["local_imports"] = sorted(
            local[name.split(".")[0]] for name in item["imports"]
            if name.split(".")[0] in local and local[name.split(".")[0]] != item["script"]
        )
    for item in results:
        item["imported_by_scripts"] = sorted(imported_by[item["script"]])
    category_counts = defaultdict(int)
    action_counts = defaultdict(int)
    for item in results:
        category_counts[item["lifecycle_class"]] += 1
        action_counts[item["repository_action"]] += 1
    report = {
        "audit": "STATIC-SCRIPT-INVENTORY",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "script_count": len(results),
        "category_counts": dict(sorted(category_counts.items())),
        "action_counts": dict(sorted(action_counts.items())),
        "syntax_failures": failures,
        "scripts": results,
        "limitations": [
            "AST-only: dynamic imports, shell references, service calls and external dependents not detected",
            "Possible mutations are syntactic warnings, not proof of execution or destructive behavior",
            "Archive-in-place preserves imports and documentation links; it is not physical relocation",
            "No script is classified for deletion because scripts occupy little space and preserve reproducibility",
        ],
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
