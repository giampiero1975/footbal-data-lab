#!/usr/bin/env python3
"""Opt-in NLI contract for inverse spatial/relational predicates.

This experimental judge is inert on import and is not wired into S2, RAG, API,
or panel routing.  It reuses the historical NLI V2 output schema and parser only
when ``judge_pair`` is called explicitly.
"""
from __future__ import annotations

import hashlib
import json
import urllib.request


CONTRACT_ID = "nli_spatial_relations_v1"
CONTRACT_VERSION = "1.0"
BASE_CONTRACT = "shadow_nli_v2_inference"
LABELS = ("supported", "contradicted", "insufficient")

INSTRUCTION = """Classifica l'intera affermazione rispetto alla sola fonte, senza conoscenze esterne.
supported: la fonte dimostra tutta l'affermazione, inclusi sinonimi e parafrasi fedeli.
contradicted: la fonte afferma esplicitamente qualcosa di incompatibile con l'affermazione.
insufficient: la fonte non dimostra né smentisce direttamente l'affermazione.
Prima di scegliere la label, confronta separatamente soggetto della relazione, proprietà o spazio considerato, riferimento spaziale, direzione della relazione, condizioni, contesto ed eventuale fase o tempo di gioco.
Se soggetto, referente e condizioni coincidono e fonte e affermazione descrivono predicati semanticamente incompatibili sulla stessa relazione, scegli contradicted anche senza una negazione grammaticale esplicita. Sono esempi di direzioni incompatibili, a parità di referente e contesto: lasciare molto spazio rispetto a togliere spazio; aumentare rispetto a ridurre una distanza; avanzare rispetto ad arretrare; ampliare rispetto a restringere la stessa zona. Questi esempi definiscono il principio e non sono una blacklist lessicale.
Se soggetto, referente, condizioni, fase o direzione non sono sufficientemente determinabili, oppure la fonte tace sulla relazione, scegli insufficient: la semplice assenza di conferma non è una contraddizione.
La presenza di parole comuni tra fonte e affermazione non costituisce supporto. Scegli supported soltanto quando la fonte sostiene effettivamente l'intera affermazione.
Controlla inoltre negazioni e quantificatori. Un numero o una garanzia non documentati non sono automaticamente falsi. Quando la frase contiene ogni, sempre, mai, garantisce o necessariamente, non scegliere contradicted soltanto perché la fonte descrive un obiettivo, vantaggio, rischio o possibilità senza promettere il risultato; in quel caso scegli insufficient, salvo una proposizione esplicitamente incompatibile.
Rispondi soltanto con JSON contenente label."""


def instruction_sha256():
    return "sha256:" + hashlib.sha256(INSTRUCTION.encode("utf-8")).hexdigest()


def descriptor():
    return {
        "contract_id": CONTRACT_ID,
        "version": CONTRACT_VERSION,
        "base_contract": BASE_CONTRACT,
        "labels": list(LABELS),
        "instruction_sha256": instruction_sha256(),
        "selection": "explicit_import_only",
    }


def build_prompt(claim, evidence):
    if not isinstance(claim, str) or not claim.strip():
        raise ValueError("claim must be a non-empty string")
    if not isinstance(evidence, str) or not evidence.strip():
        raise ValueError("evidence must be a non-empty string")
    return INSTRUCTION + "\n\nFONTE:\n" + evidence + "\n\nAFFERMAZIONE:\n" + claim


def judge_pair(claim, evidence, *, model="qwen3.5:9b",
               ollama_url="http://127.0.0.1:11434", timeout=180,
               max_tokens=1024):
    """Run the opt-in contract; importing this module never contacts Ollama."""
    # Lazy reuse preserves V2 as the canonical source of schema and parsing
    # while keeping this experimental module importable in offline mock tests.
    from shadow_nli_v2_inference import SCHEMA, Verdict

    prompt = build_prompt(claim, evidence)
    payload = {
        "model": model, "stream": False, "think": False, "format": SCHEMA,
        "options": {"temperature": 0, "num_predict": max_tokens,
                    "num_ctx": 4096},
        "messages": [
            {"role": "system", "content":
             "Rispondi esclusivamente con JSON conforme allo schema richiesto. Non aggiungere testo esterno."},
            {"role": "user", "content": prompt},
        ],
    }
    request = urllib.request.Request(
        ollama_url.rstrip("/") + "/api/chat",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        result = json.load(response)
    message = result.get("message") or {}
    content = message.get("content") or ""
    if result.get("done_reason") != "stop" or not content:
        raise RuntimeError("Ollama output incomplete")
    return Verdict.model_validate_json(content).label
