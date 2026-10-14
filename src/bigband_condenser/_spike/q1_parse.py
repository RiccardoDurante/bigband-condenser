"""Q1 - Parse integrity verification.

Verifies that music21 can parse the Kronos test case samples locally,
and that the local metrics match the cloud findings documented in
docs/pmi/KRONOS_KAI_KAIROS_FINDINGS.md v0.2.

Run from repo root:
    python src/bigband_condenser/_spike/q1_parse.py

Expected verdict: PASS (parse OK, zero errors, metrics match cloud).
"""
import sys
import warnings
from pathlib import Path

# Spike pragmatism: allow direct execution without `pip install -e .`
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from bigband_condenser._spike.common import (  # noqa: E402
    setup_logging, KRONOS_EXTRACT, KRONOS_FULL,
)

# Expected metrics from cloud FINDINGS v0.2 (sections 2 and 3)
EXPECTED_EXTRACT = {
    "parts": 19,
    "measures_part1": 33,       # pickup measure 0 + bars 1-32
    "total_notes": 1226,
}

EXPECTED_FULL = {
    "parts": 19,
    "measures_part1": 142,
    "total_notes": 6510,
    "total_rests": 2385,
}


def parse_and_measure(sample_path: Path, logger) -> dict:
    """Parse one MusicXML sample and extract key metrics."""
    from music21 import converter

    logger.info(f"Parsing: {sample_path.name}")
    logger.info(f"Size: {sample_path.stat().st_size:,} bytes")

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            score = converter.parse(str(sample_path))
            parse_ok = True
            parse_err = None
        except Exception as e:
            parse_ok = False
            parse_err = str(e)
            score = None

    result = {
        "sample": sample_path.name,
        "parse_ok": parse_ok,
        "parse_err": parse_err,
        "warnings": [str(w.message) for w in caught],
    }

    if not parse_ok:
        return result

    parts = list(score.parts)
    result["parts"] = len(parts)

    if parts:
        measures = list(parts[0].getElementsByClass("Measure"))
        result["measures_part1"] = len(measures)
        if measures:
            result["first_measure_number"] = measures[0].number
            result["last_measure_number"] = measures[-1].number

    result["total_notes"] = sum(1 for p in parts for _ in p.recurse().notes)
    result["total_rests"] = sum(
        1 for p in parts for n in p.recurse().notesAndRests if n.isRest
    )

    md = score.metadata
    if md:
        result["title"] = md.title
        result["movement"] = md.movementName
        result["composer"] = md.composer

    result["inventory"] = [
        {
            "idx": i,
            "name": p.partName or "<unnamed>",
            "notes": sum(1 for _ in p.recurse().notes),
        }
        for i, p in enumerate(parts, 1)
    ]

    return result


def compare_to_expected(result: dict, expected: dict, logger) -> bool:
    """Compare observed metrics to expected (cloud) findings. Returns True if all match."""
    all_ok = True
    for key, exp in expected.items():
        got = result.get(key)
        status = "OK" if got == exp else "MISMATCH"
        logger.info(f"  {key}: expected={exp}, got={got} [{status}]")
        if got != exp:
            all_ok = False
    return all_ok


def report(result: dict, logger) -> None:
    """Pretty-print a parse result."""
    logger.info(f"Parse OK: {result['parse_ok']}")
    if result["parse_err"]:
        logger.error(f"Parse error: {result['parse_err']}")
        return
    logger.info(f"Warnings: {len(result['warnings'])}")
    for w in result["warnings"][:3]:
        logger.info(f"  - {w[:120]}")
    logger.info(f"Parts: {result['parts']}")
    logger.info(f"Measures (part 1): {result['measures_part1']}")
    logger.info(
        f"First/Last measure number: "
        f"{result.get('first_measure_number')}/{result.get('last_measure_number')}"
    )
    logger.info(f"Total notes: {result['total_notes']}")
    logger.info(f"Total rests: {result['total_rests']}")
    logger.info(f"Movement: {result.get('movement')}")
    logger.info(f"Composer: {result.get('composer')}")
    logger.info("")
    logger.info("Parts inventory:")
    for item in result["inventory"]:
        logger.info(f"  [{item['idx']:>2}] {item['name']:<30} {item['notes']:>5} notes")


def main() -> int:
    logger = setup_logging()

    logger.info("=" * 60)
    logger.info("Q1 PARSE INTEGRITY - LOCAL VERIFICATION")
    logger.info("=" * 60)

    if not KRONOS_EXTRACT.exists():
        logger.error(f"Extract not found: {KRONOS_EXTRACT}")
        return 2

    # Primary target: extract (fast iteration)
    logger.info("")
    logger.info("--- EXTRACT (32-bar test case) ---")
    extract_result = parse_and_measure(KRONOS_EXTRACT, logger)
    logger.info("")
    report(extract_result, logger)

    if not extract_result["parse_ok"]:
        logger.error("Q1 VERDICT: FAIL - cannot parse extract")
        return 1

    logger.info("")
    logger.info("--- CLOUD-vs-LOCAL comparison (extract) ---")
    extract_match = compare_to_expected(extract_result, EXPECTED_EXTRACT, logger)

    # Secondary target: full score (sanity check)
    full_match = None
    if KRONOS_FULL.exists():
        logger.info("")
        logger.info("--- FULL SCORE (sanity check) ---")
        full_result = parse_and_measure(KRONOS_FULL, logger)
        if full_result["parse_ok"]:
            logger.info("")
            logger.info("--- CLOUD-vs-LOCAL comparison (full) ---")
            full_match = compare_to_expected(full_result, EXPECTED_FULL, logger)
        else:
            logger.warning(f"Full score parse failed: {full_result['parse_err']}")

    logger.info("")
    logger.info("=" * 60)
    all_ok = extract_match and (full_match is None or full_match)
    if all_ok:
        logger.info("Q1 VERDICT: PASS - local metrics match cloud findings")
        return 0
    else:
        logger.warning("Q1 VERDICT: MISMATCH - investigate differences")
        return 1


if __name__ == "__main__":
    sys.exit(main())
