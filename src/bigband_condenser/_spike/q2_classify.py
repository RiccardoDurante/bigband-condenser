"""Q2 - Instrument classification via partName string matching + hidden parts detection.

Classifies each XML part into one of the 4 Charter sections (Reeds/Brass/Rhythm/Drums)
by pattern-matching on the `partName` string.

Rationale (from cloud FINDINGS v0.2 section 3): music21 `part.getInstruments()` returns
WRONG classes on Finale exports. We bypass this by relying on textual `partName`.

HIDDEN PARTS detection (session 2026-10-15 finding, candidate R28):
Finale allows marking a staff as "hidden" (used for playback-only MIDI parts not shown
in the printed score). Marker in MusicXML: `<staff-details print-object="no"/>` without
`number` attribute, in the first measure's `<attributes>`. These parts must be EXCLUDED
from the condensed output: they contain playback data, not notational intent.

Example in Kronos: "Drum Set 2" (P18) is hidden; it carries realistic MIDI playback
for the drummer whose notational part lives in the visible "Drum Set 1" (P17).

Also computes logical instrument count by grouping XML parts with identical partName.

Run from repo root:
    python src/bigband_condenser/_spike/q2_classify.py

Expected: 19 XML parts classified, 1 hidden (Drum Set 2), 17 logical instruments visible.
"""
import sys
import warnings
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from bigband_condenser._spike.common import (  # noqa: E402
    setup_logging, KRONOS_EXTRACT,
    SECTION_REEDS, SECTION_BRASS, SECTION_RHYTHM, SECTION_DRUMS, SECTION_UNKNOWN,
)

EXPECTED_XML_COUNTS = {
    SECTION_REEDS: 5,
    SECTION_BRASS: 8,
    SECTION_RHYTHM: 4,
    SECTION_DRUMS: 2,
    SECTION_UNKNOWN: 0,
}

# Logical count: unique partNames, excluding hidden parts.
# Expected: 5 Reeds + 8 Brass + 3 Rhythm (Guitar+Piano+Bass, Piano x2 collapses) + 1 Drums (Drum Set 2 hidden)
EXPECTED_LOGICAL_VISIBLE = {
    SECTION_REEDS: 5,
    SECTION_BRASS: 8,
    SECTION_RHYTHM: 3,
    SECTION_DRUMS: 1,
}

EXPECTED_HIDDEN_COUNT = 1  # Drum Set 2

REEDS_KEYWORDS = ("sax", "clarinet", "flute", "oboe", "bassoon")
BRASS_KEYWORDS = ("trumpet", "trombone", "horn", "flugel", "tuba", "cornet")
RHYTHM_KEYWORDS = ("piano", "guitar", "bass", "vibraphone", "organ")
DRUMS_KEYWORDS = ("drum", "percuss")


def classify(part_name: str) -> str:
    """Classify a part by section using partName string matching."""
    if not part_name:
        return SECTION_UNKNOWN
    n = part_name.lower().strip()
    if any(kw in n for kw in DRUMS_KEYWORDS):
        return SECTION_DRUMS
    if any(kw in n for kw in REEDS_KEYWORDS):
        return SECTION_REEDS
    if any(kw in n for kw in BRASS_KEYWORDS):
        return SECTION_BRASS
    if any(kw in n for kw in RHYTHM_KEYWORDS):
        return SECTION_RHYTHM
    return SECTION_UNKNOWN


def detect_hidden_part_names(xml_path: Path) -> set:
    """Return set of partName strings that are marked as hidden in the source XML.

    Marker: <staff-details print-object="no"/> without `number` attribute, in the
    first measure's <attributes> block of a <part>.
    """
    tree = ET.parse(str(xml_path))
    root = tree.getroot()

    # Build id -> partName map from <part-list>
    id_to_name = {}
    for score_part in root.findall(".//score-part"):
        pid = score_part.get("id")
        pname_el = score_part.find("part-name")
        if pid and pname_el is not None and pname_el.text:
            id_to_name[pid] = pname_el.text

    hidden = set()
    for part in root.findall("part"):
        pid = part.get("id")
        name = id_to_name.get(pid)
        if not name:
            continue
        first_measure = part.find("measure")
        if first_measure is None:
            continue
        attrs = first_measure.find("attributes")
        if attrs is None:
            continue
        for sd in attrs.findall("staff-details"):
            if sd.get("print-object") == "no" and not sd.get("number"):
                hidden.add(name)
                break
    return hidden


