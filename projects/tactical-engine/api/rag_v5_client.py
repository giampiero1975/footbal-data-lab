#!/usr/bin/env python3
"""Small stdlib client for the authenticated V5 job API."""
from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.request


class RagApiClient:
    def __init__(self, base_url: str, token: str, timeout: float = 10):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout

    def request(self, method: str, path: str, payload: dict | None = None) -> dict:
        body = None if payload is None else json.dumps(payload).encode()
        headers = {"Authorization": f"Bearer {self.token}", "Accept": "application/json"}
        if body is not None:
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(self.base_url + path, data=body, headers=headers, method=method)
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            return json.load(response)

    def submit(self, question: str) -> str:
        return self.request("POST", "/v1/query", {"question": question})["id"]

    def job(self, job_id: str) -> dict:
        return self.request("GET", f"/v1/jobs/{job_id}")

    def wait(self, job_id: str, deadline_seconds: int = 1200, interval: float = 2) -> dict:
        deadline = time.monotonic() + deadline_seconds
        while time.monotonic() < deadline:
            job = self.job(job_id)
            if job["status"] in {"succeeded", "failed", "timed_out"}:
                return job
            time.sleep(interval)
        raise TimeoutError("client deadline exceeded")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    parser.add_argument("--url", default=os.getenv("RAG_API_URL", "http://127.0.0.1:8088"))
    parser.add_argument("--token", default=os.getenv("RAG_API_TOKEN"))
    args = parser.parse_args()
    if not args.token:
        parser.error("RAG_API_TOKEN or --token is required")
    client = RagApiClient(args.url, args.token)
    result = client.wait(client.submit(args.question))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] != "succeeded":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
