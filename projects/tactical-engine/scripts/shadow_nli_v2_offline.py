#!/usr/bin/env python3
"""Offline-only shadow NLI: prepare cited claim/evidence pairs, replay external verdicts.

No Ollama/Chroma access. Requires reviewed atomic claims; never changes source reports.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import re
from pathlib import Path

LABELS = {"supported", "contradicted", "insufficient"}
CITE = re.compile(r"\[F([1-9][0-9]*)\]")

def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def prepare(report, annotations):
    if not isinstance(report.get("questions"), list) or not isinstance(annotations.get("claims"), list):
        raise ValueError("Expected report.questions and annotations.claims")
    questions = {q["id"]: q for q in report["questions"]}
    if len(questions) != len(report["questions"]):
        raise ValueError("Duplicate question ID")
    seen, entries = set(), []
    for item in annotations["claims"]:
        qid, cid = item["question_id"], item["claim_id"]
        if (qid, cid) in seen:
            raise ValueError("Duplicate claim ID")
        seen.add((qid, cid))
        q = questions[qid]
        start, end = item["start"], item["end"]
        if (type(start) is not int or type(end) is not int or start < 0
                or end <= start or q["answer"][start:end] != item["span"]):
            raise ValueError("Claim span mismatch")
        claim = item["text"].strip()
        if not claim:
            raise ValueError("Empty claim")
        # Manual annotations must retain the cited answer wording; only citation markers may be removed.
        normalized_span = CITE.sub("", item["span"])
        normalized_span = " ".join(normalized_span.split()).strip(" .;:,!?")
        normalized_claim = " ".join(claim.split()).strip(" .;:,!?")
        if normalized_claim != normalized_span:
            raise ValueError("Claim text does not match cited answer span")
        citations = sorted(set(CITE.findall(item["span"])), key=int)
        sources = {r["label"]: r for r in q["evidence"]}
        if len(sources) != len(q["evidence"]):
            raise ValueError("Duplicate evidence label")
        invalid = ["F" + n for n in citations if "F" + n not in sources]
        pairs = []
        for n in citations:
            label = "F" + n
            if label not in sources:
                continue
            src = sources[label]
            pairs.append({"source_id": label, "source_chunk_id": src.get("id"),
                          "source_text_hash": sha(src["text"]), "claim": claim,
                          "evidence": src["text"], "nli_label": None, "elapsed_seconds": None})
        status = "invalid_citation" if invalid else ("no_citation" if not citations else "pending_nli")
        entries.append({"question_id": qid, "claim_id": cid, "claim": claim,
                        "answer_span": [start, end], "citation_ids": ["F" + n for n in citations],
                        "invalid_citation_ids": invalid, "status": status, "pairs": pairs})
    return {"schema": "dribbling_nli_shadow_offline_v1", "mode": "offline_only",
            "limitations": ["Claims manually annotated; extraction not validated",
                            "No NLI inference; labels pending",
                            "Valid citation IDs do not prove factual support"],
            "questions_in_source": len(questions), "claims": entries}

def apply_verdicts(prepared, verdicts):
    out = copy.deepcopy(prepared)
    lookup = {}
    for verdict in verdicts["verdicts"]:
        key = (verdict["question_id"], verdict["claim_id"], verdict["source_id"])
        if key in lookup or verdict["nli_label"] not in LABELS:
            raise ValueError("Duplicate or invalid verdict")
        lookup[key] = verdict
    used = set()
    for item in out["claims"]:
        labels = []
        for pair in item["pairs"]:
            key = (item["question_id"], item["claim_id"], pair["source_id"])
            verdict = lookup.get(key)
            if verdict is None:
                continue
            if verdict["source_text_hash"] != pair["source_text_hash"]:
                raise ValueError("Evidence hash mismatch")
            used.add(key)
            pair["nli_label"] = verdict["nli_label"]
            pair["elapsed_seconds"] = verdict.get("elapsed_seconds")
            labels.append(verdict["nli_label"])
        if item["status"] == "pending_nli" and len(labels) == len(item["pairs"]):
            if "supported" in labels and "contradicted" in labels:
                item["status"] = "conflicting_evidence_review"
            elif "supported" in labels:
                item["status"] = "supported_by_cited_evidence"
            elif "contradicted" in labels:
                item["status"] = "contradicted_by_cited_evidence"
            else:
                item["status"] = "citation_without_support"
    if used != set(lookup):
        raise ValueError("Unknown verdict claim/source")
    out["mode"] = "offline_verdict_replay"
    return out

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--claims", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--verdicts", type=Path)
    args = parser.parse_args()
    inputs = [args.source, args.claims] + ([args.verdicts] if args.verdicts else [])
    if args.output.resolve() in {path.resolve() for path in inputs}:
        parser.error("Output must not overwrite an input")
    result = prepare(json.loads(args.source.read_text(encoding="utf-8")),
                     json.loads(args.claims.read_text(encoding="utf-8")))
    if args.verdicts:
        result = apply_verdicts(result, json.loads(args.verdicts.read_text(encoding="utf-8")))
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(f"SHADOW OFFLINE PASS: {len(result['claims'])} claims; {args.output}")

if __name__ == "__main__":
    main()
