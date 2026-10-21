#!/usr/bin/env python3
"""Evaluate claim-to-evidence fidelity against a manually labeled gold set.

Ollama API: POST /api/chat with format JSON schema and stream=false.
Read-only: no Chroma, embeddings or production prompt changes.
"""
from __future__ import annotations
import argparse
import json
import time
import urllib.request
from collections import Counter
from pathlib import Path

LABELS = ("supported", "contradicted", "insufficient")
SCHEMA = {
    "type": "object",
    "properties": {
        "label": {"type": "string", "enum": list(LABELS)},
        "reason": {"type": "string"}
    },
    "required": ["label", "reason"],
    "additionalProperties": False
}
SYSTEM = (
    "Valuta SOLO se la singola affermazione è sostenuta dal testo della fonte. "
    "supported: il testo implica l'affermazione. "
    "contradicted: il testo afferma il contrario. "
    "insufficient: il testo non consente di stabilirla, anche se plausibile. "
    "Non usare conoscenze esterne. Mantieni condizioni, negazioni, quantificatori "
    "e distinzione tra caratteristiche statiche ed effetti di un cambiamento. "
    "Rispondi esclusivamente nel formato JSON richiesto."
)

def predict(case, model, url, timeout):
    prompt = "FONTE:\n" + case["evidence"] + "\n\nAFFERMAZIONE:\n" + case["claim"]
    body = json.dumps({
        "model": model,
        "stream": False,
        "think": False,
        "format": SCHEMA,
        "options": {"temperature": 0, "num_ctx": 4096},
        "messages": [{"role": "system", "content": SYSTEM},
                     {"role": "user", "content": prompt}]
    }).encode("utf-8")
    request = urllib.request.Request(url.rstrip("/") + "/api/chat", data=body,
                                     headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        result = json.load(response)
    obj = json.loads(result["message"]["content"])
    if obj.get("label") not in LABELS:
        raise ValueError("Unexpected label: " + repr(obj))
    return {"label": obj["label"], "reason": str(obj.get("reason", "")),
            "total_duration_ns": result.get("total_duration"),
            "eval_count": result.get("eval_count")}

def metrics(rows):
    valid = [r for r in rows if "prediction" in r]
    matrix = {g: {p: 0 for p in LABELS} for g in LABELS}
    for r in valid:
        matrix[r["gold"]][r["prediction"]["label"]] += 1
    scores = {}
    for label in LABELS:
        tp = matrix[label][label]
        fp = sum(matrix[g][label] for g in LABELS if g != label)
        fn = sum(matrix[label][p] for p in LABELS if p != label)
        precision = tp / (tp + fp) if tp + fp else 0
        recall = tp / (tp + fn) if tp + fn else 0
        scores[label] = {"precision": round(precision, 3), "recall": round(recall, 3),
                         "f1": round(2 * precision * recall / (precision + recall), 3)
                         if precision + recall else 0}
    return {"evaluated": len(valid), "correct": sum(r["gold"] == r["prediction"]["label"] for r in valid),
            "accuracy": round(sum(r["gold"] == r["prediction"]["label"] for r in valid) / len(valid), 3)
            if valid else None, "confusion_matrix": matrix, "per_label": scores}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--gold", type=Path, required=True)
    p.add_argument("--output", type=Path)
    p.add_argument("--validate-only", action="store_true")
    p.add_argument("--model", default="qwen3.5:9b")
    p.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    p.add_argument("--timeout", type=int, default=600)
    args = p.parse_args()
    dataset = json.loads(args.gold.read_text(encoding="utf-8"))
    cases = dataset["cases"]
    ids = [c["id"] for c in cases]
    if len(ids) != len(set(ids)) or not cases:
        raise ValueError("Duplicate IDs or empty dataset")
    for c in cases:
        if c.get("gold") not in LABELS or not c.get("evidence") or not c.get("claim"):
            raise ValueError("Invalid case " + str(c.get("id")))
    print("VALID GOLD:", len(cases), "cases", dict(Counter(c["gold"] for c in cases)), flush=True)
    if args.validate_only:
        return
    if not args.output:
        p.error("--output is required unless --validate-only")
    report = {"model": args.model, "gold": str(args.gold), "cases": [],
              "limitations": ["Small manually labeled dataset; not an unbiased performance estimate.",
                              "No independent human review of model rationales.",
                              "Do not deploy a judge based on this experiment alone."]}
    def save():
        report["metrics"] = metrics(report["cases"])
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for case in cases:
        row = {"id": case["id"], "gold": case["gold"], "claim": case["claim"],
               "source": case["source"], "page": case["page"]}
        report["cases"].append(row)
        try:
            start = time.monotonic()
            row["prediction"] = predict(case, args.model, args.ollama_url, args.timeout)
            row["elapsed_seconds"] = round(time.monotonic() - start, 2)
            print(case["id"], case["gold"], "=>", row["prediction"]["label"], flush=True)
        except Exception as exc:
            row["error"] = type(exc).__name__ + ": " + str(exc)
            save()
            raise
        save()
    print("METRICS", json.dumps(report["metrics"], ensure_ascii=False), flush=True)

if __name__ == "__main__":
    main()
