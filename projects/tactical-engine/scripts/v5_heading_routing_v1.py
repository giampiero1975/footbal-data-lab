"""Read-only, question-driven formation heading retrieval for V5.

No benchmark IDs, gold labels, or fixed formation lists are used.
"""
import hashlib
import json
import re

FORMATION = re.compile(r"(?<!\d)(?:[1-5]-){2,4}[1-5](?!\d)")
CUES = ("modulo", "moduli", "assetto", "assetti", "sistema di gioco", "sistemi di gioco", "formazione", "formazioni")

def headings(value):
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except (TypeError, ValueError):
            value = [value]
    return [str(x) for x in value] if isinstance(value, list) else []

def should_expand(question):
    q = question.casefold()
    return any(cue in q for cue in CUES) and any(
        cue in q for cue in ("manuale", "descrizion", "confront", "differenz", "cambiar", "variare", "passaggio")
    )

def expand(collection, question, known, normalizer):
    """Select distinct source headings matching formations, only for relevant questions.

    Bound source read to sources already represented in retrieved evidence.
    """
    if not should_expand(question):
        return []
    sources = {row["source"] for row in known.values()}
    if "manuale" in question.casefold():
        # Source-name discovery is read-only and independent of locked question IDs.
        catalog = collection.get(include=["metadatas"])
        sources.update(meta.get("source", "") for meta in catalog["metadatas"]
                       if "manual" in meta.get("source", "").casefold())
    sources = sorted(source for source in sources if source)
    explicit = set(FORMATION.findall(question))
    added = []
    for source in sources:
        data = collection.get(where={"source": source}, include=["documents", "metadatas"])
        candidates = []
        for cid, doc, meta in zip(data["ids"], data["documents"], data["metadatas"]):
            hs = headings(meta.get("headings"))
            forms = [h for h in hs if FORMATION.fullmatch(h.strip())]
            if not forms or cid in known:
                continue
            if explicit and not any(f in explicit for f in forms):
                continue
            raw = meta.get("raw_text") or doc
            candidates.append((forms[0], cid, doc, meta, hs, raw))
        # Do not force arbitrary formations into context when no names were requested.
        for _, cid, doc, meta, hs, raw in sorted(candidates)[:24]:
            added.append({"id": cid, "source": meta["source"],
                "source_relative": meta.get("source_relative"),
                "pages": meta.get("page_numbers"), "text": doc,
                "headings": hs, "distance": None,
                "fingerprint": hashlib.sha256(normalizer(raw).encode()).hexdigest()})
    return added

def generation_guidance(question):
    if not should_expand(question):
        return ""
    return (" Se le fonti presentano moduli o assetti con intestazioni, identifica quelli "
            "effettivamente pertinenti con citazioni. Non attribuire effetti causali a "
            "descrizioni tattiche: per affermare che un cambio di modulo modifichi il rischio "
            "servono evidenze comparative adeguate; in loro assenza esplicita il limite.")
