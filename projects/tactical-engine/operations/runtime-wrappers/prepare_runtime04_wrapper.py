"""Materialize a separate local artifact; never execute either wrapper."""
from pathlib import Path
import difflib
import hashlib

ROOT = Path(__file__).resolve().parent
ORIGINAL = ROOT / "spatial-v2-extraction-locator-q3-04-runtime-03.original.sh"
OUTPUT = ROOT / "spatial-v2-extraction-locator-q3-04-runtime-04.sh"
DIFF = ROOT / "runtime03-to-runtime04.diff"
ORIGINAL_SHA256 = "ba0160e0381bbe5242196a555ab5e85ae0109c0b383bc9a79825c14b4fd44d57"
BASELINE = "13814c20d80bca4d9cb4cb08a288b6e7b31dac0d"

OLD_BRANCH = """    # --------------------------------------------------------------
    # E2. Extraction strutturalmente valida
    # --------------------------------------------------------------

    else:
"""
NEW_BRANCH = """    # --------------------------------------------------------------
    # E1b. Shape valido, precontrollo semantico fallito prima del locator
    # --------------------------------------------------------------

    elif (semantic_errors := extraction_contract.extraction_semantic_errors(
        extraction
    )):
        require(
            evaluation_status == "not_evaluable",
            "semantic-invalid extraction was promoted",
        )
        require(
            reason_codes == ["E_EXTRACTION_SEMANTIC_INCONSISTENT"],
            "semantic-invalid extraction reason code invalid",
        )
        require(
            result.get("details") == semantic_errors,
            "semantic diagnostics differ from precheck errors",
        )
        require(result.get("witness") is None, "semantic failure has witness")
        require(result.get("validation") is None, "semantic failure has validation")
        require(not witness_present, "semantic failure has witness artifact")
        require(not validation_present, "semantic failure has validation artifact")
        provenance = require_diagnostic_provenance(result, claim, evidence)
        require(
            provenance.get("records") == [],
            "semantic failure unexpectedly has localization records",
        )
        require(
            not extraction_contract.verify_materialization(
                result, extraction, claim, evidence
            ),
            "semantic failure materialization/provenance mismatch",
        )
        require(
            observed_label is None and semantic_match is None,
            "semantic failure has observed label or semantic match",
        )
        localization_status = provenance.get("status")
        classification = "fail_closed_extraction_semantic"

    # --------------------------------------------------------------
    # E2. Shape e precontrollo semantico validi
    # --------------------------------------------------------------

    else:
"""

REPLACEMENTS = (
    ("db3ad66f6254f43bcc625b605b68f2f181c1af69", BASELINE, 1),
    ("spatial-v2-extraction-locator-db3ad66", "spatial-v2-dual-blocker-13814c2", 1),
    ("spatial-v2-extraction-locator-q3-04-runtime-03", "spatial-v2-extraction-locator-q3-04-runtime-04", 3),
    ("df9a7fb494956902e8af91860cab176c768992a2", "8ac93d07341e1079ee3ca6ff98327a8391b7ab5f", 1),
    ("97a666672c3a38897ff9570b03a4a749d32d0ead", "1a64827b26fb30758773049eedeb342a2bb826b2", 1),
    (OLD_BRANCH, NEW_BRANCH, 1),
)


def adapted_bytes(original):
    if len(original) != 45964 or hashlib.sha256(original).hexdigest() != ORIGINAL_SHA256:
        raise ValueError("original identity mismatch")
    text = original.decode("utf-8")
    for old, new, count in REPLACEMENTS:
        if text.count(old) != count:
            raise ValueError("unexpected replacement count: " + old)
        text = text.replace(old, new)
    return text.encode("utf-8")


def main():
    if OUTPUT.exists() or DIFF.exists():
        raise FileExistsError("output/diff already exists; no overwrite")
    before = ORIGINAL.read_bytes()
    after = adapted_bytes(before)
    difference = "".join(difflib.unified_diff(
        before.decode().splitlines(keepends=True),
        after.decode().splitlines(keepends=True),
        fromfile=ORIGINAL.name, tofile=OUTPUT.name,
    )).encode("utf-8")
    with OUTPUT.open("xb") as f:
        f.write(after)
    with DIFF.open("xb") as f:
        f.write(difference)
    assert ORIGINAL.read_bytes() == before
    print("original_bytes=" + str(len(before)))
    print("original_sha256=" + hashlib.sha256(before).hexdigest())
    print("runtime04_bytes=" + str(len(after)))
    print("runtime04_sha256=" + hashlib.sha256(after).hexdigest())
    print("diff_sha256=" + hashlib.sha256(difference).hexdigest())


if __name__ == "__main__":
    main()
