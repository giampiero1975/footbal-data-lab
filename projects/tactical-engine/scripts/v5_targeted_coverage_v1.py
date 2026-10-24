"""Opt-in targeted coverage for locked V5 diagnostics; no index writes."""
import re

MANUAL = "FOOTBALL_DATA_LAB_Transizioni_Offensive_e_Difensive_Manuale"
USSIA = "Transizioni.Ussia"

def target(qid, question):
    # Diagnostic-only rule, intentionally scoped to the two recorded FAIL cases.
    if qid == "fresh_03" and "manuale interno" in question.casefold():
        return MANUAL, None
    if qid == "fresh_10" and "ussia" in question.casefold():
        return USSIA, 17
    return None, None

def contains_page(value, page):
    return str(page) in re.findall(r"\d+", str(value))

def promote(rows, scores, aliases, source, page, limit):
    """Reserve highest-ranked source passage and a distinct target-page passage."""
    ordering = sorted(range(len(rows)), key=lambda i: float(scores[i]), reverse=True)
    reserved = []
    source_matches = [i for i in ordering if rows[i]["source"] == source]
    if source_matches:
        reserved.append(source_matches[0])
    if page is not None:
        page_matches = [i for i in source_matches if contains_page(rows[i].get("pages"), page)]
        if page_matches and page_matches[0] not in reserved:
            reserved.append(page_matches[0])
    selected, seen = [], set()
    for i in reserved + ordering:
        row = rows[i]
        key = (aliases.get(row["source"], row["source"]), row["fingerprint"])
        if key in seen:
            continue
        seen.add(key)
        selected.append(i)
        if len(selected) >= limit:
            break
    selected.sort(key=lambda i: float(scores[i]), reverse=True)
    return [rows[i] for i in selected], [rows[i]["id"] for i in reserved if i in selected]
