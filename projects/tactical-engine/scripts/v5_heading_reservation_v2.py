"""Evidence reservation for metadata heading groups (opt-in)."""
import re
from v5_source_semantic_rank_v3 import semantic_source_scores
from v5_heading_routing_v1 import headings, FORMATION, should_expand

def reserve(rows, scores, question, aliases, limit, reranker=None):
    if not should_expand(question) or "manuale" not in question.casefold():
        return None, []
    groups = {}
    for i, row in enumerate(rows):
        if "manual" not in row["source"].casefold():
            continue
        for h in headings(row.get("headings")):
            if FORMATION.fullmatch(h.strip()):
                groups.setdefault(row["source"], {}).setdefault(h.strip(), []).append(i)
    groups = {s: f for s, f in groups.items() if len(f) >= 2}
    if not groups:
        return None, []
    terms = set(re.findall(r"[a-zà-ÿ]{5,}", question.casefold()))
    def rank(source):
        topical = len(terms & set(re.findall(r"[a-zà-ÿ]{5,}", source.casefold())))
        return (topical, len(groups[source]))
    source = max(sorted(groups), key=rank)
    chosen = []
    seen = set()
    def append(i):
        row = rows[i]
        key = (aliases.get(row["source"], row["source"]), row["fingerprint"])
        if key not in seen:
            chosen.append(i)
            seen.add(key)
    for h in sorted(groups[source])[:max(2, limit // 2)]:
        append(max(groups[source][h], key=lambda i: float(scores[i])))
    reserved = [rows[i]["id"] for i in chosen]
    for i in sorted(range(len(rows)), key=lambda i: float(scores[i]), reverse=True):
        append(i)
        if len(chosen) >= limit:
            break
    return [rows[i] for i in chosen], reserved
