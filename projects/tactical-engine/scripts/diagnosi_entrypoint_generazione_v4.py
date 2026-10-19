#!/usr/bin/env python3
"""Diagnostica read-only del generatore RAG presente sulla VPS.

Cerca entrypoint e parametri effettivi senza leggere segreti, .env o file
di configurazione sensibili. Non invoca il modello e non cambia file.
"""
import ast
from pathlib import Path

ROOT=Path("/opt/football-data-lab")
BASE=ROOT/"projects/tactical-engine"
TOKENS=("ollama","qwen","chat(","generate(","system_prompt","temperature","num_predict","num_ctx")
SKIP={".git",".venv","venv","node_modules","__pycache__",".pytest_cache","dist","build"}
MAX_FILES=1500

def main():
    scanned=0
    matches=[]
    for p in BASE.rglob("*.py"):
        if any(part in SKIP for part in p.relative_to(BASE).parts):
            continue
        scanned+=1
        if scanned>MAX_FILES:
            print("Limite scansione raggiunto",flush=True)
            break
        try:
            content=p.read_text(encoding="utf-8")
        except (OSError,UnicodeError):
            continue
        hits=[]
        for lineno,line in enumerate(content.splitlines(),1):
            stripped=line.strip()
            if any(token in stripped.casefold() for token in TOKENS):
                # Mostra solo numero e tipo di istruzione, non contenuti
                hits.append(lineno)
        if hits:
            try:
                tree=ast.parse(content)
                funcs=[node.name for node in ast.walk(tree)
                       if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef))]
            except SyntaxError:
                funcs=[]
            matches.append((str(p.relative_to(ROOT)),hits[:30],funcs[:30]))
    print(f"Python analizzati: {scanned}; file candidati: {len(matches)}",flush=True)
    for name,lines,funcs in matches[:80]:
        print(f"FILE {name} linee={lines} funzioni={funcs}",flush=True)
    print("FINE: nessuna modifica e nessun segreto stampato.",flush=True)

if __name__=="__main__":
    main()
