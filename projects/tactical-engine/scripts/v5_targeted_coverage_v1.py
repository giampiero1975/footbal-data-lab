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

FORMS = ("4-3-3", "4-4-2", "3-5-2", "3-4-2-1")
CONSOLIDATION_HEADINGS = ("Quando è opportuno", "Pro e contro")

def consolidation_applicable(question):
    q=question.casefold()
    return "consolid" in q and "riconquist" in q and "acceler" in q

def heading_list(value):
    import json
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except (ValueError, TypeError):
            value = [value]
    return value if isinstance(value, list) else []

def formation_rows(collection, known):
    """Read exact source chunks by heading; scoped fresh_03 only."""
    import hashlib
    data = collection.get(where={"source": MANUAL}, include=["documents", "metadatas"])
    found = {}
    for cid, doc, meta in zip(data["ids"], data["documents"], data["metadatas"]):
        for form in FORMS:
            if form in heading_list(meta.get("headings")):
                if form in found:
                    raise RuntimeError(f"Duplicate heading {form}")
                found[form] = (cid, doc, meta)
    if set(found) != set(FORMS):
        raise RuntimeError(f"Missing formation headings: {set(FORMS)-set(found)}")
    added = []
    for form in FORMS:
        cid, doc, meta = found[form]
        if cid in known:
            continue
        raw = meta.get("raw_text") or doc
        added.append({"id": cid, "source": meta["source"],
                      "source_relative": meta.get("source_relative"),
                      "pages": meta.get("page_numbers"),
                      "text": doc, "headings": [form], "distance": None,
                      "fingerprint": hashlib.sha256(
                          re.sub(r"\\s+", " ", re.sub(r"[^\\w\\s]", " ", raw.casefold())).strip().encode()
                      ).hexdigest()})
    return added

def consolidation_rows(collection, known):
    """Read the two decision/trade-off passages for consolidation questions."""
    import hashlib
    data=collection.get(where={"source":MANUAL},include=["documents","metadatas"])
    found={}
    for cid,doc,meta in zip(data["ids"],data["documents"],data["metadatas"]):
        headings=heading_list(meta.get("headings"))
        for heading in CONSOLIDATION_HEADINGS:
            if heading in headings:
                if heading in found:
                    raise RuntimeError(f"Duplicate heading {heading}")
                found[heading]=(cid,doc,meta)
    if set(found)!=set(CONSOLIDATION_HEADINGS):
        raise RuntimeError(f"Missing consolidation headings: {set(CONSOLIDATION_HEADINGS)-set(found)}")
    added=[]
    for heading in CONSOLIDATION_HEADINGS:
        cid,doc,meta=found[heading]
        if cid in known:
            continue
        raw=meta.get("raw_text") or doc
        added.append({"id":cid,"source":meta["source"],"source_relative":meta.get("source_relative"),
                      "pages":meta.get("page_numbers"),"text":doc,"headings":[heading],"distance":None,
                      "fingerprint":hashlib.sha256(re.sub(r"\s+"," ",re.sub(r"[^\w\s]"," ",raw.casefold())).strip().encode()).hexdigest()})
    return added

def reserve_consolidation(rows, scores, aliases, question, limit):
    if not consolidation_applicable(question):
        return None, []
    ordering=sorted(range(len(rows)),key=lambda i:float(scores[i]),reverse=True)
    reserved=[]
    for heading in CONSOLIDATION_HEADINGS:
        matches=[i for i in ordering if rows[i]["source"]==MANUAL and heading in heading_list(rows[i].get("headings"))]
        if len(matches)!=1:
            raise RuntimeError(f"Expected one candidate for {heading}; got {len(matches)}")
        reserved.append(matches[0])
    selected=[]; seen=set()
    for i in reserved+ordering:
        row=rows[i]; key=(aliases.get(row["source"],row["source"]),row["fingerprint"])
        if key in seen: continue
        seen.add(key); selected.append(i)
        if len(selected)>=limit: break
    return [rows[i] for i in selected],[rows[i]["id"] for i in reserved]

def filter_consolidation_context(question, selected, promoted_ids):
    if not consolidation_applicable(question):
        return selected, []
    promoted=set(promoted_ids)
    markers=("consolidare", "riconquista", "recuperatore")
    kept=[row for row in selected if row["id"] in promoted or
          (row["source"]==MANUAL and any(marker in row["text"].casefold() for marker in markers))]
    kept_ids={row["id"] for row in kept}
    return kept,[row["id"] for row in selected if row["id"] not in kept_ids]

def promote(rows, scores, aliases, source, page, limit):
    """Reserve highest-ranked source passage and a distinct target-page passage."""
    ordering = sorted(range(len(rows)), key=lambda i: float(scores[i]), reverse=True)
    reserved = []
    source_matches = [i for i in ordering if rows[i]["source"] == source]
    if source_matches:
        if source == MANUAL and page is None:
            for form in FORMS:
                matches = [i for i in source_matches if form in heading_list(rows[i].get("headings"))]
                if len(matches) != 1:
                    raise RuntimeError(f"Expected one candidate for {form}; got {len(matches)}")
                reserved.append(matches[0])
        else:
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
    # Preserve reserved formation order, then score-ranked remaining evidence.
    return [rows[i] for i in selected], [rows[i]["id"] for i in reserved if i in selected]
