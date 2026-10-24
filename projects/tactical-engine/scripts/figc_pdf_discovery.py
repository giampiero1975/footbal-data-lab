#!/usr/bin/env python3
"""Bounded FIGC PDF discovery and verification; dry-run unless --write."""
from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import tempfile
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

QUERIES = [
    'site:figc.it/media/ "uefa pro" tattica filetype:pdf',
    'site:figc.it/media/ tesi (tattica OR "modello di gioco" OR "sistemi di gioco" OR modulo OR moduli) filetype:pdf',
]
DEFAULT_SEEDS = ["https://www.figc.it/category/Tesi"]
ALLOWED_HOSTS = {"figc.it", "www.figc.it"}
TACTICAL = ("tattic", "modello di gioco", "sistema di gioco", "pressing", "riaggress", "possesso", "transizion", "costruzion", "uefa pro")
TECHNICAL = ("tecnic", "gesto", "passaggio", "tiro", "controllo")
TRAINING = ("allenament", "esercitaz", "metodologia")


class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self._href=None; self._text=[]
    def handle_starttag(self, tag, attrs):
        if tag == "a": self._href=dict(attrs).get("href"); self._text=[]
    def handle_data(self, data):
        if self._href is not None: self._text.append(data)
    def handle_endtag(self, tag):
        if tag == "a" and self._href is not None:
            self.links.append((self._href," ".join(self._text).strip()))
            self._href=None; self._text=[]


def allowed(url):
    p=urlparse(url)
    return p.scheme == "https" and (p.hostname or "").casefold() in ALLOWED_HOSTS


def request(url, timeout):
    if not allowed(url): raise ValueError(f"URL outside FIGC allowlist: {url}")
    req=Request(url,headers={"User-Agent":"FOOTBALL-DATA-LAB-FIGC-Monitor/1.0","Accept":"text/html,application/pdf"})
    response=urlopen(req,timeout=timeout)
    if not allowed(response.geturl()):
        response.close(); raise ValueError(f"Redirect outside FIGC allowlist: {response.geturl()}")
    return response


def classify(title, sample=""):
    text=(title+" "+sample[:12000]).casefold()
    if any(x in text for x in TACTICAL): return "tattica"
    if any(x in text for x in TRAINING): return "allenamenti"
    if any(x in text for x in TECHNICAL): return "tecnica"
    return "review_required"


def discover(seeds, max_pages, timeout):
    queue=list(dict.fromkeys(seeds)); seen=set(); pdfs={}; errors=[]
    while queue and len(seen)<max_pages:
        url=queue.pop(0)
        if url in seen: continue
        seen.add(url)
        try:
            with request(url,timeout) as r:
                content_type=r.headers.get_content_type(); body=r.read(2_000_000)
            if content_type == "application/pdf" or body.startswith(b"%PDF-"):
                pdfs[url]={"url":url,"discovered_from":"direct","anchor":""}; continue
            parser=Links(); parser.feed(body.decode("utf-8","replace"))
            for href,text in parser.links:
                target=urljoin(url,href).split("#",1)[0]
                if not allowed(target): continue
                path=urlparse(target).path.casefold()
                if path.endswith(".pdf") or "/media/" in path:
                    pdfs.setdefault(target,{"url":target,"discovered_from":url,"anchor":text})
                elif "/it/tecnici/news/" in path and target not in seen:
                    queue.append(target)
        except Exception as exc:
            errors.append({"url":url,"error":f"{type(exc).__name__}: {exc}"})
    return list(pdfs.values()),errors,sorted(seen)


def known_hashes(roots):
    result={}
    for root in roots:
        if not root.is_dir(): continue
        for path in root.rglob("*.pdf"):
            digest=hashlib.sha256()
            with path.open("rb") as h:
                for chunk in iter(lambda:h.read(1024*1024),b""): digest.update(chunk)
            result.setdefault(digest.hexdigest(),str(path))
    return result


