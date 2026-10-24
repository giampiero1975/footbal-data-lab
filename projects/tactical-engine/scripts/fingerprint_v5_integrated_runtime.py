#!/usr/bin/env python3
"""Create a non-secret, read-only fingerprint for the integrated V5 runtime."""
import argparse
import hashlib
from importlib import metadata
import json
import platform
from pathlib import Path
import subprocess
import sys

import chromadb

ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]
DB=REPO/"knowledge/rag/chroma"
FILES=[
    "scripts/run_rag_v5_locked_candidate_v2.py",
    "scripts/smoke_test_rag_v5_e2e.py",
    "scripts/v5_targeted_coverage_v1.py",
    "scripts/v5_heading_routing_v1.py",
    "scripts/v5_heading_reservation_v2.py",
    "scripts/v5_source_semantic_rank_v3.py",
    "scripts/v5_source_hybrid_rank_v4.py",
    "evaluation/rag_v5_independent_candidate_v2.json",
]
PACKAGES=("chromadb","llama-index-embeddings-ollama","sentence-transformers","torch")
COLLECTIONS=("dribbling_tactics_v5_multisource","dribbling_tactics_v5_exercise_candidate_v1")

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(*args):
    return subprocess.run(args,cwd=REPO,text=True,capture_output=True,check=True).stdout.strip()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("output",type=Path)
    args=parser.parse_args()
    client=chromadb.PersistentClient(path=str(DB))
    collections={}
    for name in COLLECTIONS:
        col=client.get_collection(name)
        collections[name]={"count":col.count(),"metadata":col.metadata,
                           "configuration":getattr(col,"configuration_json",None)}
    files={name:sha(ROOT/name) for name in FILES}
    packages={name:metadata.version(name) for name in PACKAGES}
    report={
        "git":{"commit":run("git","rev-parse","HEAD"),
               "branch":run("git","branch","--show-current"),
               "tracked_clean":subprocess.run(["git","diff","--quiet"],cwd=REPO).returncode==0},
        "runtime":{"python":sys.version,"executable":sys.executable,"platform":platform.platform(),
                   "packages":packages},
        "ollama":{"version":run("ollama","--version"),"models":run("ollama","list").splitlines()},
        "files":files,
        "collections":collections,
        "invariants":{"main_count":5319,"exercise_count":34,"index_writes":False},
    }
    if collections[COLLECTIONS[0]]["count"]!=5319 or collections[COLLECTIONS[1]]["count"]!=34:
        raise RuntimeError("collection count invariant failed")
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str),encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2,default=str))

if __name__=="__main__":
    main()
