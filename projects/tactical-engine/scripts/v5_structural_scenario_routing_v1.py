#!/usr/bin/env python3
"""Generic structural-context reservation for formation/role scenario questions."""
from __future__ import annotations

import re


ROLE_ANCHORS = {
    "terzino": ("terzino", "difensore esterno"),
    "mezzala": ("mezzala", "interno di centrocampo"),
    "ala": ("ala", "esterno d'attacco", "esterno alto"),
    "centravanti": ("centravanti", "punta centrale"),
    "braccetto": ("braccetto", "difensore centro-destro", "difensore centro-sinistro"),
    "mediano": ("vertice basso", "mediano", "play basso"),
    "trequartista": ("trequartista", "sottopunta"),
}
PRINCIPLE_ANCHORS = (
    "marcatura preventiva", "copertura preventiva", "seconda palla", "half-space",
    "corridoio interno", "sovrapposizione", "sotto-sovrapposizione", "terzo uomo",
    "raddoppio", "ampiezza", "profondità", "transizione negativa",
)
MOVEMENT_QUERY_CUES = ("quale movimento", "movimento sincronizzato", "andare in porta", "attaccare lo spazio", "corsa")
MOVEMENT_TEXT_CUES = ("inserimento", "si inserisce", "corsa", "sovrapposizione", "profondità", "spazio creato", "taglio")
UNDERLAP_TEXT_CUES = ("sottoposizione", "sotto-sovrapposizione", "underlap", "corridoio interno", "terzino interno", "mezzo spazio")


def _normal(value: str) -> str:
    return re.sub(r"\s+", " ", value.casefold().replace("–", "-").replace("—", "-")).strip()


def anchors(question: str) -> dict:
    query = _normal(question)
    formations = set(re.findall(r"(?<!\d)(?:[1-9]-){2,3}[1-9](?!\d)", query))
    formations |= {value[2:] for value in formations if value.startswith("1-")}
    roles = {name for name, aliases in ROLE_ANCHORS.items() if any(alias in query for alias in aliases)}
    principles = {term for term in PRINCIPLE_ANCHORS if term in query}
    if any(cue in query for cue in MOVEMENT_QUERY_CUES):
        principles.add("movimento sincronizzato")
    if {"terzino", "ala"}.issubset(roles) and "half-space" in principles and "movimento sincronizzato" in principles:
        principles.add("underlap")
    return {"formations": formations, "roles": roles, "principles": principles}


def score_row(row: dict, signals: dict) -> int:
    haystack = _normal(" ".join((str(row.get("source") or ""), " ".join(row.get("headings") or []), str(row.get("text") or ""))))
    formation_hits = sum(value in haystack or ("1-" + value) in haystack for value in signals["formations"])
    role_hits = sum(any(alias in haystack for alias in ROLE_ANCHORS[name]) for name in signals["roles"])
    principle_hits = sum(
        any(cue in haystack for cue in MOVEMENT_TEXT_CUES) if term == "movimento sincronizzato"
        else any(cue in haystack for cue in UNDERLAP_TEXT_CUES) if term == "underlap"
        else term in haystack
        for term in signals["principles"]
    )
    return formation_hits * 10 + role_hits * 3 + principle_hits * 7


def reserve(rows: list[dict], rerank_scores, selected: list[dict], question: str, limit: int, maximum: int = 3):
    signals = anchors(question)
    if len(signals["formations"]) + len(signals["roles"]) + len(signals["principles"]) < 2:
        return selected, [], signals
    scored = []
    for index, row in enumerate(rows):
        structural = score_row(row, signals)
        if structural >= 6:
            semantic = float(rerank_scores[index]) if index < len(rerank_scores) else 0.0
            scored.append((structural, semantic, row))
    scored.sort(key=lambda value: (-value[0], -value[1], str(value[2].get("source", "")).casefold()))
    reserved = []
    used_sources = set()
    for _, _, row in scored:
        source = row.get("source")
        if source in used_sources:
            continue
        reserved.append(row)
        used_sources.add(source)
        if len(reserved) >= maximum:
            break
    if not reserved:
        return selected, [], signals
    reserved_ids = {row["id"] for row in reserved}
    revised = (reserved + [row for row in selected if row["id"] not in reserved_ids])[:limit]
    return revised, [row["id"] for row in reserved], signals
