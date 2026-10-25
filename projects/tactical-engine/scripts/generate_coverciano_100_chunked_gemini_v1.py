#!/usr/bin/env python3
"""Generate Coverciano-100 in ten resumable Gemini requests of ten questions."""
from __future__ import annotations
import argparse, datetime as dt, hashlib, importlib.util, json, os, re, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("base", ROOT / "scripts/generate_coverciano_100_gemini_v1.py")
BASE = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(BASE)

def api_key():
    path = ROOT / ".env"
    if path.is_file():
        for raw in path.read_text(encoding="utf-8").splitlines():
            if raw.strip().startswith("GEMINI_API_KEY="):
                os.environ.setdefault("GEMINI_API_KEY", raw.split("=",1)[1].strip().strip("'\"")); break
    value=os.environ.get("GEMINI_API_KEY","")
    if not value: raise SystemExit("GEMINI_API_KEY_MISSING")
    return value

def write_new(path,payload):
    if path.exists(): raise SystemExit(f"REFUSING_OVERWRITE: {path}")
    path.parent.mkdir(parents=True,exist_ok=True); tmp=path.with_name(f".{path.name}.tmp.{os.getpid()}")
    tmp.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); tmp.replace(path)

def validate_part(rows, category, start, count=10):
    if not isinstance(rows,list) or len(rows)!=count: raise ValueError(f"EXPECTED_{count}")
    seen=set()
    for offset,row in enumerate(rows):
        if row.get("id") != f"coverciano_{start+offset:03d}" or row.get("category") != category: raise ValueError("ID_OR_CATEGORY")
        question=" ".join(str(row.get("question","")).split()); norm=re.sub(r"[^a-z0-9]+"," ",question.casefold()).strip()
        if len(question)<120 or norm in seen: raise ValueError("SHORT_OR_DUPLICATE"); seen.add(norm)
        if row.get("difficulty") not in (3,4,5): raise ValueError("DIFFICULTY")
        rubric=row.get("hidden_rubric",{})
        if not all(isinstance(rubric.get(x),list) and rubric[x] for x in ("constraints","expected_points","critical_errors")): raise ValueError("RUBRIC")
    return rows

def generate(args):
    index=BASE.CATEGORIES.index(args.category); category_start=index*10+1
    count=5 if args.part else 10; start=category_start + ((args.part-1)*5 if args.part else 0)
    system=f"""Sei una commissione UEFA Pro. Genera esattamente {count} domande originali
da esame Coverciano esclusivamente sulla categoria {args.category}. Scenari
realistici e difficili con moduli, fase, tempo/punteggio, vincoli, compiti e
geometrie concrete. SOLO JSON: {{"questions":[{{"id":"coverciano_{start:03d}",
"category":"{args.category}","difficulty":4,"question":"...",
"hidden_rubric":{{"constraints":["..."],"expected_points":["..."],
"critical_errors":["..."]}}}}]}}. ID consecutivi da {start:03d} a {start+count-1:03d}."""
    question_schema={"type":"object","required":["id","category","difficulty","question","hidden_rubric"],"properties":{
        "id":{"type":"string"},"category":{"type":"string","enum":[args.category]},
        "difficulty":{"type":"integer","enum":[3,4,5]},"question":{"type":"string"},
        "hidden_rubric":{"type":"object","required":["constraints","expected_points","critical_errors"],"properties":{
            "constraints":{"type":"array","items":{"type":"string"}},"expected_points":{"type":"array","items":{"type":"string"}},
            "critical_errors":{"type":"array","items":{"type":"string"}}}}}}
    payload={"system_instruction":{"parts":[{"text":system}]},"contents":[{"role":"user","parts":[{"text":BASE.BASE_PROMPT}]}],
             "generationConfig":{"temperature":0.5,"responseMimeType":"application/json","responseSchema":{
                 "type":"object","required":["questions"],"properties":{"questions":{"type":"array","minItems":count,"maxItems":count,"items":question_schema}}},
                 "maxOutputTokens":10000}}
    key=api_key(); url=f"https://generativelanguage.googleapis.com/v1beta/models/{args.model}:generateContent"
    req=urllib.request.Request(url,data=json.dumps(payload).encode(),headers={"Content-Type":"application/json","x-goog-api-key":key},method="POST")
    try:
        with urllib.request.urlopen(req,timeout=240) as response: raw=json.loads(response.read())
        text="".join(p.get("text","") for p in raw["candidates"][0]["content"]["parts"])
        try:
            parsed=json.loads(text)
        except json.JSONDecodeError as exc:
            diagnostic=args.output.with_name(args.output.stem+".invalid-output.json")
            write_new(diagnostic,{"schema":"gemini_invalid_output_v1","category":args.category,"part":args.part,
                "model":args.model,"finish_reason":raw.get("candidates",[{}])[0].get("finishReason"),
                "text_sha256":hashlib.sha256(text.encode()).hexdigest(),"text_length":len(text),
                "error":str(exc)[:300]})
            raise
        rows=validate_part(parsed["questions"],args.category,start,count)
    except urllib.error.HTTPError as exc:
        detail=exc.read().decode(errors="replace")[:1200].replace(key,"[REDACTED]")
        raise SystemExit(f"CHUNK_HTTP_{exc.code}: {detail}")
    except (urllib.error.URLError,KeyError,ValueError,json.JSONDecodeError) as exc:
        raise SystemExit(f"CHUNK_FAILED: {type(exc).__name__}: {str(exc)[:300].replace(key,'[REDACTED]')}")
    write_new(args.output,{"schema":"coverciano_gemini_question_chunk_v1","status":"ESEGUITO","model":args.model,"category":args.category,
        "start_id":start,"generated_at_utc":dt.datetime.now(dt.timezone.utc).isoformat(),"usage_metadata":raw.get("usageMetadata",{}),"questions":rows})
    print(json.dumps({"status":"ESEGUITO","category":args.category,"part":args.part or None,"count":count}))

