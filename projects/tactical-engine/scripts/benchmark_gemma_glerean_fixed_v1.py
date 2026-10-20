#!/usr/bin/env python3
"""Confronto Gemma su 6 contesti TOP5 congelati del benchmark V4.
Solo lettura baseline; nessuna scrittura su Chroma. Ollama API ufficiale.
https://docs.ollama.com/api/generate
"""
import argparse
import hashlib
import json
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPT = """Sei DRIBBLING, analista tattico del calcio. Rispondi in italiano solo in base alle FONTI qui sotto.
La risposta deve essere completa ma solo su principi documentati. Non aggiungere tattiche generiche.
REGOLE:
- Prima identifica tutti i principi pertinenti alla domanda presenti nelle fonti; copri ciascuno distintamente.
- Distingui compiti dei difensori, centrocampisti, attaccanti centrali e laterali; non scambiare i ruoli.
- Se la fonte distingue zone di campo, esplicita le condizioni: non confondere zona difensiva nostra e avversaria.
- Se una fonte descrive una regola generale e un'eccezione contestuale, spiega entrambe.
- Non attribuire alle figure contenuti non verificati. Non parlare di Gustinetti salvo richiesta.
- Cita soltanto gli ID tra PARENTESI QUADRE presenti nell'elenco FONTI. Non usare [11], [12], [8] se non compaiono esattamente nell'elenco.
- Una citazione va accanto all'affermazione specifica sostenuta. Non inventare fonti o pagine.
- Se un elemento non e' documentato, dichiaralo.
FONTI:
{context}

DOMANDA: {question}

RISPOSTA:"""
CIT = re.compile(r"\[(?:GLEREAN-C\d{3}|\d+)\]")

def post(endpoint, payload):
    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/" + endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST")
    with urllib.request.urlopen(req, timeout=900) as response:
        return json.load(response)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, default=ROOT / "benchmark_citazioni_stabili_v4.json")
    ap.add_argument("--output", type=Path, default=ROOT / "benchmark_gemma_glerean_fixed_v1.json")
    ap.add_argument("--model", default="gemma3:12b")
    ap.add_argument("--num-ctx", type=int, default=4096)
    ap.add_argument("--reserve", type=int, default=768)
    ap.add_argument("--run", action="store_true", help="Esegue 6 generazioni dopo la verifica token")
    args = ap.parse_args()
    if args.num_ctx <= args.reserve:
        ap.error("num-ctx deve superare reserve")
    baseline = json.loads(args.input.read_text(encoding="utf-8"))
    runs = baseline.get("runs", [])
    if len(runs) != 6:
        raise ValueError("Attese esattamente 6 esecuzioni baseline")
    if args.output.exists():
        raise FileExistsError(f"Non sovrascrivo: {args.output}")
    prompts = []
    print("VERIFICA CONTENUTI CONGELATI")
    for i, r in enumerate(runs, 1):
        sources = r["sources"]
        if len(sources) != 5:
            raise ValueError(f"Run {i}: attese 5 fonti, trovate {len(sources)}")
        refs = [s["ref"] for s in sources]
        context = "\n\n".join(
            f'FONTE {s["ref"]} (pagina {s.get("page_numbers", "?")}):\n{s["text"]}'
            for s in sources)
        prompt = PROMPT.format(context=context, question=r["question"])
        # Ollama /api/tokenize non e' API ufficiale: usa /api/generate con num_predict=0?
        # Non effettuare richieste a modello durante la fase di preflight.
        # Caratteri e parole NON sono una misura affidabile dei token.
        sha = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
        prompts.append((r, refs, prompt, sha))
        print(f'{i}. {r["case_id"]} {r["mode"]}: caratteri={len(prompt)}, sha256={sha[:16]}')
    if not args.run:
        print("PRE-FLIGHT OK: nessuna generazione eseguita. Il conteggio token esatto non e' disponibile offline.")
        print("Per eseguire dopo verifica del budget token: --run")
        return
    report = {
        "schema_version": 1,
        "method": "same_fixed_top5_context_prompt_v2",
        "baseline": str(args.input),
        "model": args.model,
        "num_ctx": args.num_ctx,
        "num_predict": args.reserve,
        "temperature": 0.1,
        "limitations": [
            "Contesti TOP5 congelati: non misura retrieval end-to-end",
            "Controllo di sintassi citazioni, non supporto semantico",
            "Token prompt misurati da prompt_eval_count restituito da Ollama dopo generazione",
            "Se il prompt supera il budget il report e' marcato non comparabile",
        ],
        "runs": [],
    }
    for i, (r, refs, prompt, sha) in enumerate(prompts, 1):
        started = time.monotonic()
        result = post("generate", {
            "model": args.model, "prompt": prompt, "stream": False,
            "options": {"temperature": 0.1, "num_ctx": args.num_ctx,
                        "num_predict": args.reserve},
            "think": False,
        })
        elapsed = round(time.monotonic() - started, 2)
        answer = result.get("response", "")
        used = CIT.findall(answer)
        invalid = sorted(set(used) - set(refs))
        prompt_tokens = result.get("prompt_eval_count")
        comparable = prompt_tokens is not None and prompt_tokens <= args.num_ctx - args.reserve
        entry = {
            "case_id": r["case_id"], "mode": r["mode"],
            "question": r["question"], "allowed_refs": refs,
            "chunk_indices": r.get("chunk_indices"),
            "source_sha256": hashlib.sha256(
                json.dumps(r["sources"], ensure_ascii=False, sort_keys=True).encode()).hexdigest(),
            "prompt_sha256": sha,
            "prompt_chars": len(prompt), "prompt_eval_count": prompt_tokens,
            "eval_count": result.get("eval_count"),
            "prompt_eval_duration_ns": result.get("prompt_eval_duration"),
            "eval_duration_ns": result.get("eval_duration"),
            "total_duration_ns": result.get("total_duration"),
            "seconds_wall": elapsed,
            "answer_raw": answer, "used_refs": used,
            "invalid_refs": invalid, "comparable_context": comparable,
            "gold_claims": r.get("gold_claims"), "sources": r["sources"],
        }
        report["runs"].append(entry)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f'{i}/6 {r["case_id"]} {r["mode"]}: {elapsed}s, prompt_tokens={prompt_tokens}, '
              f'citazioni_non_valide={invalid}, contesto_comparabile={comparable}', flush=True)
        if not comparable:
            print("STOP: possibile troncamento contesto. Non eseguire altre generazioni.")
            break
    print("REPORT", args.output)

if __name__ == "__main__":
    main()
