#!/usr/bin/env python3
"""Experimental native Ollama adapter for Ragas 0.4.3 Faithfulness.

References:
https://docs.ragas.io/en/v0.4.3/howtos/migrations/migrate_from_v03_to_v04/
https://docs.ollama.com/api/chat
Uses installed InstructorBaseRagasLLM contract; no production modifications.
"""
from __future__ import annotations
import argparse
import asyncio
import json
import time
import urllib.request
from pathlib import Path
from ragas.llms import InstructorBaseRagasLLM
from ragas.metrics.collections import Faithfulness

class NativeOllamaRagasLLM(InstructorBaseRagasLLM):
    def __init__(self, model: str, url: str, timeout: int, max_tokens: int):
        self.model = model
        self.url = url.rstrip("/") + "/api/chat"
        self.timeout = timeout
        self.max_tokens = max_tokens

    def generate(self, prompt: str, response_model):
        schema = response_model.model_json_schema()
        payload = {
            "model": self.model, "stream": False, "think": False,
            "format": schema,
            "options": {"temperature": 0, "num_predict": self.max_tokens,
                        "num_ctx": 4096},
            "messages": [
                {"role": "system", "content": "Rispondi esclusivamente con JSON conforme allo schema richiesto. Non aggiungere testo esterno."},
                {"role": "user", "content": prompt}
            ],
        }
        request = urllib.request.Request(
            self.url, data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            result = json.load(response)
        message = result.get("message") or {}
        content = message.get("content") or ""
        if result.get("done_reason") != "stop" or not content:
            raise RuntimeError("Ollama incomplete output: done_reason=%r, content_length=%d, eval_count=%r" %
                               (result.get("done_reason"), len(content), result.get("eval_count")))
        return response_model.model_validate_json(content)

    async def agenerate(self, prompt: str, response_model):
        return await asyncio.to_thread(self.generate, prompt, response_model)

async def run(args):
    metric = Faithfulness(llm=NativeOllamaRagasLLM(args.model, args.ollama_url,
                                                  args.timeout, args.max_tokens))
    cases = [
        {"id": "supported",
         "user_input": "Quale condizione favorisce la profondità?",
         "response": "Lo spazio dietro la linea difensiva favorisce la ricerca della profondità.",
         "retrieved_contexts": ["Se vi è spazio alle spalle della difesa avversaria, è possibile ricercare la profondità."]},
        {"id": "unsupported",
         "user_input": "Quale condizione favorisce la profondità?",
         "response": "Una difesa bassa lascia sempre ampio spazio alle proprie spalle.",
         "retrieved_contexts": ["Se la squadra avversaria difende vicino alla propria area, la profondità è difficile da attaccare e si preferisce l'ampiezza."]}
    ]
    report = {"test": "ragas_043_faithfulness_native_ollama_smoke",
              "model": args.model, "adapter": "NativeOllamaRagasLLM",
              "notes": ["Ragas official Faithfulness; custom native Ollama transport.",
                        "Synthetic smoke test only; scores do not establish judge accuracy.",
                        "No Chroma, model or production modifications."],
              "results": []}
    for case in cases:
        started = time.monotonic()
        row = {"id": case["id"]}
        try:
            value = await metric.ascore(user_input=case["user_input"],
                                        response=case["response"],
                                        retrieved_contexts=case["retrieved_contexts"])
            row["score"] = getattr(value, "value", None)
            row["result_repr"] = str(value)[:1200]
        except Exception as exc:
            row["error"] = type(exc).__name__ + ": " + str(exc)[:1500]
        row["elapsed_seconds"] = round(time.monotonic() - started, 2)
        report["results"].append(row)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(row, ensure_ascii=False), flush=True)
        if "error" in row:
            break
    print("REPORT", args.output, flush=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default="qwen3.5:9b")
    parser.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--max-tokens", type=int, default=1024)
    args = parser.parse_args()
    asyncio.run(run(args))

if __name__ == "__main__":
    main()
