#!/usr/bin/env python3
"""Ragas H07 integration test: OpenAI-compatible Ollama with per-request think=false.
No changes to Ollama global settings, Chroma, gold, or existing benchmark.
Official refs: https://docs.ollama.com/api/openai-compatibility
https://docs.ollama.com/capabilities/thinking
https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/general_purpose/
"""
import asyncio, json, sys, time, traceback
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from benchmark_holdout_glerean_v4 import TESTS

async def main():
    import httpx, ragas, openai
    from openai import AsyncOpenAI
    from ragas.llms import llm_factory
    from ragas.metrics import DiscreteMetric
    output = ROOT / "diagnostica_ragas_no_think_h07_v1.json"
    if output.exists():
        raise FileExistsError(f"Non sovrascrivo: {output}")
    class NoThinkTransport(httpx.AsyncBaseTransport):
        def __init__(self):
            self.inner = httpx.AsyncHTTPTransport()
            self.request_seen = False
            self.response_finishes = []
        async def handle_async_request(self, request):
            if request.url.path.endswith("/chat/completions"):
                payload = json.loads(request.content)
                payload["think"] = False
                # Ollama OpenAI-compatible API: forwarding extra field is an
                # experimental capability, validated only by returned response.
                encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
                headers = dict(request.headers)
                headers.pop("content-length", None)
                request = httpx.Request(request.method, request.url, headers=headers, content=encoded)
                self.request_seen = True
            response = await self.inner.handle_async_request(request)
            return response
        async def aclose(self):
            await self.inner.aclose()
    transport = NoThinkTransport()
    async with httpx.AsyncClient(transport=transport, timeout=600) as http:
        client = AsyncOpenAI(api_key="ollama", base_url="http://127.0.0.1:11434/v1", http_client=http, max_retries=0)
        llm = llm_factory("qwen3.5:9b", client=client)
        gold = json.loads((ROOT / "evaluation/gold_glerean_principi_v1.json").read_text(encoding="utf-8"))
        claims = {c["id"]: c for case in gold["cases"] for c in case["gold_claims"]}
        case = next(t for t in TESTS if t["id"] == "H07")
        coverage = DiscreteMetric(
            name="tactical_coverage", allowed_values=["completo", "parziale"],
            prompt=("Valuta SOLO la copertura dei nuclei semantici presenti nella FONTE. "
                    "Completo se tutti i nuclei (ruoli, azioni, condizioni essenziali) "
                    "sono trattati anche con parafrasi, indipendentemente dalla loro "
                    "correttezza; parziale se almeno un nucleo essenziale e' assente. "
                    "Non richiedere ripetizioni letterali.\nFONTE: {reference}\nFRASE: {response}"))
        report = {"schema_version": 1, "purpose": "ragas_no_think_integration_h07",
                  "ragas_version": getattr(ragas, "__version__", "unknown"),
                  "openai_version": getattr(openai, "__version__", "unknown"),
                  "model": "qwen3.5:9b", "case": "H07",
                  "expected": case["expected_coverage"], "think_requested": False,
                  "limitations": ["Single synthetic case; custom DiscreteMetric, not standard Ragas Faithfulness",
                                  "OpenAI-compatible forwarding of think is experimental"]}
        start = time.monotonic()
        try:
            result = await coverage.ascore(reference=claims[case["claim"]]["evidence"],
                                           response=case["statement"], llm=llm)
            report.update(status="ok", predicted=str(result.value),
                          match=str(result.value) == case["expected_coverage"])
            print(f"RAGAS_NO_THINK_OK value={result.value} expected={case['expected_coverage']}", flush=True)
        except Exception as exc:
            details = {"type": type(exc).__name__, "message": str(exc),
                       "traceback": "".join(traceback.format_exception(exc))}
            completion = getattr(exc, "last_completion", None)
            if completion is not None:
                details["last_completion"] = completion.model_dump(mode="json", exclude_none=True)
            report.update(status="error", exception=details)
            print(f"RAGAS_NO_THINK_ERROR {type(exc).__name__}: {exc}", flush=True)
        finally:
            report["request_intercepted"] = transport.request_seen
            report["elapsed_seconds"] = round(time.monotonic()-start, 2)
            output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
            print(f"REPORT {output}", flush=True)
if __name__ == "__main__":
    asyncio.run(main())