def merge_category(args):
    index=BASE.CATEGORIES.index(args.category); start=index*10+1; rows=[]; models=set()
    for part in (1,2):
        data=json.loads((args.input_dir/f"coverciano_{args.category}_part{part}_v1.json").read_text(encoding="utf-8"))
        rows.extend(data["questions"]); models.add(data["model"])
    validate_part(rows,args.category,start,10)
    write_new(args.output,{"schema":"coverciano_gemini_question_chunk_v1","status":"ESEGUITO","model":"+".join(sorted(models)),
        "category":args.category,"start_id":start,"generated_at_utc":dt.datetime.now(dt.timezone.utc).isoformat(),"questions":rows})
    print(json.dumps({"status":"ESEGUITO","category":args.category,"count":10,"merged_parts":2}))

def merge(args):
    rows=[]; models=set()
    for category in BASE.CATEGORIES:
        data=json.loads((args.input_dir/f"coverciano_{category}_v1.json").read_text(encoding="utf-8")); rows.extend(data["questions"]); models.add(data["model"])
    BASE.validate(rows)
    write_new(args.output,{"schema":"coverciano_gemini_question_manifest_v1","status":"ESEGUITO","transport":"chunked generateContent",
        "models":sorted(models),"base_prompt":BASE.BASE_PROMPT,"question_count":100,
        "categories":{c:10 for c in BASE.CATEGORIES},"questions_sha256":hashlib.sha256(json.dumps(rows,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),"questions":rows})
    print(json.dumps({"status":"ESEGUITO","question_count":100}))

def main():
    parser=argparse.ArgumentParser(); sub=parser.add_subparsers(dest="action",required=True)
    gen=sub.add_parser("generate"); gen.add_argument("--category",choices=BASE.CATEGORIES,required=True); gen.add_argument("--model",default="gemini-3.6-flash"); gen.add_argument("--part",type=int,choices=(1,2)); gen.add_argument("--output",type=Path,required=True)
    cat=sub.add_parser("merge-category"); cat.add_argument("--category",choices=BASE.CATEGORIES,required=True); cat.add_argument("--input-dir",type=Path,required=True); cat.add_argument("--output",type=Path,required=True)
    mer=sub.add_parser("merge"); mer.add_argument("--input-dir",type=Path,required=True); mer.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    if args.action=="generate": generate(args)
    elif args.action=="merge-category": merge_category(args)
    else: merge(args)
if __name__=="__main__": main()