def analyze_sample(sample_path: Path, logger) -> dict:
    """Parse a MusicXML sample, classify all parts, flag hidden ones."""
    from music21 import converter

    hidden_names = detect_hidden_part_names(sample_path)
    logger.info(f"Hidden parts detected in XML: {sorted(hidden_names) if hidden_names else '(none)'}")

    logger.info(f"Parsing: {sample_path.name}")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        score = converter.parse(str(sample_path))

    parts = list(score.parts)
    classified = []  # list of (idx, part_name, section, is_hidden)
    for i, p in enumerate(parts, 1):
        name = p.partName or ""
        section = classify(name)
        is_hidden = name in hidden_names
        classified.append((i, name, section, is_hidden))

    xml_counts = {s: 0 for s in (SECTION_REEDS, SECTION_BRASS, SECTION_RHYTHM, SECTION_DRUMS, SECTION_UNKNOWN)}
    for _, _, section, _ in classified:
        xml_counts[section] += 1

    # Logical count: unique partName per section, EXCLUDING hidden
    unique_visible = set()
    logical_visible = {s: 0 for s in (SECTION_REEDS, SECTION_BRASS, SECTION_RHYTHM, SECTION_DRUMS)}
    for _, name, section, is_hidden in classified:
        if section == SECTION_UNKNOWN or is_hidden:
            continue
        key = (name, section)
        if key not in unique_visible:
            unique_visible.add(key)
            logical_visible[section] += 1

    return {
        "classified": classified,
        "xml_counts": xml_counts,
        "logical_visible": logical_visible,
        "hidden_count": sum(1 for _, _, _, h in classified if h),
    }


def report(result: dict, logger) -> None:
    logger.info("")
    logger.info("CLASSIFICATION BY XML PART (H = hidden):")
    for section in (SECTION_REEDS, SECTION_BRASS, SECTION_RHYTHM, SECTION_DRUMS, SECTION_UNKNOWN):
        items = [(i, n, h) for i, n, s, h in result["classified"] if s == section]
        if items:
            logger.info(f"  {section} ({len(items)} parts):")
            for i, name, is_hidden in items:
                marker = "H " if is_hidden else "  "
                logger.info(f"    [{i:>2}] {marker}{name}")

    logger.info("")
    logger.info(f"HIDDEN PARTS FOUND: {result['hidden_count']} (expected {EXPECTED_HIDDEN_COUNT})")

    logger.info("")
    logger.info("XML PART COUNTS vs CLOUD EXPECTED:")
    for section, expected in EXPECTED_XML_COUNTS.items():
        got = result["xml_counts"].get(section, 0)
        status = "OK" if got == expected else "MISMATCH"
        logger.info(f"  {section:<10} expected={expected}, got={got} [{status}]")

    logger.info("")
    logger.info("LOGICAL VISIBLE INSTRUMENTS vs EXPECTED:")
    for section, expected in EXPECTED_LOGICAL_VISIBLE.items():
        got = result["logical_visible"].get(section, 0)
        status = "OK" if got == expected else "MISMATCH"
        logger.info(f"  {section:<10} expected={expected}, got={got} [{status}]")


def main() -> int:
    logger = setup_logging()

    logger.info("=" * 60)
    logger.info("Q2 INSTRUMENT CLASSIFICATION - LOCAL VERIFICATION")
    logger.info("=" * 60)

    if not KRONOS_EXTRACT.exists():
        logger.error(f"Extract not found: {KRONOS_EXTRACT}")
        return 2

    result = analyze_sample(KRONOS_EXTRACT, logger)
    report(result, logger)

    unknown_count = result["xml_counts"].get(SECTION_UNKNOWN, 0)
    xml_match = all(result["xml_counts"].get(s, 0) == v for s, v in EXPECTED_XML_COUNTS.items())
    logical_match = all(result["logical_visible"].get(s, 0) == v for s, v in EXPECTED_LOGICAL_VISIBLE.items())
    hidden_match = result["hidden_count"] == EXPECTED_HIDDEN_COUNT

    logger.info("")
    logger.info("=" * 60)
    if unknown_count == 0 and xml_match and logical_match and hidden_match:
        total_visible = sum(result["logical_visible"].values())
        logger.info(f"Q2 VERDICT: PASS - 19/19 XML classified, 1 hidden detected, {total_visible} logical visible instruments")
        return 0
    else:
        logger.warning(
            f"Q2 VERDICT: FAIL - unknowns={unknown_count}, "
            f"xml_match={xml_match}, logical_match={logical_match}, hidden_match={hidden_match}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
