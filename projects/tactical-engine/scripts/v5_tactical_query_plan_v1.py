#!/usr/bin/env python3
"""Deterministic tactical question planning and evidence diversification.

The module is deliberately model-free: it extracts the requested tactical
facets, builds bounded retrieval queries and reserves evidence covering
different facets.  It never writes to the index and contains no benchmark IDs.
"""
from __future__ import annotations

import re


FACETS = {
    "possession": ("fase di possesso", "costruzione", "sviluppo", "rifinitura", "attacco", "offensivo", "palla nostra"),
    "non_possession": ("fase di non possesso", "blocco", "difesa", "difendere", "scivolamento", "sotto-blocco", "fuorigioco"),
    "negative_transition": ("transizione negativa", "perdita", "riaggressione", "contro-pressing", "ripiegamento"),
    "positive_transition": ("transizione positiva", "riconquista", "contropiede", "ripartenza"),
    "prevention": ("preventiva", "marcatura preventiva", "copertura preventiva", "seconda palla", "equilibrio"),
    "goalkeeper": ("portiere", "estremo difensore"),
    "third_man": ("terzo uomo", "3° uomo"),
    "width": ("ampiezza", "corsia laterale", "cambio gioco", "cambio di gioco", "lato debole"),
    "inside_space": ("rifinitura", "tra le linee", "half-space", "corridoio interno", "interspazio"),
    "box": ("area di rigore", "primo palo", "secondo palo", "dischetto", "fuori area", "cross"),
    "offside": ("fuorigioco", "palla scoperta", "palla libera", "palla coperta"),
    "substitutions": ("sostituz", "cambio di sistema", "cambi di sistema", "gestione del risultato"),
    "communication": ("comunicazione", "comando", "leader", "segnale"),
    "psychology": ("emotiv", "psicolog", "pressione della gara"),
}

OPPOSITE = {
    "possession": "non_possession",
    "non_possession": "possession",
    "negative_transition": "positive_transition",
    "positive_transition": "negative_transition",
}

FACET_GUIDANCE = {
    "possession": "Descrivi soltanto azioni della squadra in possesso; non introdurre perdita, marcatura o pressing difensivo salvo che siano richiesti.",
    "non_possession": "Definisci riferimenti, distanze, scivolamenti e protezione della porta senza trasformarli in principi di costruzione offensiva.",
    "negative_transition": "Confronta riaggressione e ripiegamento usando prossimità e densità attorno alla palla, zona del campo, palla coperta/scoperta, qualità dell'avversario e preventive già predisposte.",
    "prevention": "Indica sempre quanti e quali giocatori restano in equilibrio, cosa controllano e come proteggono profondità e seconde palle.",
    "goalkeeper": "Spiega come il portiere crea superiorità, orienta il pressing e sceglie tra uscita corta e soluzione oltre pressione.",
    "third_man": "Rendi esplicita la sequenza portatore-appoggio-terzo uomo, lo spazio liberato e il tempo del movimento.",
    "width": "Distingui lato palla e lato debole, momento del cambio gioco e duello o superiorità creati in ampiezza.",
    "inside_space": "Distingui la fascia orizzontale di rifinitura dai corridoi verticali interni e specifica postura e smarcamento del ricevente.",
    "box": "Mappa occupazione e responsabilità su primo palo, zona centrale/dischetto, secondo palo e limite area, oltre al coordinamento col portiere.",
    "offside": "Distingui palla coperta e scoperta, gioco aperto e palla inattiva; specifica leader, comando, innesco e rischio alle spalle.",
    "substitutions": "Per ogni cambio indica giocatore/ruolo che esce ed entra, nuova struttura, compito concreto e rischio compensato.",
    "communication": "Indica chi comunica, con quale comando o canale e in quale momento della gara.",
    "psychology": "Collega l'impatto emotivo a un comportamento osservabile e a una comunicazione concreta, non a formule astratte.",
}


def normal(value: str) -> str:
    return re.sub(r"\s+", " ", value.casefold().replace("–", "-").replace("—", "-")).strip()


def analyse(question: str) -> dict:
    query = normal(question)
    facets = [name for name, cues in FACETS.items() if any(cue in query for cue in cues)]
    formations = sorted(set(re.findall(r"(?<!\d)(?:[1-9]-){2,3}[1-9](?!\d)", query)))
    roles = sorted(set(re.findall(
        r"\b(?:portiere|terzino|braccetto|difensore centrale|centrale|mediano|vertice basso|mezzala|trequartista|ala|esterno|centravanti|punta)\b",
        query,
    )))
    request_parts = []
    for part in re.split(r"[?;]|\b(?:inoltre|infine|considerando|e come)\b", query):
        part = part.strip(" .,:-")
        if len(part.split()) >= 4 and part not in request_parts:
            request_parts.append(part)
    return {
        "facets": facets,
        "formations": formations,
        "roles": roles,
        "request_parts": request_parts[:8],
    }


def retrieval_queries(question: str, plan: dict, maximum: int = 5) -> list[str]:
    """Return the original question plus bounded, facet-specific expansions."""
    queries = [" ".join(question.split())]
    context = " ".join(plan["formations"] + plan["roles"][:5])
    for facet in plan["facets"]:
        cues = " ".join(FACETS[facet][:4])
        candidate = f"{cues} {context}".strip()
        if candidate and candidate not in queries:
            queries.append(candidate)
        if len(queries) >= maximum:
            break
    return queries


