#!/usr/bin/env python3
"""Frozen pilot question set for RAG V5 quality gate; no gold labels yet."""
import argparse
import json
from pathlib import Path

QUESTIONS = [
    ("holdout_01", "Quali compiti difensivi distinguono marcatura a uomo e marcatura a zona nelle situazioni di copertura?"),
    ("holdout_02", "Come deve adattarsi il sostegno al portatore quando la squadra tenta di creare superiorità numerica?"),
    ("holdout_03", "Quali fattori condizionano la scelta tra costruzione dal portiere e costruzione dai difensori?"),
    ("holdout_04", "Quali movimenti coordinati favoriscono la creazione di linee di passaggio nella manovra offensiva?"),
    ("holdout_05", "Quali principi aiutano a mantenere equilibrio difensivo mentre si sviluppa un attacco?"),
    ("holdout_06", "Come cambiano le priorità della transizione positiva a seconda della zona di recupero della palla?"),
    ("holdout_07", "Confronta i principi di ampiezza e profondità nella progressione offensiva, distinguendo quando le fonti non danno indicazioni."),
    ("holdout_08", "Quali rischi di copertura emergono quando gli esterni partecipano contemporaneamente alla fase offensiva?"),
    ("holdout_09", "Che cosa consentono di affermare le fonti sul cambio di modulo a partita in corso e che cosa invece non documentano?"),
    ("holdout_10", "Come organizzare la prima giocata dopo la riconquista della palla senza confondere transizione positiva e possesso consolidato?")
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if len(QUESTIONS) != 10 or len({row[0] for row in QUESTIONS}) != 10:
        parser.error("Invalid questions")
    report = {
        "schema": "rag_v5_quality_holdout_pilot_questions_v1",
        "status": "frozen_candidate_not_gold",
        "caveat": "Novel wording drafted from project themes, not independently adjudicated; verify novelty and source answerability before calling this a validated holdout.",
        "questions": [{"id": qid, "question": question} for qid, question in QUESTIONS]
    }
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print("FROZEN_CANDIDATE", len(QUESTIONS), args.output)

if __name__ == "__main__":
    main()
