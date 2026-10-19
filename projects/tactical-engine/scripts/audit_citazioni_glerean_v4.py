#!/usr/bin/env python3
"""Audit offline delle citazioni: non usa LLM, Ollama, Chroma o rete.

Non confondere validita dell'ID e supporto semantico. Il secondo richiede
revisione esplicita ed e' rappresentato come 'non_verificato'.
"""
import argparse
import json
import re
from pathlib import Path

STABLE = re.compile(r"\[GLEREAN-C\d{3}\]")
NUMERIC = re.compile(r"\[(\d+)\]")
PAGE = re.compile(r"\b(?:pagina|pag\.|page)\s*\[(\d+)\]", re.I)
CITATION_LABEL = re.compile(r"\b(?:fonte|source|citazione)\s*\[(\d+)\]", re.I)

def citations(answer, mode):
    if mode == "stable":
        return STABLE.findall(answer)
    # Nella modalita numerica, escludere i riferimenti a pagina espliciti.
    pages = {(m.start(1)-1, m.end(1)+1) for m in PAGE.finditer(answer)}
    return [m.group(0) for m in NUMERIC.finditer(answer)
            if (m.start(), m.end()) not in pages]

def audit(run):
    answer=run["answer"]
    sources=run["sources"]
    allowed={s["ref"] for s in sources}
    refs=citations(answer,run["mode"])
    unknown=sorted(set(refs)-allowed)
    page_numbers=[m.group(0) for m in PAGE.finditer(answer)]
    claims=run.get("gold_claims",[])
    return {
        "case_id":run["case_id"],"mode":run["mode"],
        "citations":refs,"invalid_citations":unknown,
        "explicit_page_references":page_numbers,
        "citation_count":len(refs),
        "source_count":len(sources),
        "gold_claims":[{"id":g["id"],"claim":g["claim"],
                        "coverage":"non_verificato","semantic_support":"non_verificato"}
                       for g in claims],
        "semantic_verdict":"richiede_revisione_umano_o_valutatore_separato",
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("input",type=Path)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    data=json.loads(args.input.read_text(encoding="utf-8"))
    if len(data.get("runs",[]))!=6:
        raise ValueError("Attese sei generazioni nel benchmark")
    results=[audit(r) for r in data["runs"]]
    output=args.output or args.input.with_name(args.input.stem+"_audit.json")
    if output.exists():
        raise FileExistsError(f"File gia presente: {output}")
    output.write_text(json.dumps({
        "type":"offline_citation_audit","input":str(args.input),
        "warning":"La validita degli ID non prova la fedelta semantica",
        "results":results},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    for r in results:
        print(f'{r["case_id"]} {r["mode"]}: citazioni={r["citation_count"]}, '
              f'ID_non_validi={r["invalid_citations"]}, '
              f'claim_da_verificare={len(r["gold_claims"])}')
    print(f"REPORT: {output}")

if __name__=="__main__":
    main()
