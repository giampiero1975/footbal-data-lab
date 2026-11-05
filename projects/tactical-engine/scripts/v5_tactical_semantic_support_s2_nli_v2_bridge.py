#!/usr/bin/env python3
"""Fail-closed bridge from the injected S2 judge contract to NLI V2.

The bridge performs no inference on import or construction.  A caller supplies
the NLI V2-compatible callable; the returned callable can then be injected into
the S2 shadow adapter.  S1 remains authoritative and S2 remains non-promotable.
"""
from __future__ import annotations

import json
from dataclasses import dataclass


BRIDGE_SCHEMA = "tactical_semantic_support_s2_nli_v2_bridge_v1"
BRIDGE_VERSION = "1.0"
NLI_LABELS = {"supported", "contradicted", "insufficient"}
PAYLOAD_FIELDS = {
    "claim_id", "statement", "conditions", "polarity", "bindings",
    "evidence_ref", "evidence",
}


class BridgeContractError(ValueError):
    """The S2/NLI boundary cannot be represented without information loss."""


def _canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))


def _non_empty_string(value):
    return isinstance(value, str) and bool(value.strip())


def _validate_payload(payload):
    if not isinstance(payload, dict) or set(payload) != PAYLOAD_FIELDS:
        raise BridgeContractError("invalid_s2_judge_payload_shape")
    if not all(_non_empty_string(payload.get(key))
               for key in ("claim_id", "statement", "polarity",
                           "evidence_ref", "evidence")):
        raise BridgeContractError("invalid_s2_judge_text_field")
    if not isinstance(payload["conditions"], list):
        raise BridgeContractError("invalid_s2_judge_conditions")
    if not isinstance(payload["bindings"], dict):
        raise BridgeContractError("invalid_s2_judge_bindings")
    try:
        _canonical_json(payload["conditions"])
        _canonical_json(payload["bindings"])
    except (TypeError, ValueError) as exc:
        raise BridgeContractError("non_serializable_s2_judge_metadata") from exc


def project_claim(payload):
    """Create the exact NLI claim string without dropping S2 semantics."""
    _validate_payload(payload)
    return "\n".join((
        "S2_CLAIM_V1",
        "claim_id=" + payload["claim_id"],
        "statement=" + payload["statement"],
        "conditions_json=" + _canonical_json(payload["conditions"]),
        "polarity=" + payload["polarity"],
        "bindings_json=" + _canonical_json(payload["bindings"]),
    ))


def descriptor(nli_config):
    """Return the complete, hashable provenance descriptor consumed by S2."""
    if not isinstance(nli_config, dict):
        raise BridgeContractError("invalid_nli_v2_config")
    try:
        config = json.loads(_canonical_json(nli_config))
    except (TypeError, ValueError) as exc:
        raise BridgeContractError("non_serializable_nli_v2_config") from exc
    return {
        "kind": "injected",
        "name": "shadow-nli-v2-s2-bridge",
        "version": BRIDGE_VERSION,
        "config": {
            "bridge_schema": BRIDGE_SCHEMA,
            "nli_contract": "shadow_nli_v2_inference.judge_pair(claim,evidence)",
            "labels": sorted(NLI_LABELS),
            "rationale_mode": "bridge_trace_only_no_semantic_rationale",
            "nli_config": config,
        },
    }


def _normalise_result(result):
    if isinstance(result, str):
        label = result
        rationale = (
            "NLI V2 returned the recorded label for the exact projected "
            "claim/evidence pair; the historical contract provides no "
            "semantic rationale."
        )
    elif isinstance(result, dict) and set(result) == {"label", "rationale"}:
        label = result.get("label")
        rationale = result.get("rationale")
        if not _non_empty_string(rationale):
            raise BridgeContractError("malformed_nli_v2_rationale")
    else:
        raise BridgeContractError("malformed_nli_v2_result")
    if not isinstance(label, str) or label not in NLI_LABELS:
        raise BridgeContractError("unknown_nli_v2_label")
    return label, rationale


@dataclass(frozen=True)
class NliV2S2Bridge:
    """Callable adapter; exceptions are contained by the existing S2 boundary."""

    nli_judge: object
    judge_descriptor: dict

    def __call__(self, payload):
        if not callable(self.nli_judge):
            raise BridgeContractError("invalid_nli_v2_judge")
        claim = project_claim(payload)
        evidence = payload["evidence"]
        label, rationale = _normalise_result(self.nli_judge(claim, evidence))
        return {"label": label, "rationale": rationale}


def build_bridge(nli_judge, nli_config):
    """Build an inert bridge and its descriptor for explicit S2 injection."""
    if not callable(nli_judge):
        raise BridgeContractError("invalid_nli_v2_judge")
    judge_descriptor = descriptor(nli_config)
    return NliV2S2Bridge(nli_judge, judge_descriptor)
