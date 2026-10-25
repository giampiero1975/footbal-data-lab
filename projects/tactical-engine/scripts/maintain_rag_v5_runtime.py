#!/usr/bin/env python3
"""Fail-closed health audit and bounded retention for RAG API run artifacts."""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
JOB_RE=re.compile(r"^([0-9a-f]{32})\.(request|result)\.json$")


def cleanup_plan(directory: Path, now: float, retention_days: int, preserve_jobs: int) -> list[Path]:
    groups=defaultdict(list)
    for path in directory.iterdir() if directory.is_dir() else []:
        match=JOB_RE.match(path.name)
        if match: groups[match.group(1)].append(path)
    ordered=sorted(groups, key=lambda job:max(p.stat().st_mtime for p in groups[job]), reverse=True)
    protected=set(ordered[:preserve_jobs]); cutoff=now-retention_days*86400
    return sorted((p for job,paths in groups.items() if job not in protected for p in paths if p.stat().st_mtime<cutoff),key=str)


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix=f".{path.name}.",dir=path.parent)
    try:
        with os.fdopen(fd,"w",encoding="utf-8") as h: json.dump(payload,h,ensure_ascii=False,indent=2,sort_keys=True); h.write("\n")
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)


def api_json(url: str, token: str | None = None) -> dict:
    headers={} if token is None else {"Authorization":"Bearer "+token}
    with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=10) as response:
        return {"http":response.status,"body":json.load(response)}


def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--write",action="store_true")
    p.add_argument("--retention-days",type=int,default=30)
    p.add_argument("--preserve-jobs",type=int,default=100)
    p.add_argument("--api-runs",type=Path,default=ROOT/"evaluation/api-runs")
    p.add_argument("--report",type=Path,default=ROOT/"evaluation/api-runs/maintenance-latest.json")
    p.add_argument("--collection",default=os.getenv("RAG_COLLECTION","dribbling_tactics_v5_multisource"))
    p.add_argument("--expected-count",type=int,default=int(os.getenv("RAG_EXPECTED_COUNT","5319")))
    p.add_argument("--chroma",type=Path,default=ROOT.parent.parent/"knowledge/rag/chroma")
    a=p.parse_args()
    if min(a.retention_days,a.preserve_jobs)<1: p.error("retention limits must be positive")
    token=os.getenv("RAG_API_TOKEN",""); port=os.getenv("RAG_API_PORT","8088"); base=f"http://127.0.0.1:{port}"
    errors=[]; checks={}
    try: checks["health"]=api_json(base+"/healthz")
    except Exception as exc: errors.append(f"health: {type(exc).__name__}: {exc}")
    try: checks["ready"]=api_json(base+"/readyz",token)
    except Exception as exc: errors.append(f"ready: {type(exc).__name__}: {exc}")
    try: checks["metrics"]=api_json(base+"/v1/metrics",token)["body"]
    except Exception as exc: errors.append(f"metrics: {type(exc).__name__}: {exc}")
    try:
        import chromadb
        count=chromadb.PersistentClient(path=str(a.chroma)).get_collection(a.collection).count()
        checks["collection"]={"name":a.collection,"count":count,"expected":a.expected_count}
        if count!=a.expected_count: errors.append(f"collection count {count} != {a.expected_count}")
    except Exception as exc: errors.append(f"collection: {type(exc).__name__}: {exc}")
    usage=shutil.disk_usage(ROOT); used_percent=round((usage.total-usage.free)*100/usage.total,2)
    checks["disk"]={"total":usage.total,"free":usage.free,"used_percent":used_percent}
    if used_percent>=90: errors.append(f"disk critical: {used_percent}%")
    git=subprocess.run(["git","status","--porcelain","--untracked-files=no"],cwd=ROOT.parent.parent,capture_output=True,text=True)
    checks["git"]={"commit":subprocess.run(["git","rev-parse","HEAD"],cwd=ROOT.parent.parent,capture_output=True,text=True).stdout.strip(),"tracked_clean":not git.stdout.strip()}
    plan=cleanup_plan(a.api_runs,time.time(),a.retention_days,a.preserve_jobs)
    removed=[]
    if a.write and not errors:
        for path in plan: path.unlink(); removed.append(str(path))
    report={"schema":"rag_v5_runtime_maintenance_v1","observed_at":datetime.now(timezone.utc).isoformat(),"write":a.write,
            "retention_days":a.retention_days,"preserve_jobs":a.preserve_jobs,"checks":checks,"planned_removals":[str(x) for x in plan],
            "removed":removed,"errors":errors,"status":"ok" if not errors else "failed"}
    atomic_json(a.report,report); print(json.dumps(report,ensure_ascii=False,indent=2))
    return 1 if errors else 0


if __name__=="__main__": raise SystemExit(main())
