"""Instrument classifier for Big Band Condenser v1.

Classifies parts into the 4 Charter sections (Reeds, Brass, Rhythm, Drums)
using partName string matching, and detects "hidden" parts marked for
playback-only (not visible in the printed score).

Rationale (from Spike M2):
- R26: music21.getInstruments() returns WRONG classes on Finale export, so we
  classify by partName string matching instead.
- R28: Finale marks hidden parts with <staff-details print-object="no"/>
  (without `number` attribute) in the first measure's <attributes>.
  Hidden parts are playback-only (realistic MIDI) and must be excluded
  from the condensed output.

API:
    classify_section(part_name) -> str           # section slug
    detect_hidden_part_names(xml_path) -> set   # hidden partNames in a file
    classify_score(xml_path) -> list[PartClassification]  # one-shot analysis
"""
from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


# Section slugs (Charter sezione 3.2)
SECTION_REEDS = "Reeds"
SECTION_BRASS = "Brass"
SECTION_RHYTHM = "Rhythm"
SECTION_DRUMS = "Drums"
SECTION_UNKNOWN = "UNKNOWN"


# Keyword tables - order matters: more distinctive (Drums) checked first,
# then Reeds, Brass, Rhythm. See _spike/q2_classify.py for the empirical
# validation (19/19 correct on Kronos test case).
_DRUMS_KEYWORDS = ("drum", "percuss")
_REEDS_KEYWORDS = ("sax", "clarinet", "flute", "oboe", "bassoon")
_BRASS_KEYWORDS = ("trumpet", "trombone", "horn", "flugel", "tuba", "cornet")
_RHYTHM_KEYWORDS = ("piano", "guitar", "bass", "vibraphone", "organ")


@dataclass(frozen=True)
class PartClassification:
    """Result of classifying one MusicXML <part>.

    Attributes:
        part_id: The MusicXML part id (e.g. "P1").
        part_name: The <part-name> text as it appears in the file.
        section: One of SECTION_* constants.
        is_hidden: True if the part is marked as hidden (playback-only).
    """
    part_id: str
    part_name: str
    section: str
    is_hidden: bool


def classify_section(part_name: str) -> str:
    """Classify a partName into one of the 4 Charter sections.

    Returns one of SECTION_REEDS, SECTION_BRASS, SECTION_RHYTHM, SECTION_DRUMS,
    or SECTION_UNKNOWN if no keyword matches.

    Validated 19/19 (100%) on Kronos kai Kairos test case in Spike M2 Q2.

    Examples:
        >>> classify_section("Alto Sax")
        'Reeds'
        >>> classify_section("Trumpet in Bb 3")
        'Brass'
        >>> classify_section("Horn in F 1")  # non-canonical big band but ok
        'Brass'
        >>> classify_section("Piano")
        'Rhythm'
        >>> classify_section("Drum Set 1")
        'Drums'
        >>> classify_section("")
        'UNKNOWN'
    """
    if not part_name:
        return SECTION_UNKNOWN
    n = part_name.lower().strip()

    # Drums first - most distinctive
    if any(kw in n for kw in _DRUMS_KEYWORDS):
        return SECTION_DRUMS
    if any(kw in n for kw in _REEDS_KEYWORDS):
        return SECTION_REEDS
    if any(kw in n for kw in _BRASS_KEYWORDS):
        return SECTION_BRASS
    if any(kw in n for kw in _RHYTHM_KEYWORDS):
        return SECTION_RHYTHM
    return SECTION_UNKNOWN


def detect_hidden_part_names(xml_path: Path | str) -> set[str]:
    """Return the set of partName strings marked as hidden in a MusicXML file.

    Hidden marker: <staff-details print-object="no"/> without `number` attribute,
    in the first measure's <attributes> block of a <part>. The `number` attribute
    exists on multi-staff instruments to hide a SPECIFIC staff within a part
    (not the whole part), so we require its absence to flag the whole part hidden.

    Validated on Kronos kai Kairos (Drum Set 2 correctly identified) in Q2.
    """
    tree = ET.parse(str(xml_path))
    root = tree.getroot()

    # Build id -> partName map from <part-list>
    id_to_name: dict[str, str] = {}
    for score_part in root.findall(".//score-part"):
        pid = score_part.get("id")
        pname_el = score_part.find("part-name")
        if pid and pname_el is not None and pname_el.text:
            id_to_name[pid] = pname_el.text

    hidden: set[str] = set()
    for part in root.findall("part"):
        name = id_to_name.get(part.get("id") or "")
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


def classify_score(xml_path: Path | str) -> list[PartClassification]:
    """Classify every <part> in a MusicXML file.

    Returns a list of PartClassification in document order. Combines
    classify_section() + detect_hidden_part_names() into a single pass.
    """
    path = Path(xml_path)
    tree = ET.parse(str(path))
    root = tree.getroot()

    hidden_names = detect_hidden_part_names(path)

    results: list[PartClassification] = []
    # Walk <part-list> to preserve order and get partName for each id
    part_list = root.find("part-list")
    if part_list is None:
        return results

    for score_part in part_list.findall("score-part"):
        pid = score_part.get("id") or ""
        pname_el = score_part.find("part-name")
        pname = pname_el.text if (pname_el is not None and pname_el.text) else ""
        section = classify_section(pname)
        is_hidden = pname in hidden_names
        results.append(PartClassification(
            part_id=pid, part_name=pname, section=section, is_hidden=is_hidden
        ))
    return results


def summarize(classifications: list[PartClassification]) -> dict:
    """Return summary counts: XML parts per section, logical visible instruments.

    Logical visible = unique partNames per section, excluding hidden parts.
    (Multiple XML parts with same partName collapse into 1 logical instrument,
    e.g. Piano split as 2 staves across 2 XML parts.)
    """
    xml_counts: dict[str, int] = {}
    unique_visible: set[tuple[str, str]] = set()
    logical_visible: dict[str, int] = {}
    hidden_count = 0

    for c in classifications:
        xml_counts[c.section] = xml_counts.get(c.section, 0) + 1
        if c.is_hidden:
            hidden_count += 1
            continue
        if c.section == SECTION_UNKNOWN:
            continue
        key = (c.part_name, c.section)
        if key not in unique_visible:
            unique_visible.add(key)
            logical_visible[c.section] = logical_visible.get(c.section, 0) + 1

    return {
        "xml_counts": xml_counts,
        "logical_visible": logical_visible,
        "hidden_count": hidden_count,
        "total_xml_parts": len(classifications),
        "total_logical_visible": sum(logical_visible.values()),
    }
