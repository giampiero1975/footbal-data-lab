#!/usr/bin/env python3
"""Isolated, opt-in vision experiment on existing Docling PNGs via local Ollama.

Does not alter PDFs, Docling JSON, Chroma, or existing manifests.
"""
import argparse
import base64
import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/opt/football-data-lab")
PROCESSED = ROOT / "knowledge/processed"
OUTPUT = ROOT / "knowledge/experiments/vision_pilot"
PROMPT = (
    "Analizza esclusivamente il diagramma calcistico nell'immagine. "
    "Riporta solo ciò che è visibile: numeri leggibili dei giocatori, "
    "posizioni relative, frecce e loro direzione, palla e eventuali etichette. "
    "Non attribuire ruoli, intenzioni o sequenze non esplicitamente rappresentati. "
    "Se un elemento non è distinguibile, dichiaralo. Rispondi in italiano."
)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", default="formations-and-systems/334_principi_Glerean.pdf")
    p.add_argument("--figure-index", type=int, default=1)
    p.add_argument("--model", default="qwen3.5:9b")
    p.add_argument("--timeout", type=int, default=240)
    args = p.parse_args()
    if args.figure_index < 1:
        p.error("--figure-index must be >= 1")
    source = Path(args.source)
    if source.is_absolute() or ".." in source.parts or source.suffix.lower() != ".pdf":
        p.error("--source must be a relative PDF path within knowledge/sources")
    base = PROCESSED / source.parent / source.stem
    manifest = base.parent / (base.name + "_images") / "images.json"
    entries = json.loads(manifest.read_text(encoding="utf-8"))
    item = next((e for e in entries if e.get("figure_index") == args.figure_index), None)
    if item is None:
        p.error("Figure index absent from manifest")
    image_name = item["file"]
    if Path(image_name).name != image_name:
        p.error("Unsafe image filename")
    image_path = manifest.parent / image_name
    image_bytes = image_path.read_bytes()
    payload = {
        "model": args.model, "stream": False,
        "messages": [{"role": "user", "content": PROMPT,
                      "images": [base64.b64encode(image_bytes).decode("ascii")]}],
        "options": {"temperature": 0, "num_ctx": 4096, "num_predict": 700},
        "think": False,
    }
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST")
    started = time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            result = json.load(response)
    except (urllib.error.URLError, TimeoutError) as exc:
        raise SystemExit(f"Ollama request failed: {exc}")
    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "source": source.as_posix(), "figure_index": args.figure_index,
        "image": image_name, "page": item.get("page"),
        "model": args.model, "prompt": PROMPT,
        "description": result.get("message", {}).get("content", ""),
        "duration_seconds": round(time.monotonic() - started, 2),
        "eval_count": result.get("eval_count"),
        "total_duration_ns": result.get("total_duration"),
        "status": "unreviewed_model_output",
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    target = OUTPUT / f"{source.stem}_figure_{args.figure_index:03d}_{int(time.time())}.json"
    with target.open("x", encoding="utf-8") as stream:
        json.dump(record, stream, ensure_ascii=False, indent=2)
    print(json.dumps({"output": str(target), **record}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
