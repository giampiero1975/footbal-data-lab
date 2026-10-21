#!/usr/bin/env python3
"""Read-only exact text dedup simulation for DRIBBLING V5 A/B evidence."""
import argparse
import hashlib
import json
import re
from pathlib import Path

def normalize(text):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", text.casefold())).strip()

def deduplicate(rows):
    kept, seen, duplicates = [], {}, []
    for index, row in enumerate(rows, 1):
        key = hashlib.sha256(normalize(row["text"]).encode("utf-8")).hexdigest()
        if key in seen:
            original_index = seen[key]
            duplicates.append({"duplicate_original_slot": index,
                               "kept_original_slot": original_index,
                               "duplicate_source": row["source"],
                               "kept_source": rows[original_index-1]["source"]})
        else:
            seen[key] = index
            kept.append({"original_slot": index, "source": row["source"], "id": row["id"]})
    return kept, duplicates

def simulate(report):
    result = {"collection": report["collection"], "mode": "read_only_final_evidence_simulation",
              "questions": [], "totals": {"duplicate_slots_removed": 0,
                                         "evidence_before": 0, "evidence_after": 0},
              "limits": ["Only 8 selected chunks per question are stored in the A/B JSON.",
                         "Replacing removed duplicates requires reranking the original 24 candidates.",
                         "Existing answers are not regenerated or rescored.",
                         "Source files and ChromaDB remain unchanged."]}
    for q in report["questions"]:
        kept, duplicates = deduplicate(q["evidence"])
        result["questions"].append({"id": q["id"], "before": len(q["evidence"]),
                                    "after": len(kept), "kept": kept, "duplicates": duplicates,
                                    "available_replacement_candidates": "not_in_report"})
        result["totals"]["duplicate_slots_removed"] += len(duplicates)
        result["totals"]["evidence_before"] += len(q["evidence"])
        result["totals"]["evidence_after"] += len(kept)
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = json.loads(args.input.read_text(encoding="utf-8"))
    result = simulate(report)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result["totals"], ensure_ascii=False))

if __name__ == "__main__":
    main()
