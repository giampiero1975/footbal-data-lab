"""Semantic source ranking for opt-in V5 heading reservation.

Rank source-level descriptions, not the number of formation headings.
Uses the existing cross-encoder; no gold labels, benchmark IDs or index writes.
"""
import re

def source_profiles(rows):
    groups = {}
    for row in rows:
        source = row["source"]
        if "manual" not in source.casefold():
            continue
        group = groups.setdefault(source, {"forms": set(), "texts": []})
        for heading in row.get("headings") or []:
            if re.fullmatch(r"(?:[1-5]-){2,4}[1-5]", heading.strip()):
                group["forms"].add(heading.strip())
                if len(group["texts"]) < 8:
                    group["texts"].append(row["text"][:260])
    return {name: data for name, data in groups.items() if len(data["forms"]) >= 2}

def semantic_source_scores(question, rows, reranker):
    return {
        item["source"]: item["score"]
        for item in semantic_source_ranking(question, rows, reranker)
    }

def semantic_source_ranking(question, rows, reranker):
    """Return an inspectable, deterministic ranking of eligible sources."""
    profiles = source_profiles(rows)
    names = sorted(profiles)
    if not names:
        return []
    # Represent the source by its title and short actual indexed excerpts.
    # Repeating the title preserves document identity for the cross-encoder.
    pairs = []
    for name in names:
        title = name.replace("_", " ")
        snippets = profiles[name]["texts"]
        summary = " | ".join(snippets[:4])
        pairs.append((question, (title + ". " + summary)[:1200]))
    scores = reranker.predict(pairs, batch_size=1, show_progress_bar=False)
    ranking = [
        {
            "source": name,
            "score": float(score),
            "formations": sorted(profiles[name]["forms"]),
            "profile_excerpt_count": len(profiles[name]["texts"]),
        }
        for name, score in zip(names, scores)
    ]
    return sorted(ranking, key=lambda item: (-item["score"], item["source"]))
