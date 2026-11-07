#!/usr/bin/env python3
"""Explicit-only Spatial V2 judge; importing this module is inert."""
from __future__ import annotations

import json
import urllib.request

from v5_tactical_semantic_support_s2_spatial_v2 import (
    CONTRACT_ID, CONTRACT_VERSION, SPATIAL_V2_SCHEMA, validate_spatial_v2,
)


INSTRUCTION = """Classifica l'affermazione rispetto alla sola fonte e restituisci un relation witness conforme a nli_spatial_relations_v2 2.0.0. Ancora ogni componente esplicito al testo originale. Non inventare equivalenze: compatible per soggetto o referente e una dichiarazione shadow, non una verifica indipendente. La label deve essere coerente con il witness. Rispondi soltanto con JSON conforme allo schema."""


def descriptor():
    return {
        "contract_id": CONTRACT_ID,
        "version": CONTRACT_VERSION,
        "selection": "explicit_import_only",
        "single_generation": True,
        "retry": False,
        "repair": False,
        "fallback": False,
    }


def build_prompt(claim, evidence):
    if type(claim) is not str or not claim:
        raise ValueError("claim must be a non-empty string")
    if type(evidence) is not str or not evidence:
        raise ValueError("evidence must be a non-empty string")
    return INSTRUCTION + "\n\nFONTE:\n" + evidence + "\n\nAFFERMAZIONE:\n" + claim


def _default_transport(url, payload, timeout):
    request = urllib.request.Request(
        url.rstrip("/") + "/api/chat",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def judge_pair(claim, evidence, *, model="qwen3.5:9b",
               ollama_url="http://127.0.0.1:11434", timeout=180,
               max_tokens=2048, transport=None):
    """Perform exactly one transport call, then validate the returned witness."""
    prompt = build_prompt(claim, evidence)
    payload = {
        "model": model, "stream": False, "think": False,
        "format": SPATIAL_V2_SCHEMA,
        "options": {"temperature": 0, "num_predict": max_tokens, "num_ctx": 4096},
        "messages": [
            {"role": "system", "content": "Rispondi soltanto con JSON conforme allo schema."},
            {"role": "user", "content": prompt},
        ],
    }
    call = transport or _default_transport
    result = call(ollama_url, payload, timeout)
    if type(result) is not dict or result.get("done_reason") != "stop":
        raise RuntimeError("spatial_v2_output_incomplete")
    message = result.get("message")
    content = message.get("content") if type(message) is dict else None
    if type(content) is not str or not content:
        raise RuntimeError("spatial_v2_output_missing")
    try:
        witness = json.loads(content)
    except json.JSONDecodeError as exc:
        raise RuntimeError("spatial_v2_output_not_json") from exc
    validation = validate_spatial_v2(witness, claim, evidence)
    if validation["technical_status"] != "valid":
        return {
            "evaluation_status": "not_evaluable",
            "label": None,
            "witness": witness,
            "validation": validation,
            "promotion_authorized": False,
        }
    return {
        "evaluation_status": "evaluated",
        "label": witness["label"],
        "witness": witness,
        "validation": validation,
        "promotion_authorized": False,
    }
