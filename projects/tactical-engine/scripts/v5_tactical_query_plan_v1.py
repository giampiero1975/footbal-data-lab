#!/usr/bin/env python3
"""Deterministic tactical question planning and evidence diversification.

The module is deliberately model-free: it extracts the requested tactical
facets, builds bounded retrieval queries and reserves evidence covering
different facets.  It never writes to the index and contains no benchmark IDs.
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

try:
    from v5_tactical_state_contract_v1 import build_question_plan
except ModuleNotFoundError:  # Support direct importlib loading used by offline tests.
    _contract_spec = importlib.util.spec_from_file_location(
        "v5_tactical_state_contract_v1", Path(__file__).with_name("v5_tactical_state_contract_v1.py"))
    _contract_module = importlib.util.module_from_spec(_contract_spec)
    _contract_spec.loader.exec_module(_contract_module)
    build_question_plan = _contract_module.build_question_plan


FACETS = {
    "possession": ("fase di possesso", "costruzione", "sviluppo", "rifinitura", "attacco", "offensivo", "palla nostra"),
    "non_possession": ("fase di non possesso", "blocco", "difesa", "difendere", "scivolamento", "sotto-blocco", "fuorigioco"),
    "negative_transition": ("transizione negativa", "perdita", "riaggressione", "contro-pressing", "ripiegamento"),
    "positive_transition": ("transizione positiva", "riconquista", "contropiede", "ripartenza"),
    "prevention": ("preventiv", "seconda palla", "equilibrio"),
    "goalkeeper": ("portiere", "estremo difensore"),
    "third_man": ("terzo uomo", "3° uomo"),
    "width": ("ampiezza", "corsia laterale", "cambio gioco", "cambio di gioco", "lato debole"),
    "inside_space": ("rifinitura", "tra le linee", "half-space", "corridoio interno", "interspazio"),
    "box": ("area di rigore", "primo palo", "secondo palo", "dischetto", "fuori area", "cross"),
    "offside": ("fuorigioco", "palla scoperta", "palla libera", "palla coperta"),
    "substitutions": ("sostituz", "cambio di sistema", "cambi di sistema", "gestione del risultato"),
    "communication": ("comunicazione", "comando", "leader", "segnale"),
    "psychology": ("emotiv", "psicolog", "pressione della gara"),
    "five_lanes": ("cinque corridoi", "5 corridoi", "cinque canali", "5 canali"),
    "relational_superiority": ("superiorità socio-affettiva", "superiorita socio-affettiva", "superiorità posizionale", "superiorita posizionale"),
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
    "goalkeeper": "Se la domanda riguarda la costruzione, spiega come il portiere crea superiorità, orienta il pressing e sceglie tra uscita corta e soluzione oltre pressione. Se riguarda un cross, definisci invece chiamata, zona d'uscita e ripartizione palla-uomo-porta con i difensori.",
    "third_man": "Rendi esplicita la sequenza portatore-appoggio-terzo uomo, lo spazio liberato e il tempo del movimento.",
    "width": "Distingui lato palla e lato debole, usa il tempo di volo del cambio gioco per scivolare e accorciare, e descrivi il nuovo lato forte senza aprire il corridoio interno.",
    "inside_space": "Distingui la fascia orizzontale di rifinitura dai corridoi verticali interni e specifica postura e smarcamento del ricevente.",
    "box": "Distingui attacco e difesa del cross. In attacco mappa primo palo, zona centrale/dischetto, secondo palo e limite area; in difesa definisci postura semiaperta, visione palla-uomo, contatto, protezione porta e competenza del portiere.",
    "offside": "Distingui palla coperta e scoperta: su palla scoperta la priorità è scappare e proteggere profondità, non salire alla cieca. Se descrivi una trappola, separa gioco aperto e palla inattiva e specifica leader, comando, istante del calcio e rischio alle spalle.",
    "substitutions": "Per ogni cambio indica giocatore/ruolo che esce ed entra, nuova struttura, compito concreto e rischio compensato; non limitarti a dire che entra il giocatore piu adatto.",
    "communication": "Indica chi comunica, con quale comando o canale e in quale momento della gara. Non proporre video come canale operativo durante il gioco.",
    "psychology": "Collega l'impatto emotivo a un comportamento osservabile e a una comunicazione concreta, non a formule astratte.",
    "five_lanes": "Nomina e occupa esplicitamente i cinque corridoi verticali: fascia, half-space, centro, half-space e fascia; collega la linea avanzata alla struttura residua 2+3 o 3+2.",
    "relational_superiority": "Distingui superiorità posizionale da relazione socio-affettiva: vicinanze, conoscenza reciproca, appoggi e combinazioni coordinate.",
}

REQUIRED_DETAILS = {
    "negative_transition": {
        "density_or_proximity": ("densità", "prossimità", "vicini"),
        "covered_or_uncovered_ball": ("palla coperta", "palla scoperta"),
        "field_zone": ("zona", "campo"),
        "preventive_structure": ("preventiv",),
    },
    "five_lanes": {
        "five_lane_geometry": ("cinque corridoi", "5 corridoi", "fascia", "half-space"),
        "residual_structure": ("2+3", "3+2", "struttura residua"),
    },
    "substitutions": {
        "players_in_out": ("esce", "entra", "sostit"),
        "new_structure": ("struttura", "sistema", "modulo"),
    },
    "goalkeeper": {
        "goalkeeper_decision": ("portiere", "uscita", "oltre pressione"),
    },
    "third_man": {
        "third_man_sequence": ("terzo uomo", "portatore", "appoggio"),
    },
    "width": {
        "strong_and_weak_side": ("lato debole", "lato forte"),
        "ball_flight_trigger": ("tempo di volo", "palla viaggia"),
    },
    "inside_space": {
        "between_lines_receiving": ("tra le linee", "alle spalle", "orientato"),
        "next_action": ("scarico", "inserimento", "attacca la linea", "attacco della linea"),
    },
    "box": {
        "box_roles": ("primo palo", "secondo palo", "dischetto", "limite area", "palla-uomo"),
    },
    "offside": {
        "covered_uncovered_choice": ("palla coperta", "palla scoperta"),
        "leader_command": ("comando", "leader", "chiama"),
        "open_vs_restart": ("palla inattiva", "punizione", "gioco aperto"),
    },
    "communication": {
        "live_communication": ("comando", "comandi", "parola", "parole", "gesto", "gesti", "segnale", "segnali"),
    },
    "psychology": {
        "observable_psychology": ("ansia", "fiducia", "responsabil", "chiarezza", "sicurezza"),
    },
}

DETAIL_QUERIES = {
    "negative_transition": "transizione negativa riaggressione ripiegamento palla coperta palla scoperta marcatura preventiva densita zona perdita",
    "goalkeeper": "portiere costruzione superiorita pressione uscita corta palla lunga oppure portiere cross chiamata uscita difensori",
    "third_man": "terzo uomo portatore appoggio pressione uomo su uomo liberare spazio",
    "width": "cambio gioco tempo di volo lato debole lato forte scivolamento mediano schermo",
    "inside_space": "rifinitura tra le linee ricezione orientata scarico inserimento attacco linea difensiva",
    "box": "cross attacco area primo palo dischetto secondo palo limite area oppure difesa palla uomo portiere",
    "offside": "fuorigioco palla coperta scoperta gioco aperto palla inattiva comando leader postura profondita",
    "substitutions": "cambio sistema in gara giocatore esce entra compiti comunicazione equilibrio transizione",
}

SCENARIOS = {
    "build_out": ("costruzione dal basso", "pressing alto"),
    "cross_defence": ("protezione della porta", "cross"),
    "lateral_shift": ("scivolamento", "cambio gioco"),
    "counterpress_deadline": ("contro-pressing", "tempo massimo"),
    "between_lines": ("zona di rifinitura", "tra la linea difensiva"),
    "cross_attack": ("primo palo", "secondo palo", "dischetto"),
    "offside_trap": ("trappola del fuorigioco", "palla inattiva"),
    "game_management": ("sostituzioni", "ultimi 15 minuti"),
}

SCENARIO_GUIDANCE = {
    "build_out": "Non abbassare genericamente il baricentro: descrivi portiere uomo libero, attrazione della prima pressione, smarcamento opposto dell'appoggio e del terzo uomo, uscita oltre pressione e soluzione lunga preparata con struttura per la seconda palla. Resta nella costruzione dal basso: non introdurre cross, primo/secondo palo o occupazioni dell'area offensiva.",
    "cross_defence": "Descrivi marcatura a uomo nella zona: difensore lato porta, distanza di contatto, postura semiaperta per vedere palla e uomo, attacco del punto di caduta e chiamata del portiere; evita numeri di maglia rigidi non ricavati dallo scenario.",
    "lateral_shift": "Il tempo di volo del cambio gioco serve per traslare lateralmente, non per scappare all'indietro: il nuovo quarto/quinto lato forte esce sul ricevente, il lato debole stringe, il mediano resta distinto e scherma l'imbucata, le linee mantengono distanze corte. Non attribuire al quarto/quinto il compito del mediano.",
    "counterpress_deadline": "Distingui uomo e linee di passaggio, mantieni una preventiva aggressiva dietro la pressione e indica una finestra operativa breve di circa 5-6 secondi; se viene superata o la palla e scoperta, interrompi e scappa in blocco.",
    "between_lines": "Il ricevente si smarca alle spalle del centrocampo avversario con corpo aperto; dopo la ricezione deve scegliere tra girarsi e attaccare la linea, giocare a muro/scarico per il terzo uomo o liberare un inserimento in profondita.",
    "cross_attack": "Assegna quattro occupazioni distinte: primo palo, zona centrale/dischetto, secondo palo e limite area per raccogliere la respinta e garantire preventiva. Collega il cross a un segnale del portatore, non a una coreografia automatica; non usare numeri di maglia se assenti dalla domanda.",
    "offside_trap": "Correzione vincolante: su palla scoperta in gioco aperto la linea scappa e protegge profondita; la salita e ammessa solo su palla coperta o gesto tecnico leggibile. Su palla inattiva la linea concordata sale all'istante del calcio, comandata da un leader, con portiere pronto alla profondita.",
    "game_management": "Fornisci almeno un esempio completo e coerente di trasformazione: indica un cambio ruolo senza sostituzione oppure, per ogni sostituzione realmente proposta, chi esce e chi entra. Nel passaggio 4-3-3 a 3-5-2 usa questa geometria applicativa senza numeri di maglia: un'ala esce e un difensore centrale entra; i tre centrali compongono la linea, i due terzini si alzano da quinti, l'ala rimasta stringe accanto al centravanti e i tre centrocampisti restano nel reparto. Non trasformare terzini o centrocampisti in ruoli incompatibili. Descrivi protezione delle seconde palle e messaggio semplice dato prima dell'ingresso. Non inventare tre cambi generici e non usare il video come comunicazione live.",
}

SCENARIO_DETAILS = {
    "build_out": {
        "goalkeeper_spare_man": ("uomo libero", "superiorità"),
        "third_man_escape": ("terzo uomo",),
        "long_exit_and_second_ball": ("palla lunga", "oltre pressione", "seconda palla"),
    },
    "cross_defence": {
        "body_orientation": ("semiapert", "palla e uomo", "palla-uomo"),
        "contact_distance": ("contatto", "braccio", "distanza"),
        "landing_point": ("punto di caduta", "traiettoria"),
        "goalkeeper_call": ("chiama", "chiamata", "mia"),
    },
    "lateral_shift": {
        "flight_time": ("tempo di volo", "palla viaggia"),
        "new_strong_side": ("lato forte",),
        "weak_side_squeeze": ("lato debole", "stringe"),
        "midfielder_screen": ("mediano", "schermo", "imbucata"),
    },
    "counterpress_deadline": {
        "man_vs_lane": ("orientato sull'uomo", "linee di passaggio"),
        "preventive_defenders": ("preventiv", "difensori rimasti"),
        "five_six_seconds": ("5 second", "6 second", "5-6 second", "cinque second", "sei second"),
    },
    "between_lines": {
        "open_body": ("corpo aperto", "orientato"),
        "attack_or_layoff": ("attacca la linea", "attacco diretto", "scarico", "a muro"),
        "runner": ("inserimento", "terzo uomo"),
    },
    "cross_attack": {
        "first_post": ("primo palo",),
        "penalty_spot": ("dischetto", "zona centrale"),
        "far_post": ("secondo palo",),
        "edge_of_box": ("limite area", "fuori area"),
        "cross_signal": ("testa alta", "segnale", "tempo del cross", "portatore"),
    },
    "offside_trap": {
        "uncovered_ball_drop": ("palla scoperta", "scappa"),
        "covered_ball_step": ("palla coperta", "sale", "salita"),
        "restart_kick_moment": ("istante del calcio", "momento del calcio", "palla inattiva"),
        "leader_and_keeper": ("leader", "portiere"),
    },
    "game_management": {
        "concrete_role_change": ("esce", "entra", "scala", "si abbassa", "si alza"),
        "transition_balance": ("seconda palla", "profondità", "preventiv"),
        "live_message": ("comando", "comandi", "parola", "parole", "gesto", "gesti", "messaggio"),
        "emotional_effect": ("fiducia", "chiarezza", "sicurezza", "ansia", "responsabil"),
    },
}

SCENARIO_ANCHORS = {
    "build_out": ("terzo uomo", "portiere"),
    "cross_defence": ("punto di caduta", "postura del corpo"),
    "lateral_shift": ("punto critico è il tempo di volo", "difendente lontano deve valutare"),
    "counterpress_deadline": ("regola dei cinque secondi", "entro i 6 secondi", "marcatura preventiva"),
    "between_lines": ("tra le linee", "terzo uomo"),
    "cross_attack": ("primo palo", "secondo palo", "dischetto"),
    "offside_trap": ("la difesa innanzitutto scappa", "durante il tragitto della palla"),
    "game_management": ("cambio del sistema di gioco", "comunicazione efficace"),
}


def normal(value: str) -> str:
    return re.sub(r"\s+", " ", value.casefold().replace("–", "-").replace("—", "-")).strip()


def relation_requirements(plan: dict) -> list[dict]:
    """Build conservative subproblem envelopes without prescribing solutions."""
    phase_terms = {
        "possession": ["in possesso", "fase offensiva"],
        "non_possession": ["non possesso", "fase difensiva"],
        "negative_transition": ["transizione negativa", "alla perdita"],
        "positive_transition": ["transizione positiva", "alla riconquista"],
    }
    explicit_phases = []
    for facet in plan.get("facets", []):
        explicit_phases.extend(phase_terms.get(facet, []))
    requirements = []
    for index, part in enumerate(plan.get("request_parts", [])):
        required = ["actor", "task", "space", "trigger", "purpose"]
        item = {
            "requirement_id": f"question_part:{index}",
            "question_part": part,
            "required_dimensions": required,
        }
        phases_in_part = [term for term in explicit_phases if term in normal(part)]
        if phases_in_part:
            item["required_dimensions"] = ["actor", "phase", "task", "space", "trigger", "purpose"]
            item["phase_terms"] = phases_in_part
        actor_terms = [cue for cue in RELATION_DIMENSION_CUES["actor"] if cue in normal(part)]
        task_terms = [cue for cue in RELATION_DIMENSION_CUES["task"] if cue in normal(part)]
        if actor_terms:
            item["actor_terms"] = actor_terms
        if task_terms:
            item["task_terms"] = task_terms
        item["specificity"] = "explicit_relation" if actor_terms and task_terms else "underspecified"
        requirements.append(item)
    return requirements


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
    scenarios = [name for name, cues in SCENARIOS.items() if all(cue in query for cue in cues)]
    plan = {
        "question_text": query,
        "facets": facets,
        "scenarios": scenarios,
        "formations": formations,
        "roles": roles,
        "request_parts": request_parts[:8],
    }
    plan["state_contract"] = build_question_plan(
        question, formations=formations, roles=roles, scenarios=scenarios)
    plan["relation_requirements"] = relation_requirements(plan)
    return plan


def retrieval_queries(question: str, plan: dict, maximum: int = 5) -> list[str]:
    """Return the original question plus bounded, facet-specific expansions."""
    queries = [" ".join(question.split())]
    context = " ".join(plan["formations"] + plan["roles"][:5])
    scenario_queries = {
        "build_out": "costruzione dal basso portiere uomo libero terzo uomo uscita pressione seconda palla",
        "cross_defence": "difesa porta cross postura palla uomo contatto punto caduta chiamata portiere",
        "lateral_shift": "cambio gioco tempo volo scivolamento lato debole forte mediano schermo imbucata",
        "counterpress_deadline": "contropressing uomo linee passaggio marcatura preventiva cinque sei secondi ripiegamento",
        "between_lines": "rifinitura tra linee corpo aperto attacco linea scarico terzo uomo inserimento",
        "cross_attack": "cambio gioco uno contro uno cross primo palo dischetto secondo palo limite area segnale",
        "offside_trap": "fuorigioco palla coperta salita palla scoperta scappare punizione istante calcio leader portiere",
        "game_management": "cambio sistema gara ruoli entra esce comunicazione fiducia preventive seconde palle",
    }
    for scenario in plan.get("scenarios", []):
        candidate = f"{scenario_queries[scenario]} {context}".strip()
        if candidate not in queries:
            queries.append(candidate)
        if len(queries) >= maximum:
            return queries
    priority = [name for name in plan["facets"] if name in DETAIL_QUERIES]
    priority.extend(name for name in plan["facets"] if name not in priority)
    for facet in priority:
        cues = DETAIL_QUERIES.get(facet) or " ".join(FACETS[facet][:4])
        candidate = f"{cues} {context}".strip()
        if candidate and candidate not in queries:
            queries.append(candidate)
        if len(queries) >= maximum:
            break
    return queries


def retrieval_anchors(plan: dict, maximum: int = 4) -> list[str]:
    """Return bounded exact phrases used only to widen the candidate pool."""
    anchors = []
    for scenario in plan.get("scenarios", []):
        for anchor in SCENARIO_ANCHORS.get(scenario, ()):
            if anchor not in anchors:
                anchors.append(anchor)
            if len(anchors) >= maximum:
                return anchors
    return anchors


def reserve_anchor_candidates(rows: list[dict], scores, selected: list[dict],
                              candidate_ids: list[str], limit: int, maximum: int = 3):
    """Reserve the best exact-anchor candidates without bypassing reranking."""
    allowed = set(candidate_ids)
    ranked = sorted(
        (i for i, row in enumerate(rows) if row["id"] in allowed),
        key=lambda i: float(scores[i]), reverse=True,
    )
    reserved = []
    used_sources = set()
    for index in ranked:
        row = rows[index]
        source = row.get("source")
        if source in used_sources:
            continue
        reserved.append(row)
        used_sources.add(source)
        if len(reserved) >= maximum:
            break
    reserved_ids = {row["id"] for row in reserved}
    return (reserved + [row for row in selected if row["id"] not in reserved_ids])[:limit], sorted(reserved_ids)


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
    guidance += " " + " ".join(SCENARIO_GUIDANCE[name] for name in plan.get("scenarios", []))
    mandatory = []
    question_text = plan.get("question_text", "")
    for facet in plan["facets"]:
        details = REQUIRED_DETAILS.get(facet, {})
        for name in details:
            if name == "ball_flight_trigger" and not any(
                    cue in question_text for cue in ("cambio gioco", "tempo di volo", "palla viaggia")):
                continue
            if name in ("between_lines_receiving", "next_action") and not any(
                    cue in question_text for cue in ("tra le linee", "successiv", "dopo la ricezione", "attacco diretto")):
                continue
            if name == "box_roles" and not any(
                    cue in question_text for cue in ("riempimento", "attacco del primo palo", "dischetto", "secondo palo")):
                continue
            mandatory.append(name)
    for scenario in plan.get("scenarios", []):
        mandatory.extend(SCENARIO_DETAILS.get(scenario, {}).keys())
    mandatory_text = ", ".join(dict.fromkeys(mandatory)) or "copertura integrale della domanda"
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
        "Non mostrare nomi tecnici del controllo interno, non aggiungere una sezione di verifica e non assegnare numeri di maglia se lo scenario non li fornisce. "
        f"Il controllo finale deve verificare esplicitamente: {mandatory_text}. "
        "I seguenti requisiti specifici sono obbligatori, non suggerimenti. Mantieni l'intera risposta entro 420 parole, "
        "accorpa i criteri in una matrice o in punti compatti e non ripetere la stessa griglia per concetti equivalenti: " + guidance
    )


RELATION_DIMENSION_CUES = {
    "actor": ("portiere", "terzino", "braccetto", "centrale", "difensore", "mediano",
              "mezzala", "ala", "esterno", "punta", "centravanti", "squadra", "reparto"),
    "phase": ("in possesso", "non possesso", "transizione negativa", "transizione positiva",
              "alla perdita", "alla riconquista", "fase offensiva", "fase difensiva"),
    "task": ("scivola", "stringe", "esce", "copre", "proteg", "accorc", "marca", "pressa", "scherm", "attacca",
             "si abbassa", "si alza", "accompagna", "intercetta", "raddoppia", "fissa"),
    "space": ("fascia", "corridoio", "half-space", "interspazio", "area", "linea", "profondità",
              "secondo palo", "primo palo", "limite area", "zona palla", "lato debole"),
    "trigger": ("quando", "se ", "nel momento", "alla perdita", "alla riconquista", "sul passaggio",
                "palla coperta", "palla scoperta", "al cambio gioco"),
    "purpose": ("perché", "perche", "in modo da", "così da", "per evitare", "per impedire",
                "per proteggere", "per creare", "costringe", "consente", "riduce il rischio"),
}


def _relation_clauses(answer: str) -> list[dict]:
    """Extract clause-local signals without inferring missing tactical links."""
    clauses = []
    raw_clauses = [raw for raw in re.split(r"[.;\n]+", answer) if raw.strip()]
    for index, raw in enumerate(raw_clauses):
        text = normal(raw)
        if not text:
            continue
        dimensions = {
            name: [cue for cue in cues if cue in text]
            for name, cues in RELATION_DIMENSION_CUES.items()
        }
        clauses.append({
            "clause_id": f"clause:{index}",
            "text": text,
            "dimensions": dimensions,
            "citations": sorted(set(re.findall(r"\[(F\d+)\]", raw, re.I))),
        })
    base = list(clauses)
    for index in range(len(base) - 1):
        second = base[index + 1]["text"]
        if not re.match(r"^(?:in questo modo|cos[iì]|questo|questa|tale)\b", second):
            continue
        combined_text = base[index]["text"] + ". " + second
        clauses.append({
            "clause_id": f"window:{index}-{index + 1}",
            "text": combined_text,
            "dimensions": {
                name: [cue for cue in cues if cue in combined_text]
                for name, cues in RELATION_DIMENSION_CUES.items()
            },
            "citations": sorted(set(base[index]["citations"] + base[index + 1]["citations"])),
        })
    return clauses


def _task_is_negated(text: str, task_terms: list[str]) -> bool:
    for term in task_terms:
        for match in re.finditer(re.escape(term), text):
            prefix = text[max(0, match.start() - 35):match.start()]
            if re.search(r"\bnon\b(?:\s+\w+){0,3}\s*$", prefix):
                return True
    return False


def _actor_task_linked(text: str, actor_terms: list[str], task_terms: list[str]) -> bool:
    """Conservatively require the requested actor to be the nearest actor before the task."""
    if not actor_terms or not task_terms:
        return False
    actors = []
    for cue in RELATION_DIMENSION_CUES["actor"]:
        actors.extend((match.start(), cue) for match in re.finditer(r"\b" + re.escape(cue) + r"\b", text))
    for term in task_terms:
        for task in re.finditer(re.escape(term), text):
            preceding = [(position, cue) for position, cue in actors if position < task.start()]
            if not preceding:
                continue
            _, nearest = max(preceding)
            if any(expected in nearest or nearest in expected for expected in actor_terms):
                return True
    return False


def audit_relations(answer: str, requirements: list[dict] | None = None,
                    evidence: list[dict] | None = None) -> dict:
    """Non-blocking relational diagnosis, independent from the legacy gate.

    A requirement is satisfied only when its required dimensions and explicit
    constraints occur in the same clause.  The function never assigns a score,
    repairs text, or changes ``audit_answer(...)["complete"]``.
    """
    requirements = requirements or []
    evidence = evidence or []
    clauses = _relation_clauses(answer)
    evidence_by_id = {str(item.get("id", "")).upper(): item for item in evidence}
    results = []
    for index, requirement in enumerate(requirements):
        required = requirement.get("required_dimensions") or ["actor", "phase", "task"]
        constraints = {
            dimension: [normal(term) for term in requirement.get(f"{dimension}_terms", [])]
            for dimension in RELATION_DIMENSION_CUES
        }
        candidates = []
        rejected_negation = False
        rejected_association = False
        specified = bool(constraints.get("actor") and constraints.get("task"))
        for clause in clauses:
            present = {name: bool(values) for name, values in clause["dimensions"].items()}
            constraint_matches = {
                name: (not terms or any(term in clause["text"] for term in terms))
                for name, terms in constraints.items()
            }
            if not all(present.get(name, False) and constraint_matches.get(name, True) for name in required):
                continue
            if not specified:
                continue
            if _task_is_negated(clause["text"], constraints["task"]):
                rejected_negation = True
                continue
            if not _actor_task_linked(clause["text"], constraints["actor"], constraints["task"]):
                rejected_association = True
                continue
            candidates.append(clause)
        matched = candidates[0] if candidates else None
        issue_codes = []
        if not matched:
            issue_codes.append("relation_not_demonstrated")
            if not specified:
                issue_codes.append("requirement_underspecified")
            if rejected_negation:
                issue_codes.append("required_relation_negated")
            if rejected_association:
                issue_codes.append("actor_task_link_not_demonstrated")
            task_terms = constraints.get("task", [])
            task_clauses = [item for item in clauses if task_terms and any(term in item["text"] for term in task_terms)]
            if task_clauses:
                actor_terms = constraints.get("actor", [])
                phase_terms = constraints.get("phase", [])
                if actor_terms and any(item["dimensions"]["actor"] and
                                       not any(term in item["text"] for term in actor_terms)
                                       for item in task_clauses):
                    issue_codes.append("wrong_actor_for_task")
                if phase_terms and any(item["dimensions"]["phase"] and
                                       not any(term in item["text"] for term in phase_terms)
                                       for item in task_clauses):
                    issue_codes.append("wrong_phase_for_task")
        citation_status = "not_applicable"
        if matched and matched["citations"]:
            valid = [evidence_by_id.get(item.upper()) for item in matched["citations"]]
            if any(item is None for item in valid):
                citation_status = "invalid_id"
                issue_codes.append("invalid_citation_id")
            else:
                relevance_terms = [normal(term) for term in requirement.get("evidence_terms", [])]
                relevant = not relevance_terms or any(
                    any(term in normal(" ".join((str(item.get("topic", "")), str(item.get("text", "")))))
                        for term in relevance_terms) for item in valid
                )
                citation_status = "formally_valid_relevant" if relevant else "formally_valid_but_irrelevant"
                if not relevant:
                    issue_codes.append("citation_tactically_irrelevant")
        results.append({
            "requirement_id": requirement.get("requirement_id", f"requirement:{index}"),
            "satisfied": bool(matched),
            "matched_clause_id": matched["clause_id"] if matched else None,
            "issue_codes": issue_codes,
            "citation_status": citation_status,
            "semantic_support_verified": False,
        })
    return {
        "schema": "tactical_relational_audit_v1",
        "mode": "offline_non_blocking",
        "requirements": results,
        "all_relations_demonstrated": bool(results) and all(item["satisfied"] for item in results),
        "clauses_examined": len(clauses),
        "affects_legacy_gate": False,
    }


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
        "reason": any(cue in text for cue in ("perché", "perche", "in modo da", "così da", "obiettivo", "costringe",
                                                   "serve a", "consente", "evita", "riduce", "impedisce", "garantisce")),
        "coverage_or_risk": any(cue in text for cue in ("copertura", "preventiva", "rischio", "equilibrio", "protezione")),
    }
    missing_facets = [name for name, covered in facet_coverage.items() if not covered]
    missing_operational = [name for name, covered in operational.items() if not covered]
    detail_coverage = {}
    question_text = plan.get("question_text", "")
    for facet in plan["facets"]:
        for name, alternatives in REQUIRED_DETAILS.get(facet, {}).items():
            if name == "ball_flight_trigger" and not any(
                    cue in question_text for cue in ("cambio gioco", "tempo di volo", "palla viaggia")):
                continue
            if name in ("between_lines_receiving", "next_action") and not any(
                    cue in question_text for cue in ("tra le linee", "successiv", "dopo la ricezione", "attacco diretto")):
                continue
            if name == "box_roles" and not any(
                    cue in question_text for cue in ("riempimento", "attacco del primo palo", "dischetto", "secondo palo")):
                continue
            if name == "covered_or_uncovered_ball":
                detail_coverage[name] = bool(re.search(r"palla.{0,18}(?:coperta|scoperta)", text))
            else:
                detail_coverage[name] = any(term in text for term in alternatives)
    for scenario in plan.get("scenarios", []):
        for name, alternatives in SCENARIO_DETAILS.get(scenario, {}).items():
            detail_coverage[name] = any(term in text for term in alternatives)
    if "offside_trap" in plan.get("scenarios", []):
        detail_coverage["uncovered_ball_drop"] = "palla scoperta" in text and "scapp" in text
        detail_coverage["covered_ball_step"] = "palla coperta" in text and any(term in text for term in ("sale", "salita"))
        detail_coverage["leader_and_keeper"] = "leader" in text and "portiere" in text
    semantic_issues = []
    clauses = [normal(part) for part in re.split(r"[.;\n]+", answer) if part.strip()]
    if any("palla coperta" in clause and re.search(r"\b(?:scapp|arretr)", clause)
           and not re.search(r"\b(?:sale|salita|risal)", clause) for clause in clauses):
        semantic_issues.append("covered_ball_mapped_to_drop")
    if any("palla scoperta" in clause and re.search(r"\b(?:sale|salita|risal)", clause)
           and not re.search(r"\b(?:scapp|arretr)", clause) for clause in clauses):
        semantic_issues.append("uncovered_ball_mapped_to_step")
    if "counterpress_deadline" in plan.get("scenarios", []):
        if re.search(r"(?:contro-?pressing|attacco spazio).{0,80}\(possesso\)|principio.{0,80}\(possesso\)", text):
            semantic_issues.append("counterpress_labelled_as_possession")
        if re.search(r"densit.{0,80}(?:cede|cedere|deve cedere)", text):
            semantic_issues.append("defensive_density_must_yield")
    if "cross_attack" in plan.get("scenarios", []) and re.search(
            r"\bin difesa\b|postura semiaperta|difesa del cross", text):
        semantic_issues.append("cross_attack_contaminated_by_defensive_phase")
    if re.search(r"\b(?:goalkeeper_decision|third_man_sequence|box_roles|next_action|between_lines_receiving|transition_balance|emotional_effect|field_zone|live_message|density_or_proximity)\b", text):
        semantic_issues.append("internal_audit_labels_exposed")
    if re.search(r"\b(?:n[.°]?\s*|numero\s+|giocatore\s+|#)(?:2|3|4|5|6|7|8|9|10|11)\b", text) and not re.search(
            r"\b(?:n[.°]?\s*|numero\s+|giocatore\s+|#)(?:2|3|4|5|6|7|8|9|10|11)\b", question_text):
        semantic_issues.append("unsupported_rigid_player_numbers")
    if re.search(r"\b(?:es\.?|ad esempio)\s*(?:il\s+)?(?:n[.°]?\s*)?(?:2|3|4|5|6|7|8|9|10|11)\b", text) and not re.search(
            r"\b(?:es\.?|ad esempio)\s*(?:il\s+)?(?:n[.°]?\s*)?(?:2|3|4|5|6|7|8|9|10|11)\b", question_text):
        if "unsupported_rigid_player_numbers" not in semantic_issues:
            semantic_issues.append("unsupported_rigid_player_numbers")
    if "build_out" in plan.get("scenarios", []) and re.search(
            r"\b(?:cross|primo palo|secondo palo|dischetto)\b", text):
        semantic_issues.append("build_out_contaminated_by_cross_attack")
    if "lateral_shift" in plan.get("scenarios", []) and re.search(
            r"scivol\w*\s+(?:all'indietro|indietro)|ripiegamento verticale", text):
        semantic_issues.append("lateral_shift_mapped_to_vertical_drop")
    if "lateral_shift" in plan.get("scenarios", []) and re.search(
            r"(?:quarto|quinto).{0,90}(?:scherm|spazio di imbucata|davanti alla difesa)", text):
        semantic_issues.append("wide_defender_given_midfielder_screen")
    if "cross_attack" in plan.get("scenarios", []) and re.search(
            r"limite (?:dell['’]?)?area.{0,70}evitare tiri da fuori", text):
        semantic_issues.append("edge_of_box_role_inverted")
    if "game_management" in plan.get("scenarios", []) and re.search(
            r"(?:scambio|sostituzione) simultane[oa] di tre|tre giocatori.{0,50}tre riserve", text):
        semantic_issues.append("generic_triple_substitution")
    if "game_management" in plan.get("scenarios", []) and re.search(
            r"(?:due\s+)?esterni difensivi.{0,80}centrocampisti centrali", text):
        semantic_issues.append("incoherent_role_transformation")
    if plan.get("scenarios") and len(text.split()) < 150:
        semantic_issues.append("complex_answer_too_short")
    missing_details = [name for name, covered in detail_coverage.items() if not covered]
    return {
        "facet_coverage": facet_coverage,
        "operational_coverage": operational,
        "missing_facets": missing_facets,
        "missing_operational": missing_operational,
        "detail_coverage": detail_coverage,
        "missing_details": missing_details,
        "semantic_issues": semantic_issues,
        "relational_audit": audit_relations(
            answer, plan.get("relation_requirements"), plan.get("audit_evidence")),
        "complete": not missing_facets and len(missing_operational) <= 1 and not missing_details and not semantic_issues,
    }
