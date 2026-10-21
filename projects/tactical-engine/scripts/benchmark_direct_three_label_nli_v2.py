#!/usr/bin/env python3
"""Experimental v2 of direct tactical NLI; no production changes.

One isolated change: clarify the difference between an unsupported absolute
claim and a direct source contradiction. All other code and Ollama settings
are inherited from v1.

Official Ollama docs:
https://docs.ollama.com/api/chat
https://docs.ollama.com/capabilities/structured-outputs
"""
import benchmark_direct_three_label_nli_v1 as benchmark

benchmark.INSTRUCTION = """Classifica l'intera affermazione rispetto alla fonte, senza conoscenze esterne.
supported: la fonte dimostra tutta l'affermazione, inclusi sinonimi e parafrasi fedeli.
contradicted: la fonte afferma esplicitamente qualcosa di incompatibile con l'affermazione.
insufficient: la fonte non dimostra né smentisce direttamente l'affermazione.
Controlla negazioni, direzione dei confronti e quantificatori. Un numero o una garanzia non documentati non sono automaticamente falsi. Un'affermazione può omettere dettagli della fonte ed essere comunque supportata.
Regola decisiva: quando la frase contiene 'ogni', 'sempre', 'mai', 'garantisce' o 'necessariamente', NON etichettarla contradicted soltanto perché la fonte descrive un obiettivo, un vantaggio, un rischio o una possibilità senza promettere quel risultato. In quel caso scegli insufficient. Scegli contradicted solo quando la fonte presenta effettivamente una proposizione incompatibile, non quando manca la dimostrazione della certezza.
Rispondi soltanto con JSON contenente label."""

if __name__ == "__main__":
    benchmark.main()
