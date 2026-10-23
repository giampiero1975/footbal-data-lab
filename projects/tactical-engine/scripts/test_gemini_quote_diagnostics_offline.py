#!/usr/bin/env python3
"""Check citation rejection and diagnostic report persistence without network."""
import json
from pathlib import Path
import tempfile
import review_rag_v5_gemini as client

def main():
    row = {"id": "fresh_01", "mandatory_claims": [], "forbidden_claims": []}
    docs = [{"source_file_id": "source", "page": "21", "text": "La squadra cerca la riconquista della palla."}]
    review = {"id": "fresh_01", "decision": "REVISIONE", "checks": [
        {"claim": "claim", "supported": True, "evidence": [
            {"source_file_id": "source", "page": "21", "quote": "testo assente"}]}]}
    try:
        client.validate_review(review, row, docs)
    except ValueError as exc:
        assert "UNVERIFIABLE_QUOTE" in str(exc)
        assert "page=21" in str(exc)
        reason = str(exc)
    else:
        raise AssertionError("Citation gate incorrectly accepted a nonexistent quote")
    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp) / "diagnostic.json"
        client.atomic_write(output, {"status": "BLOCCATO", "raw_review": review, "reason": reason})
        saved = json.loads(output.read_text(encoding="utf-8"))
        assert saved["raw_review"] == review
        assert saved["status"] == "BLOCCATO"
    print("OFFLINE_DIAGNOSTICS_PASS API_REQUESTS=0")

if __name__ == "__main__":
    main()
