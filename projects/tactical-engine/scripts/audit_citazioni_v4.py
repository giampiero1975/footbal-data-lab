#!/usr/bin/env python3
"""Audit offline delle citazioni dei report DRIBBLING TOP 5/TOP 10.

Uso: python audit_citazioni_v4.py report.txt [output_dir]
Solo standard library. Nessun accesso a Chroma, Ollama o modelli.
L'overlap lessicale NON e' una validazione semantica.
"""
import csv
import re
import sys
from pathlib import Path

STOP = set("il lo la i gli le un uno una di a da in con su per tra fra che e ed o ma non nel nella nelle nei degli delle della dello del al allo alla alle ai agli dal dalla dalle dei come quando viene sono si sua suoi loro piu più sempre invece anche tutti tutto due tre quattro stesso stessa questo questa quelli quelle".split())
TOKEN = re.compile(r"[a-zàèéìòù0-9]+", re.I)
CIT = re.compile(r"\[(\d+)\]")
SOURCE = re.compile(r"^\[(\d+)\] id=.*$", re.M)

def tokens(text):
    return {w for w in TOKEN.findall(text.lower()) if len(w) >= 4 and w not in STOP}

def parse(text):
    blocks = re.split(r"(?m)^=== (TOP \d+) ===\s*$", text)
    if len(blocks) < 3:
        raise ValueError("Report non riconosciuto")
    for i in range(1, len(blocks), 2):
        name, body = blocks[i], blocks[i + 1]
        m = re.search(r"(?s)RISPOSTA:\s*(.*?)\s*FONTI RESTITUITE DAL CITATION ENGINE:", body)
        if not m:
            raise ValueError("RISPOSTA mancante: " + name)
        source_text = body.split("FONTI RESTITUITE DAL CITATION ENGINE:", 1)[1].split("\nCitazioni:", 1)[0]
        matches = list(SOURCE.finditer(source_text))
        sources = {}
        for j, hit in enumerate(matches):
            end = matches[j + 1].start() if j + 1 < len(matches) else len(source_text)
            chunk = source_text[hit.end():end].strip()
            sources[int(hit.group(1))] = re.sub(r"^Source \d+:\s*", "", chunk).strip()
        elapsed = re.search(r"Tempo:\s*([\d.]+)s", body)
        yield name, m.group(1), sources, float(elapsed.group(1)) if elapsed else None

def claims(answer):
    for line in answer.splitlines():
        line = re.sub(r"^\s*(?:[-*]|\d+[.)])\s*", "", line).strip()
        if CIT.search(line):
            for part in re.split(r"(?<=[.!?;])\s+(?=[A-ZÀ-Ú])", line):
                if CIT.search(part):
                    yield part

def main():
    if len(sys.argv) not in (2, 3):
        sys.exit("Uso: python audit_citazioni_v4.py report.txt [output_dir]")
    report = Path(sys.argv[1])
    output = Path(sys.argv[2]) if len(sys.argv) == 3 else report.parent
    output.mkdir(parents=True, exist_ok=True)
    rows = []
    for test, answer, sources, elapsed in parse(report.read_text(encoding="utf-8")):
        for claim in claims(answer):
            cleaned = CIT.sub("", claim).strip()
            words = tokens(cleaned)
            for ref in dict.fromkeys(int(n) for n in CIT.findall(claim)):
                source = sources.get(ref)
                if source is None:
                    status, overlap, shared = "FUORI_INTERVALLO", "", ""
                else:
                    common = words & tokens(source)
                    overlap = round(len(common) / len(words), 3) if words else 0.0
                    shared = ", ".join(sorted(common))
                    status = "DA_RIVEDERE" if overlap < 0.20 else "CONTROLLO_MANUALE"
                rows.append(dict(test=test, tempo_s=elapsed, affermazione=cleaned, citazione=ref,
                                 esito_automatico=status, overlap_lessicale=overlap,
                                 termini_in_comune=shared, testo_fonte_citata=source or ""))
    dest = output / "audit_citazioni_v4.csv"
    with dest.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]) if rows else ["test"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"{dest}: {len(rows)} associazioni")
    for test in sorted({row["test"] for row in rows}):
        subset = [row for row in rows if row["test"] == test]
        print(test, {status: sum(row["esito_automatico"] == status for row in subset)
                     for status in ("FUORI_INTERVALLO", "DA_RIVEDERE", "CONTROLLO_MANUALE")})
    print("ATTENZIONE: gli esiti sono euristici, non verifiche semantiche.")

if __name__ == "__main__":
    main()
