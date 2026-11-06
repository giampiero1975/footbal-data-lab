#!/usr/bin/env python3
"""Fail-closed Spatial V1 bridge for the non-authoritative S2 adapter.

Construction validates declared provenance but does not authenticate the
injected Python callable.  The runner is responsible for the explicit binding.
Import and construction are inert: inference occurs only when the bridge is
called by S2.
"""
from __future__ import annotations

import copy
import json
from dataclasses import dataclass

from v5_tactical_semantic_support_s2_nli_v2_bridge import (
    BridgeContractError,
    NLI_LABELS,
    project_claim,
)


BRIDGE_SCHEMA = "tactical_semantic_support_s2_spatial_v1_bridge_v1"
BRIDGE_VERSION = "1.0"
BRIDGE_NAME = "shadow-nli-spatial-v1-s2-bridge"
DECLARED_CALLABLE = "shadow_nli_spatial_relations_v1_inference.judge_pair"
CONTRACT_ID = "nli_spatial_relations_v1"
CONTRACT_VERSION = "1.0"
BASE_CONTRACT = "shadow_nli_v2_inference"
INSTRUCTION_SHA256 = (
    "sha256:861dbec3daac9ac34169356ad51a453f6267175afaa5d296f84c92586d2f3a00"
)
CONTRACT_LABELS = ["supported", "contradicted", "insufficient"]
CONTRACT_KEYS = {
    "contract_id", "version", "base_contract", "labels",
    "instruction_sha256", "selection",
}
CONFIG_KEYS = {
    "judge", "model", "ollama_url", "timeout_seconds_per_call",
    "max_tokens", "temperature", "num_ctx", "think", "retry", "repair",
}
EXPECTED_CONFIG = {
    "judge": DECLARED_CALLABLE,
    "model": "qwen3.5:9b",
    "ollama_url": "http://127.0.0.1:11434",
    "timeout_seconds_per_call": 180,
    "max_tokens": 1024,
    "temperature": 0,
    "num_ctx": 4096,
    "think": False,
    "retry": False,
    "repair": False,
}
TECHNICAL_NOTICE = (
    "Adapter-generated technical provenance notice (not verdict rationale): "
    "the injected Spatial V1 judge returned only a label; no semantic "
    "rationale was provided by the model."
)


def _canonical_copy(value, error_code):
    try:
        return json.loads(json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    except (TypeError, ValueError) as exc:
        raise BridgeContractError(error_code) from exc


def _validate_contract_descriptor(value):
    if not isinstance(value, dict) or set(value) != CONTRACT_KEYS:
        raise BridgeContractError("invalid_spatial_contract_descriptor_shape")
    descriptor = _canonical_copy(
        value, "non_serializable_spatial_contract_descriptor")
    expected = {
        "contract_id": CONTRACT_ID,
        "version": CONTRACT_VERSION,
        "base_contract": BASE_CONTRACT,
        "labels": CONTRACT_LABELS,
        "instruction_sha256": INSTRUCTION_SHA256,
        "selection": "explicit_import_only",
    }
    if descriptor != expected:
        raise BridgeContractError("inconsistent_spatial_contract_descriptor")
    return descriptor


def _validate_nli_config(value):
    if not isinstance(value, dict) or set(value) != CONFIG_KEYS:
        raise BridgeContractError("invalid_spatial_nli_config_shape")
    config = _canonical_copy(value, "non_serializable_spatial_nli_config")
    type_rules = {
        "judge": str,
        "model": str,
        "ollama_url": str,
        "timeout_seconds_per_call": int,
        "max_tokens": int,
        "temperature": int,
        "num_ctx": int,
        "think": bool,
        "retry": bool,
        "repair": bool,
    }
    if any(type(config.get(key)) is not expected_type
           for key, expected_type in type_rules.items()):
        raise BridgeContractError("invalid_spatial_nli_config_type")
    if config != EXPECTED_CONFIG:
        raise BridgeContractError("inconsistent_spatial_nli_config")
    return config


def descriptor(nli_config, contract_descriptor):
    """Return exact declared provenance; callable authenticity is not claimed."""
    config = _validate_nli_config(nli_config)
    contract = _validate_contract_descriptor(contract_descriptor)
    return {
        "kind": "injected",
        "name": BRIDGE_NAME,
        "version": BRIDGE_VERSION,
        "config": {
            "bridge_schema": BRIDGE_SCHEMA,
            "declared_callable_identity": DECLARED_CALLABLE,
            "runtime_callable_authentication": "not_performed_by_bridge",
            "binding_evidence": "explicit_spatial_runner_import_and_closure",
            "contract": contract,
            "labels": list(CONTRACT_LABELS),
            "label_provenance": "canonical_spatial_v1_judge_output",
            "rationale_mode": (
                "adapter_generated_technical_notice_not_verdict_rationale"
            ),
            "nli_config": config,
        },
    }


def _normalise_result(result):
    if not isinstance(result, str) or result not in NLI_LABELS:
        raise BridgeContractError("malformed_spatial_v1_result")
    return {"label": result, "rationale": TECHNICAL_NOTICE}


@dataclass(frozen=True)
class SpatialV1S2Bridge:
    """Callable adapter with immutable internal declared provenance."""

    nli_judge: object
    _descriptor: dict

    @property
    def judge_descriptor(self):
        return copy.deepcopy(self._descriptor)

    def __call__(self, payload):
        claim = project_claim(payload)
        evidence = payload["evidence"]
        return _normalise_result(self.nli_judge(claim, evidence))


def build_bridge(nli_judge, nli_config, contract_descriptor):
    """Build an inert Spatial V1 bridge without inference."""
    if not callable(nli_judge):
        raise BridgeContractError("invalid_spatial_v1_judge")
    judge_descriptor = descriptor(nli_config, contract_descriptor)
    return SpatialV1S2Bridge(nli_judge, copy.deepcopy(judge_descriptor))
