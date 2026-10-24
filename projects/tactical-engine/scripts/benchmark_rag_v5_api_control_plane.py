#!/usr/bin/env python3
"""Concurrent load probe for health/readiness only; never submits RAG jobs."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import statistics
import time
import urllib.request


def call(url: str, token: str | None) -> tuple[int, float]:
    headers = {} if token is None else {"Authorization": f"Bearer {token}"}
    request = urllib.request.Request(url, headers=headers)
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=5) as response:
        response.read()
        return response.status, (time.perf_counter() - started) * 1000


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8088")
    parser.add_argument("--token")
    parser.add_argument("--requests", type=int, default=200)
    parser.add_argument("--concurrency", type=int, default=20)
    parser.add_argument("--output")
    args = parser.parse_args()
    if not 1 <= args.requests <= 5000 or not 1 <= args.concurrency <= 100:
        parser.error("requests/concurrency outside safe range")
    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        rows = list(pool.map(lambda _: call(args.url + "/healthz", None), range(args.requests)))
    ready = call(args.url + "/readyz", args.token) if args.token else None
    latencies = [row[1] for row in rows]
    result = {
        "requests": args.requests,
        "concurrency": args.concurrency,
        "success": sum(status == 200 for status, _ in rows),
        "latency_ms": {
            "min": min(latencies), "median": statistics.median(latencies),
            "max": max(latencies), "mean": statistics.mean(latencies),
        },
        "authenticated_ready": ready,
        "job_submissions": 0,
    }
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        from pathlib import Path
        Path(args.output).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if result["success"] != args.requests or (ready and ready[0] != 200):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