def row_facets(row: dict) -> set[str]:
    text = normal(" ".join((str(row.get("source") or ""), " ".join(row.get("headings") or []), str(row.get("text") or ""))))
    return {name for name, cues in FACETS.items() if any(cue in text for cue in cues)}


def phase_adjustment(row: dict, plan: dict) -> int:
    present = row_facets(row)
    requested = set(plan["facets"])
    score = 4 * len(present & requested)
    for wanted, opposite in OPPOSITE.items():
        if wanted in requested and opposite in present and wanted not in present:
            score -= 7
    return score


def diversify(rows: list[dict], scores, selected: list[dict], plan: dict, limit: int, maximum: int = 4):
    """Reserve distinct evidence for requested facets, then retain semantic rank."""
    requested = list(plan["facets"])
    if not requested:
        return selected, [], {}
    ranked = sorted(
        range(len(rows)),
        key=lambda i: (float(scores[i]) + phase_adjustment(rows[i], plan), float(scores[i])),
        reverse=True,
    )
    reserved = []
    covered: dict[str, str] = {}
    used_sources = set()
    for facet in requested:
        for index in ranked:
            row = rows[index]
            if facet not in row_facets(row) or row["id"] in {item["id"] for item in reserved}:
                continue
            source = row.get("source")
            if source in used_sources and len(rows) > limit:
                continue
            reserved.append(row)
            used_sources.add(source)
            covered[facet] = row["id"]
            break
        if len(reserved) >= maximum:
            break
    reserved_ids = {row["id"] for row in reserved}
    opposite_only = set()
    requested = set(plan["facets"])
    for index, row in enumerate(rows):
        present = row_facets(row)
        if any(wanted in requested and opposite in present and wanted not in present
               for wanted, opposite in OPPOSITE.items()):
            opposite_only.add(row["id"])
    phase_ranked = [rows[index] for index in ranked if rows[index]["id"] not in opposite_only]
    revised = (reserved + [row for row in phase_ranked if row["id"] not in reserved_ids])[:limit]
    return revised, [row["id"] for row in reserved], covered


def generation_contract(plan: dict) -> str:
    facets = ", ".join(plan["facets"]) or "tema principale"
    parts = plan["request_parts"]
    checklist = "\n".join(f"- {part}" for part in parts) if parts else "- Rispondi alla richiesta esplicita."
    guidance = " ".join(FACET_GUIDANCE[facet] for facet in plan["facets"] if facet in FACET_GUIDANCE)
    return (
        "\nPIANO TATTICO OBBLIGATORIO\n"
        f"Ambiti rilevati: {facets}.\nRichieste da coprire:\n{checklist}\n"
        "Prima di scrivere, verifica internamente la copertura di ogni richiesta e non creare sezioni duplicate. "
        "Per ciascun punto formula una soluzione applicativa indicando: CHI agisce, COSA fa, DOVE, "
        "QUANDO/INNESCO, PERCHE e quale COPERTURA o rischio residuo rimane. "
        "Mantieni distinti squadra propria e avversario e non trasferire azioni tra possesso, non possesso e transizioni. "
        "Le fonti sostengono principi e fatti documentali; l'applicazione allo scenario va dichiarata come proposta tattica, "
        "senza attribuirla letteralmente alla fonte. Non usare l'assenza di una fonte identica allo scenario come motivo per "
        "omettere la soluzione: applica prudentemente i principi recuperati e segnala solo il limite specifico. "
        "Evita termini anacronistici se esiste un equivalente moderno e chiudi controllando che nessun sottopunto sia rimasto fuori. "
        + guidance
    )


def audit_answer(answer: str, plan: dict) -> dict:
    """Conservative, deterministic completeness signals; never assigns a tactical score."""
    text = normal(answer)
    facet_coverage = {
        facet: any(cue in text for cue in FACETS[facet])
        for facet in plan["facets"]
    }
    operational = {
        "who": bool(re.search(r"\b(?:portiere|terzino|braccetto|centrale|mediano|mezzala|ala|esterno|punta|centravanti|squadra|reparto)\b", text)),
        "where": any(cue in text for cue in ("spazio", "zona", "fascia", "corridoio", "area", "linea")),
        "trigger": any(cue in text for cue in ("quando", "nel momento", "se ", "alla perdita", "sul passaggio", "durante")),
        "reason": any(cue in text for cue in ("perché", "perche", "in modo da", "così da", "obiettivo", "costringe")),
        "coverage_or_risk": any(cue in text for cue in ("copertura", "preventiva", "rischio", "equilibrio", "protezione")),
    }
    missing_facets = [name for name, covered in facet_coverage.items() if not covered]
    missing_operational = [name for name, covered in operational.items() if not covered]
    return {
        "facet_coverage": facet_coverage,
        "operational_coverage": operational,
        "missing_facets": missing_facets,
        "missing_operational": missing_operational,
        "complete": not missing_facets and len(missing_operational) <= 1,
    }
