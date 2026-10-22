#!/usr/bin/env python3
"""Experimental V3 instruction on the same 11 NLI shadow controls.

Does not modify the canonical V2 prompt, RAG, Chroma or production.
Ollama API: https://docs.ollama.com/api/chat
Structured outputs: https://docs.ollama.com/capabilities/structured-outputs
"""
import sys
from pathlib import Path
import shadow_nli_v2_inference as inference
import benchmark_shadow_nli_v2_adversarial as benchmark

V3_INSTRUCTION = """Classifica l'INTERA affermazione rispetto alla SOLA fonte.
supported: ogni proposizione della frase e' dimostrata dalla fonte, inclusi sinonimi fedeli.
contradicted: la fonte sostiene esplicitamente una proposizione incompatibile con la frase.
insufficient: la fonte non dimostra l'intera frase e non contiene una incompatibilita' esplicita.
Per frasi composte: se una parte e' supportata e un'altra non e' documentata, scegli insufficient; se una parte e' esplicitamente incompatibile, scegli contradicted.
Confronta attentamente condizioni, preferenze, negazioni, direzione del confronto e contesto. Se la fonte raccomanda A anziche' B NELLA STESSA CONDIZIONE e la frase raccomanda B anziche' A, scegli contradicted: e' una contraddizione di preferenza, anche se entrambe le opzioni sono teoricamente possibili.
Non generalizzare da un insieme specifico a tutti i casi possibili. Se la fonte descrive tre sistemi e la frase dice tutti i sistemi, senza controesempio esplicito scegli insufficient, NON contradicted.
Non interpretare un rischio o una possibilita' come una garanzia. Parole come sempre, mai, ogni, necessariamente, garantisce richiedono prova esplicita; se assente scegli insufficient, salvo controesempio esplicito.
Usa solo la fonte, non conoscenze esterne. Rispondi esclusivamente con JSON contenente label."""

def main():
    inference.load_v2_instruction = lambda: V3_INSTRUCTION
    benchmark.judge_pair = inference.judge_pair
    if "--output" not in sys.argv:
        sys.argv.extend(["--output", str(Path("projects/tactical-engine/evaluation/reports/rag_v5_shadow_adversarial_v3_20261022.json"))])
    benchmark.main()

if __name__ == "__main__":
    main()
