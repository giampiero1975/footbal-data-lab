#!/usr/bin/env python3
"""Paired reversible Ollama ablation using frozen V5 shadow evidence.

Run with --dry-run or --execute. No Chroma access; original F labels preserved.
"""
import argparse, hashlib, json, re, time
from pathlib import Path
from urllib.request import Request, urlopen

REMOVALS = {"holdout_06": {"F2", "F6"}, "holdout_10": {"F5"}}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--shadow", type=Path, required=True)
    p.add_argument("--audit", type=Path, required=False, help="Optional local phase-audit JSON")
    p.add_argument("--output", type=Path, required=True)
    mode=p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    p.add_argument("--timeout", type=int, default=900)
    a=p.parse_args()
    if a.output.exists() or a.output.resolve()==a.shadow.resolve() or (a.audit and a.output.resolve()==a.audit.resolve()):
        p.error("Refusing overwrite")
    shadow=json.loads(a.shadow.read_text(encoding="utf-8"))
    audit=json.loads(a.audit.read_text(encoding="utf-8")) if a.audit else None
    if shadow.get("schema")!="rag_v5_quality_shadow_frozen_evidence_v1":
        p.error("Unexpected shadow schema")
    flagged={q["id"]:{e["label"] for e in q["evidence"] if e["status"].startswith("REVIEW")} for q in audit["questions"]} if audit else REMOVALS
    questions={q["id"]:q for q in shadow["questions"]}
    report={"schema":"rag_v5_phase_ablation_v1","status":"dry_run" if a.dry_run else "running",
            "source_sha256":{"shadow":sha(a.shadow),"audit":sha(a.audit) if a.audit else None},
            "model":shadow["model"],"system_prompt":shadow["system_prompt"],
            "policy":"Frozen passages; unchanged F labels; no Chroma or production changes",
            "questions":[]}
    for qid,removed in REMOVALS.items():
        q=questions[qid]
        if not removed <= flagged[qid]:raise RuntimeError("Unflagged removal: "+qid)
        kept=[e for e in q["evidence"] if e["label"] not in removed]
        if len(kept)+len(removed)!=len(q["evidence"]):raise RuntimeError("Missing label: "+qid)
        entry={"id":qid,"question":q["question"],"removed_labels":sorted(removed),
               "kept_labels":[e["label"] for e in kept],"evidence":kept,
               "original_shadow_answer":q["shadow_answer"],"original_citation_ids":q["citation_ids"]}
        if a.execute:
            start=time.monotonic()
            context="\n\n".join(f"[{e['label']}] Fonte: {e['source']} | Pagine: {e['pages']}\n{e['text']}" for e in kept)
            payload={"model":shadow["model"],"stream":False,"think":False,
                     "messages":[{"role":"system","content":shadow["system_prompt"]},
                                 {"role":"user","content":f"DOMANDA:\n{q['question']}\n\nFONTI:\n{context}"}],
                     "options":{"temperature":0,"num_ctx":8192}}
            request=Request("http://127.0.0.1:11434/api/chat",
                            data=json.dumps(payload,ensure_ascii=False).encode(),
                            headers={"Content-Type":"application/json"},method="POST")
            try:
                with urlopen(request,timeout=a.timeout) as response: raw=json.load(response)
                answer=(raw.get("message") or {}).get("content","")
                if not answer.strip():raise RuntimeError("Empty response")
                cited=sorted(set(re.findall(r"\[F(\d+)\]",answer)),key=int)
                allowed={e["label"][1:] for e in kept}
                entry.update({"ablation_answer":answer,"citation_ids":cited,
                              "invalid_or_removed_citation_ids":[c for c in cited if c not in allowed],
                              "elapsed_seconds":round(time.monotonic()-start,2)})
            except Exception as exc:
                entry["error"]=f"{type(exc).__name__}: {exc}"
                report["status"]="partial_error"
                report["questions"].append(entry)
                break
        report["questions"].append(entry)
    if a.execute and report["status"]=="running":report["status"]="complete"
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open("x",encoding="utf-8") as file:
        json.dump(report,file,ensure_ascii=False,indent=2);file.write("\n")
    print("REPORT",a.output,"STATUS",report["status"])
    if report["status"]=="partial_error":raise SystemExit(1)

if __name__=="__main__":main()
