#!/usr/bin/env python3
"""DRIBBLING V4 - Test di ragionamento tattico applicato."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import test_prompt_fedelta_dribbling_v4_corretto as v4

OriginalOllama = v4.Ollama

class ThinkingOllama(OriginalOllama):
    def __init__(self, *args, **kwargs):
        kwargs["thinking"] = True
        kwargs["context_window"] = 16384
        kwargs["request_timeout"] = 1800.0
        super().__init__(*args, **kwargs)

v4.Ollama = ThinkingOllama

v4.QUESTION = (
    "Nel 3-3-4 di Glerean, una squadra fatica a sviluppare "
    "l'azione offensiva perché, quando il pallone si trova "
    "nella propria zona difensiva, i giocatori si concentrano "
    "centralmente e manca ampiezza. Analizza il problema "
    "secondo i principi documentati di Glerean. "
    "Quali giocatori devono muoversi, dove e come? "
    "Distingui i comportamenti nelle diverse zone del campo. "
    "Proponi correzioni pratiche, distinguendo chiaramente "
    "i principi documentati dalle tue deduzioni tattiche. "
    "Non inventare indicazioni attribuite a Glerean."
)

sys.argv = [
    sys.argv[0],
    "--output",
    "/opt/football-data-lab/projects/tactical-engine/"
    "test_ragionamento_thinking_16k_timeout_v4.txt",
]

v4.main()
