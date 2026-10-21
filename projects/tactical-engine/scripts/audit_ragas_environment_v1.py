#!/usr/bin/env python3
"""Read-only environment inventory for documented Ragas/Ollama compatibility.

No packages are installed, imported from ragas, or modified.
Official references:
https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/
https://docs.ragas.io/en/latest/howtos/customizations/metrics/modifying-prompts-metrics/
https://docs.ragas.io/en/latest/howtos/customizations/metrics/metrics_language_adaptation/
https://docs.ollama.com/capabilities/structured-outputs
"""
from __future__ import annotations
import argparse
import importlib.metadata
import importlib.util
import json
import os
import platform
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

PACKAGES = ("ragas", "ollama", "transformers", "torch", "sentence-transformers",
            "huggingface-hub", "pydantic", "openai", "langchain-ollama")
def package_info(name):
    try:
        dist = importlib.metadata.distribution(name)
        return {"installed": True, "version": dist.version}
    except importlib.metadata.PackageNotFoundError:
        return {"installed": False}

def ollama_info(base_url, timeout):
    result = {}
    for path in ("/api/version", "/api/tags"):
        try:
            with urllib.request.urlopen(base_url.rstrip("/") + path, timeout=timeout) as response:
                payload = json.load(response)
            if path == "/api/version":
                result["version"] = payload.get("version")
            else:
                result["models"] = [m.get("name") or m.get("model") for m in payload.get("models", [])]
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            result[path] = {"error": type(exc).__name__, "detail": str(exc)[:240]}
    return result

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    p.add_argument("--timeout", type=int, default=5)
    args = p.parse_args()
    report = {
        "method": "Read-only version and capability inventory",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python": {"executable": sys.executable, "version": sys.version.split()[0],
                   "platform": platform.platform()},
        "packages": {name: package_info(name) for name in PACKAGES},
        "ollama": ollama_info(args.ollama_url, args.timeout),
        "ragas_api": {
            "guidance": "Prefer collections API when supported by installed version; no imports executed",
            "documentation": [
                "https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/",
                "https://docs.ragas.io/en/latest/howtos/customizations/metrics/modifying-prompts-metrics/",
                "https://docs.ragas.io/en/latest/howtos/customizations/metrics/metrics_language_adaptation/"
            ]
        },
        "limitations": [
            "Version inventory does not establish API compatibility by itself.",
            "Run separately in each Python environment to distinguish installations.",
            "No model inference or package installation performed."
        ]
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("REPORT", args.output)
    print("RAGAS", report["packages"]["ragas"])
    print("OLLAMA", report["ollama"].get("version", "unavailable"))
    print("PYTHON", report["python"]["executable"])

if __name__ == "__main__":
    main()