def verify(item, download_dir, timeout, max_bytes, write, existing):
    url=item["url"]
    digest=hashlib.sha256(); total=0; prefix=b""; chunks=[]
    with request(url,timeout) as r:
        content_type=r.headers.get_content_type(); final_url=r.geturl()
        while True:
            chunk=r.read(min(1024*1024,max_bytes-total+1))
            if not chunk: break
            total+=len(chunk)
            if total>max_bytes: raise ValueError(f"PDF exceeds {max_bytes} bytes")
            if len(prefix)<5: prefix=(prefix+chunk)[:5]
            digest.update(chunk)
            if write: chunks.append(chunk)
    if prefix != b"%PDF-": raise ValueError("Missing PDF signature")
    name=Path(urlparse(final_url).path).name or digest.hexdigest()+".pdf"
    row={**item,"final_url":final_url,"file_name":name,"content_type":content_type,
         "size_bytes":total,"sha256":digest.hexdigest(),"category":classify(name+" "+item.get("anchor","")),"status":"verified"}
    if row["sha256"] in existing:
        row["status"]="duplicate_existing"
        row["existing_path"]=existing[row["sha256"]]
        return row
    if write:
        download_dir.mkdir(parents=True,exist_ok=True)
        target=download_dir/name
        if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest()!=row["sha256"]:
            target=download_dir/f"{target.stem}-{row['sha256'][:12]}{target.suffix}"
        if not target.exists():
            fd,tmp=tempfile.mkstemp(prefix=f".{target.name}.",dir=download_dir)
            try:
                with os.fdopen(fd,"wb") as h:
                    for chunk in chunks: h.write(chunk)
                os.replace(tmp,target)
            finally:
                if os.path.exists(tmp): os.unlink(tmp)
        row["local_path"]=str(target)
        row["status"]="downloaded"
    return row


def append_events(path, events):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("a",encoding="utf-8") as h:
        for event in events: h.write(json.dumps(event,ensure_ascii=False,sort_keys=True)+"\n")


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--seed",action="append",default=[])
    p.add_argument("--candidate-url",action="append",default=[])
    p.add_argument("--max-pages",type=int,default=30)
    p.add_argument("--timeout",type=int,default=30)
    p.add_argument("--max-mib",type=int,default=100)
    p.add_argument("--write",action="store_true")
    p.add_argument("--download-dir",type=Path,default=Path("knowledge/candidates/figc-discovery/downloads"))
    p.add_argument("--events",type=Path,default=Path("knowledge/candidates/figc-discovery/events.jsonl"))
    p.add_argument("--report",type=Path)
    p.add_argument("--known-root",action="append",type=Path,default=[])
    a=p.parse_args()
    if a.max_pages<1 or a.timeout<1 or a.max_mib<1: p.error("limits must be positive")
    seeds=DEFAULT_SEEDS+a.seed
    for url in seeds+a.candidate_url:
        if not allowed(url): p.error(f"URL outside FIGC allowlist: {url}")
    found,errors,pages=discover(seeds,a.max_pages,a.timeout)
    roots=a.known_root or [Path("knowledge/sources"),Path("knowledge/candidates/drive11/sources")]
    existing=known_hashes(roots)
    known={x["url"]:x for x in found}
    for url in a.candidate_url: known.setdefault(url,{"url":url,"discovered_from":"candidate","anchor":""})
    verified=[]
    for item in sorted(known.values(),key=lambda x:x["url"]):
        try: verified.append(verify(item,a.download_dir,a.timeout,a.max_mib*1024*1024,a.write,existing))
        except Exception as exc: errors.append({**item,"status":"failed","error":f"{type(exc).__name__}: {exc}"})
    duplicates={}
    for row in verified: duplicates.setdefault(row["sha256"],[]).append(row["url"])
    report={"schema":"figc_pdf_discovery_v1","queries":QUERIES,"write":a.write,"pages_scanned":pages,
            "known_roots":[str(x) for x in roots],"known_pdf_hashes":len(existing),
            "documents":verified,"errors":errors,"duplicate_sha256":{k:v for k,v in duplicates.items() if len(v)>1}}
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if a.write:
        append_events(a.events,[{"event":"discovery",**row} for row in verified]+[{"event":"error",**row} for row in errors])
        if a.report:
            a.report.parent.mkdir(parents=True,exist_ok=True)
            a.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return 1 if errors else 0


if __name__ == "__main__": raise SystemExit(main())
