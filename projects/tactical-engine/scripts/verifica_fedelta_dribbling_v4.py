#!/usr/bin/env python3
"""Audit documentale della risposta TOP 10, senza modificare indici o modelli."""
from pathlib import Path
import re
import time
from llama_index.llms.ollama import Ollama

BASE = Path('/opt/football-data-lab/projects/tactical-engine')
INPUT = BASE / 'risposte_v4_top5_top10.txt'
OUTPUT = BASE / 'audit_fedelta_v4_top10.txt'


def main():
    report = INPUT.read_text(encoding='utf-8')
    match = re.search(r'(?ms)^=== TOP 10 ===\s*\n(.*?)(?=^=== TOP \d+ ===|\Z)', report)
    if not match:
        raise RuntimeError('Sezione TOP 10 non trovata nel report.')
    section = match.group(1)
    answer_match = re.search(r'(?s)\nRISPOSTA:\s*\n(.*?)\nFONTI RESTITUITE DAL CITATION ENGINE:', section)
    sources_match = re.search(r'(?s)\nFONTI RESTITUITE DAL CITATION ENGINE:\s*\n(.*?)(?:\nCitazioni:|\Z)', section)
    if not answer_match or not sources_match:
        raise RuntimeError('Formato report inatteso: risposta o fonti non individuate.')
    answer = answer_match.group(1).strip()
    sources = sources_match.group(1).strip()
    print(f'Risposta: {len(answer)} caratteri | Fonti: {len(sources)} caratteri', flush=True)

    prompt = f'''Sei un revisore documentale rigoroso di analisi tattica calcistica.
Devi VERIFICARE una risposta rispetto alle fonti, non riscriverla e non aggiungere conoscenze esterne.
Considera le FONTI come unica verità documentale. Distingui sempre la nostra metà campo da quella avversaria.

Compiti:
1. Scomponi la risposta in affermazioni tattiche verificabili. Per ciascuna indica SUPPORTATA, CONTRADDETTA o NON VERIFICABILE, il numero della fonte e una breve citazione TESTUALE che motivi il giudizio. Non inventare citazioni.
2. Controlla in particolare chi possiede la palla e DOVE: nostra zona difensiva, centrocampo, zona d'attacco, zona difensiva avversaria. Segnala qualunque inversione.
3. Controlla se sono coperti i tre elementi: (a) centrocampisti esterni larghi con palla nella nostra zona difensiva; (b) ampiezza dei reparti con palla a centrocampo; (c) profondità e ampiezza degli attaccanti laterali con corse diagonali.
4. Verifica che i numeri di citazione della risposta corrispondano davvero alle fonti pertinenti, non solo che esistano.
5. Chiudi con un verdetto: IDONEA oppure DA CORREGGERE; elenca solo le correzioni necessarie, con il testo originale e quello corretto.
Non assumere che la risposta sia giusta. Se non puoi verificare un dettaglio, scrivi NON VERIFICABILE.

RISPOSTA DA VERIFICARE:
{answer}

FONTI NUMERATE:
{sources}

AUDIT DOCUMENTALE IN ITALIANO:
'''
    llm = Ollama(model='qwen3.5:9b', base_url='http://127.0.0.1:11434',
                 request_timeout=900.0, temperature=0.0, context_window=8192,
                 thinking=False)
    print('Audit Qwen3.5 in corso (CPU): potrebbe richiedere alcuni minuti...', flush=True)
    start = time.monotonic()
    audit = str(llm.complete(prompt))
    elapsed = time.monotonic() - start
    content = (f'AUDIT FEDELTA DRIBBLING V4 TOP 10\nTempo: {elapsed:.1f}s\n'
               f'Origine: {INPUT}\n\n{audit}\n\n'
               'NOTA: audit automatico sperimentale, NON garanzia di correttezza. '
               'Le contestazioni vanno confermate sulle fonti originali.\n')
    OUTPUT.write_text(content, encoding='utf-8')
    print(content, flush=True)
    print(f'Report salvato: {OUTPUT}', flush=True)


if __name__ == '__main__':
    main()
