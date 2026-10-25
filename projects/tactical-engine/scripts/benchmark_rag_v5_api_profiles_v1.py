#!/usr/bin/env python3
"""Sequential application benchmark for short, medium and complex RAG questions."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import time
from urllib.request import Request, urlopen

CASES = [
    ("short", "Quali sono i principi essenziali della marcatura preventiva?"),
    ("medium", "Come organizzi pressing, coperture e distanze in un 4-3-3 contro la costruzione di un 4-2-3-1?"),
    ("complex", "Contro una pressione a uomo alta, la mia squadra costruisce 4-2-3-1 e perde palla centralmente. Senza sostituzioni: 1) modifica struttura e rotazioni per creare un uomo libero; 2) organizza la protezione preventiva e la reazione immediata alla perdita evitando campo aperto."),
]


def call(base: str, token: str, method: str, path: str, payload=None, timeout=20):
    body = None if payload is None else json.dumps(payload).encode()
    request = Request(base + path, data=body, method=method,
                      headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urlopen(request, timeout=timeout) as response:
        return json.load(response)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8088")
    parser.add_argument("--token", default=os.getenv("RAG_API_TOKEN"))
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--poll-seconds", type=float, default=2)
    parser.add_argument("--timeout", type=int, default=900)
    args = parser.parse_args()
    if not args.token:
        parser.error("RAG_API_TOKEN or --token is required")
    if args.output.exists():
        parser.error(f"output exists; refusing overwrite: {args.output}")

    report = {"schema": "rag_v5_api_profiles_v1", "cases": []}
    for profile, question in CASES:
        started = time.monotonic()
        job = call(args.url, args.token, "POST", "/v1/query", {"question": question})
        deadline = started + args.timeout
        while time.monotonic() < deadline:
            current = call(args.url, args.token, "GET", f"/v1/jobs/{job['id']}")
            if current["status"] in {"failed", "timed_out"}:
                raise RuntimeError(f"{profile}: {current.get('error', current['status'])}")
            if current["status"] == "succeeded":
                item = current["result"]["questions"][0]
                generation = item.get("generation", {})
                report["cases"].append({
                    "profile": profile, "question": question, "question_chars": len(question),
                    "wall_seconds": round(time.monotonic() - started, 2),
                    "pipeline_seconds": item.get("elapsed_seconds"), "generation": generation,
                    "evidence_count": len(item.get("evidence", [])),
                    "citation_count": len(item.get("citation_ids", [])),
                    "invalid_citations": item.get("invalid_citation_ids", []),
                    "index_unchanged": current["result"].get("index_unchanged"),
                    "answer": item.get("answer", ""),
                })
                print(f"{profile}: {report['cases'][-1]['wall_seconds']}s", flush=True)
                break
            time.sleep(args.poll_seconds)
        else:
            raise TimeoutError(f"{profile}: benchmark timeout")
    report["all_succeeded"] = len(report["cases"]) == len(CASES)
    report["all_stopped"] = all(x["generation"].get("done_reason") == "stop" for x in report["cases"])
    report["all_citations_valid"] = all(not x["invalid_citations"] and x["citation_count"] for x in report["cases"])
    report["index_unchanged"] = all(x["index_unchanged"] for x in report["cases"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if not all((report["all_succeeded"], report["all_stopped"], report["all_citations_valid"], report["index_unchanged"])):
        raise SystemExit("BENCHMARK_FAILED")
    print("BENCHMARK_COMPLETE", flush=True)


if __name__ == "__main__":
    main()
