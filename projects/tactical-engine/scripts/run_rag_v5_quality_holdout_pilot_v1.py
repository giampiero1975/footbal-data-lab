#!/usr/bin/env python3
"""Run frozen candidate questions using the existing read-only V5 E2E smoke pipeline."""
import argparse
import json
import sys
from pathlib import Path
import smoke_test_rag_v5_e2e as v5

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--questions",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--model",default="qwen3.5:9b")
    parser.add_argument("--timeout",type=int,default=900)
    parser.add_argument("--execute",action="store_true")
    args=parser.parse_args()
    if not args.execute:
        parser.error("Explicit --execute required")
    if args.questions.resolve()==args.output.resolve() or args.output.exists():
        parser.error("Refusing to overwrite input or existing report")
    dataset=json.loads(args.questions.read_text(encoding="utf-8"))
    if dataset.get("schema")!="rag_v5_quality_holdout_pilot_questions_v1":
        parser.error("Unexpected question schema")
    questions=dataset["questions"]
    if len(questions)!=10 or len({r["id"] for r in questions})!=10:
        parser.error("Expected ten distinct questions")
    v5.QUESTIONS=[(r["id"],r["question"]) for r in questions]
    sys.argv=[str(Path(v5.__file__)), "--model",args.model,"--timeout",str(args.timeout),
              "--limit","8","--output",str(args.output)]
    v5.main()
    print("NOTE: Candidate pilot only; answers require independent manual review. No 9/10 claim.")

if __name__=="__main__":
    main()
