"""Q5 - Transpose tag preservation in music21 output.

Verifies that the output file produced by Q4 Experiment 3 (strip hidden + filter)
preserves correct <transpose> tags for all transposing instruments.

Checks EFFECTIVE transposition (chromatic + 12 * octave-change) rather than the raw
representation, because music21 may serialize differently from the source Finale
(e.g. "chromatic=-14, octave-change=0" vs "chromatic=-2, octave-change=-1" are both
valid for a Tenor Sax -M9).

Also verifies R24 (music21 bug: omitted <transpose> for parts sharing same instrument
class). On Finale input, music21 sees WRONG classes (R26) so parts are seen as different
classes - R24 may not manifest. We check empirically.
"""
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from bigband_condenser._spike.common import setup_logging  # noqa: E402

OUT_FILE = Path(__file__).resolve().parent / "_tmp" / "q4_exp3_filtered.musicxml"

# Expected EFFECTIVE transposition in semitones. None = no tag expected (concert instrument).
EXPECTED_EFFECTIVE = {
    "Soprano Sax": -2,
    "Alto Sax": -9,
    "Tenor Sax 1": -14,
    "Tenor Sax 2": -14,
    "Baritone Sax": -21,
    "Trumpet in Bb 1": -2,
    "Trumpet in Bb 2": -2,
    "Trumpet in Bb 3": -2,
    "Trumpet in Bb 4": -2,
    "Horn in F 1": -7,
    "Horn in F 2": -7,
    "Trombone": None,
    "Bass Trombone": None,
    "Electric Guitar": -12,
    "Piano": None,
    "Acoustic Bass": -12,
}


def extract_transpose_tags(xml_path):
    tree = ET.parse(str(xml_path))
    root = tree.getroot()
    id_to_name = {}
    for sp in root.findall(".//score-part"):
        pid = sp.get("id")
        pn = sp.find("part-name")
        if pid and pn is not None and pn.text:
            id_to_name[pid] = pn.text

    results = []
    for part in root.findall("part"):
        pid = part.get("id")
        name = id_to_name.get(pid, "<?>")
        found = None
        first_measure = part.find("measure")
        if first_measure is not None:
            attrs = first_measure.find("attributes")
            if attrs is not None:
                tr = attrs.find("transpose")
                if tr is not None:
                    chrom = tr.find("chromatic")
                    oc = tr.find("octave-change")
                    chrom_v = int(chrom.text) if chrom is not None and chrom.text else 0
                    oc_v = int(oc.text) if oc is not None and oc.text else 0
                    found = {"chromatic": chrom_v, "octave_change": oc_v, "effective": chrom_v + 12 * oc_v}
        results.append({"id": pid, "name": name, "found": found})
    return results


def main():
    logger = setup_logging()
    logger.info("=" * 70)
    logger.info("Q5 TRANSPOSE TAG PRESERVATION IN OUTPUT")
    logger.info("=" * 70)

    if not OUT_FILE.exists():
        logger.error(f"Q4 Exp 3 output not found: {OUT_FILE}")
        return 2

    logger.info(f"Checking: {OUT_FILE.name}")
    results = extract_transpose_tags(OUT_FILE)

    logger.info("")
    logger.info(f"{'ID':<6}{'Part':<22}{'Tag (c, oc, eff)':<24}{'Expected':<10}{'Verdict':<16}")
    logger.info("-" * 78)

    failures = []
    for r in results:
        name = r["name"]
        found = r["found"]
        expected = EXPECTED_EFFECTIVE.get(name)

        if expected is None:
            if found is None or found["effective"] == 0:
                verdict = "OK (no/identity)"
            else:
                verdict = "UNEXPECTED TAG"
                failures.append(name)
        else:
            if found is None:
                verdict = "MISSING TAG"
                failures.append(name)
            elif found["effective"] == expected:
                verdict = "OK"
            else:
                verdict = f"MISMATCH {found['effective']} vs {expected}"
                failures.append(name)

        tag_str = (
            f"c={found['chromatic']}, oc={found['octave_change']}, eff={found['effective']}"
            if found else "(none)"
        )
        exp_str = str(expected) if expected is not None else "None"
        logger.info(f"{r['id']:<6}{name[:21]:<22}{tag_str[:23]:<24}{exp_str:<10}{verdict:<16}")

    logger.info("")
    logger.info("=" * 70)
    if not failures:
        logger.info("Q5 VERDICT: PASS - all transpose tags preserved correctly")
        logger.info("  R24 did NOT manifest on this file (likely because music21 sees different (wrong) classes per part, see R26).")
        return 0
    else:
        logger.warning(f"Q5 VERDICT: FAIL - {len(failures)} issues: {failures}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
