#!/usr/bin/env python3
"""Static inventory of tactical-engine scripts; no imports/execution of target scripts.

Run from any cwd; outputs JSON to stdout. Uses only Python standard library.
The graph is syntactic and cannot prove that scripts are active in systemd/cron.
"""
from __future__ import annotations

import ast
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
    return {
        "script": path.name,
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
    print(json.dumps({
        "audit": "STATIC-SCRIPT-INVENTORY",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "script_count": len(results),
        "syntax_failures": failures,
        "scripts": results,
        "limitations": [
            "AST-only: dynamic imports, shell references, service calls and external dependents not detected",
            "Possible mutations are syntactic warnings, not proof of execution or destructive behavior",
            "No script classified as removable without VPS process, cron, systemd and dependency checks",
        ],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
