#!/usr/bin/env python3
"""Explicit-only Spatial V2 judge; importing this module is inert."""
from __future__ import annotations

import json
import urllib.error
import urllib.request

from v5_tactical_semantic_support_s2_spatial_v2 import (
    CONTRACT_ID, CONTRACT_VERSION, SPATIAL_V2_SCHEMA, validate_spatial_v2,
)
from v5_tactical_semantic_support_s2_spatial_v2_extraction import (
    EXTRACTION_SCHEMA, boundary_failure as extraction_boundary_failure,
    descriptor as extraction_contract_descriptor,
    materialize_extraction, extraction_handoff_instructions,
)


INSTRUCTION = """Classifica l'affermazione rispetto alla sola fonte e restituisci un relation witness conforme a nli_spatial_relations_v2 2.0.0. Ancora ogni componente esplicito esclusivamente al testo originale del rispettivo claim o evidence. Gli offset sono indici Unicode code-point zero-based in intervalli semiaperti [start,end): start incluso, end escluso. Deve valere esattamente e con confronto case-sensitive source_text[start:end] == exact_span. Non usare offset del prompt completo, token del modello o byte UTF-8; non stimare, approssimare, normalizzare o correggere gli offset e non inventare span assenti. Per un quantificatore grammaticale non osservato usa {\"status\":\"implicit\",\"value\":\"none\",\"literal\":null,\"anchors\":[]}; la sentinella distinta è {\"status\":\"absent\",\"value\":\"absent\",\"literal\":null,\"anchors\":[]}. Un quantificatore explicit usa un valore non sentinella e diverso da none, con 1-2 anchor testuali; literal è null salvo numeric, che richiede un literal non vuoto. ambiguous usa value=ambiguous, literal=null e 1-2 anchor; unknown usa value=unknown, literal=null e nessun anchor. È vietato {\"status\":\"explicit\",\"value\":\"absent\",\"literal\":\"\",\"anchors\":[]}. Non rendere intercambiabili sentinelle e stati. Non inventare equivalenze: compatible per soggetto o referente è una dichiarazione shadow, non una verifica indipendente. La label deve essere coerente con il witness. Il witness deve rispettare sia lo schema JSON sia tutti i vincoli deterministici del contratto: JSON sintatticamente valido non implica witness strutturalmente valido. Rispondi soltanto con JSON conforme allo schema."""

EXTRACTION_INSTRUCTION = extraction_handoff_instructions()


DEFAULT_TIMEOUT_SECONDS = 180
Q3_04_DIAGNOSTIC_TIMEOUT_SECONDS = 360


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


def extraction_descriptor():
    return {
        **extraction_contract_descriptor(),
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


def build_extraction_prompt(claim, evidence):
    if type(claim) is not str or not claim:
        raise ValueError("claim must be a non-empty string")
    if type(evidence) is not str or not evidence:
        raise ValueError("evidence must be a non-empty string")
    return (EXTRACTION_INSTRUCTION + "\n\nFONTE:\n" + evidence +
            "\n\nAFFERMAZIONE:\n" + claim)


def _default_transport(url, payload, timeout):
    request = urllib.request.Request(
        url.rstrip("/") + "/api/chat",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def _not_evaluable(code, *, witness=None, validation=None):
    diagnostic = validation or {
        "validator_id": "nli_spatial_relations_v2_judge_boundary",
        "validator_version": "1.0.0",
        "technical_status": "not_evaluable",
        "derived_label": None,
        "model_label": None,
        "comparison_verified": False,
        "semantic_compatibility_verified": False,
        "error_codes": [code],
    }
    return {
        "evaluation_status": "not_evaluable",
        "label": None,
        "witness": witness,
        "validation": diagnostic,
        "promotion_authorized": False,
    }


def judge_pair(claim, evidence, *, model="qwen3.5:9b",
               ollama_url="http://127.0.0.1:11434",
               timeout=DEFAULT_TIMEOUT_SECONDS, max_tokens=2048,
               transport=None, q3_04_timeout_360=False,
               extraction_locator=False):
    """Perform exactly one transport call, then validate the returned witness."""
    if type(extraction_locator) is not bool:
        raise TypeError("extraction_locator must be boolean")
    prompt = (build_extraction_prompt(claim, evidence) if extraction_locator
              else build_prompt(claim, evidence))
    if type(q3_04_timeout_360) is not bool:
        raise TypeError("q3_04_timeout_360 must be boolean")
    effective_timeout = (Q3_04_DIAGNOSTIC_TIMEOUT_SECONDS
                         if q3_04_timeout_360 else timeout)
    payload = {
        "model": model, "stream": False, "think": False,
        "format": EXTRACTION_SCHEMA if extraction_locator else SPATIAL_V2_SCHEMA,
        "options": {"temperature": 0, "num_predict": max_tokens, "num_ctx": 4096},
        "messages": [
            {"role": "system", "content": "Rispondi soltanto con JSON conforme allo schema."},
            {"role": "user", "content": prompt},
        ],
    }
    call = transport or _default_transport
    try:
        result = call(ollama_url, payload, effective_timeout)
    except TimeoutError:
        if extraction_locator:
            return extraction_boundary_failure(
                "E_JUDGE_TIMEOUT", claim_text=claim, evidence_text=evidence)
        return _not_evaluable("E_JUDGE_TIMEOUT")
    except (ConnectionError, urllib.error.URLError, OSError):
        if extraction_locator:
            return extraction_boundary_failure(
                "E_JUDGE_TRANSPORT", claim_text=claim, evidence_text=evidence)
        return _not_evaluable("E_JUDGE_TRANSPORT")
    if type(result) is not dict or result.get("done_reason") != "stop":
        if extraction_locator:
            return extraction_boundary_failure(
                "E_JUDGE_RESPONSE_INCOMPLETE", claim_text=claim,
                evidence_text=evidence)
        return _not_evaluable("E_JUDGE_RESPONSE_INCOMPLETE")
    message = result.get("message")
    content = message.get("content") if type(message) is dict else None
    if type(content) is not str or not content:
        if extraction_locator:
            return extraction_boundary_failure(
                "E_JUDGE_RESPONSE_MISSING", claim_text=claim,
                evidence_text=evidence)
        return _not_evaluable("E_JUDGE_RESPONSE_MISSING")
    try:
        witness = json.loads(content)
    except json.JSONDecodeError:
        if extraction_locator:
            return extraction_boundary_failure(
                "E_JUDGE_JSON_INVALID", claim_text=claim,
                evidence_text=evidence)
        return _not_evaluable("E_JUDGE_JSON_INVALID")
    if extraction_locator:
        return materialize_extraction(witness, claim, evidence)
    validation = validate_spatial_v2(witness, claim, evidence)
    if validation["technical_status"] != "valid":
        return _not_evaluable("E_WITNESS_INVALID", witness=witness,
                              validation=validation)
    return {
        "evaluation_status": "evaluated",
        "label": witness["label"],
        "witness": witness,
        "validation": validation,
        "promotion_authorized": False,
    }
