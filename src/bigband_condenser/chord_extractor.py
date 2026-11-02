"""M6.2: extract chord symbols from a MusicXML part.

Reads <harmony> elements, including <root>, <kind>, <bass>, and
<degree> alterations, and converts them into human-readable chord
labels (e.g. 'Am9', 'G7alt', 'Cmaj9/E').

Each returned entry has:
  - measure_number: int
  - offset_in_measure_divisions: int (raw MusicXML offset)
  - label: str (chord label)
  - raw_kind: str (original <kind> value, for debugging)
"""
from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass


_KIND_SUFFIX = {
    "major": "",
    "minor": "m",
    "augmented": "aug",
    "diminished": "dim",
    "dominant": "7",
    "major-seventh": "maj7",
    "minor-seventh": "m7",
    "diminished-seventh": "dim7",
    "augmented-seventh": "aug7",
    "half-diminished": "m7b5",
    "major-minor": "mMaj7",
    "major-sixth": "6",
    "minor-sixth": "m6",
    "dominant-ninth": "9",
    "major-ninth": "maj9",
    "minor-ninth": "m9",
    "dominant-11th": "11",
    "major-11th": "maj11",
    "minor-11th": "m11",
    "dominant-13th": "13",
    "major-13th": "maj13",
    "minor-13th": "m13",
    "suspended-second": "sus2",
    "suspended-fourth": "sus4",
    "power": "5",
    "none": "N.C.",
}


_ALTER_TO_ACC = {-2: "bb", -1: "b", 0: "", 1: "#", 2: "##"}


@dataclass(frozen=True)
class ChordSymbol:
    measure_number: int
    offset_divisions: int
    label: str
    raw_kind: str


def _step_with_alter(step: str, alter_str: str | None) -> str:
    try:
        alter = int(alter_str) if alter_str is not None else 0
    except Exception:
        alter = 0
    return f"{step}{_ALTER_TO_ACC.get(alter, '')}"


def _format_kind(kind_el):
    """Return (label_suffix, raw_kind, used_text).
    used_text=True means Finale provided an explicit text label on
    <kind text='...'>: in that case the caller must NOT also concatenate
    <degree> elements, because the text already encodes them."""
    if kind_el is None:
        return "", "", False
    raw = (kind_el.text or "").strip()
    text_attr = kind_el.get("text")
    if text_attr:
        return text_attr, raw, True
    return _KIND_SUFFIX.get(raw, raw), raw, False


def _format_degrees(harmony):
    parts = []
    for deg in harmony.iter("degree"):
        val = deg.findtext("degree-value", default="")
        alter = deg.findtext("degree-alter", default="0")
        dtype = deg.findtext("degree-type", default="add")
        try:
            a = int(alter)
        except Exception:
            a = 0
        acc = _ALTER_TO_ACC.get(a, "")
        if dtype == "add":
            parts.append(f"add{acc}{val}")
        elif dtype == "alter":
            parts.append(f"{acc}{val}")
        elif dtype == "subtract":
            parts.append(f"no{val}")
    return "".join(parts)


def _jazzify(label):
    """Convert label to jazz-standard spelling (minor -> m).
    Only touches 'min' prefixes attached to a chord quality marker; does
    not touch instrument-like words that would never appear in a chord."""
    # 'min' at the start of the quality suffix or after a root letter
    import re
    # Match 'min' only when preceded by a chord-root boundary (letter+optional accidental)
    # and followed by a digit, slash, or end of string. 'min9', 'min7b5', etc.
    return re.sub(r"min(?=\d|b|#|/|$)", "m", label)


def extract_chord_symbols(xml_path, part_id):
    """Return list of ChordSymbol for the given part, in document order."""
    tree = ET.parse(str(xml_path))
    root_el = tree.getroot()
    part = next((p for p in root_el.iter("part") if p.get("id") == part_id), None)
    if part is None:
        return []

    chords = []
    for m in part.iter("measure"):
        try:
            mnum = int(m.get("number"))
        except Exception:
            continue
        offset_in_m = 0
        for child in m:
            if child.tag == "note":
                dur = child.findtext("duration", default="0")
                try:
                    offset_in_m += int(dur)
                except Exception:
                    pass
            elif child.tag == "backup":
                dur = child.findtext("duration", default="0")
                try:
                    offset_in_m -= int(dur)
                except Exception:
                    pass
            elif child.tag == "forward":
                dur = child.findtext("duration", default="0")
                try:
                    offset_in_m += int(dur)
                except Exception:
                    pass
            elif child.tag == "harmony":
                root_el2 = child.find("root")
                if root_el2 is None:
                    continue
                step = root_el2.findtext("root-step", default="")
                alter = root_el2.findtext("root-alter", default=None)
                root_label = _step_with_alter(step, alter)
                kind_text, raw_kind, used_text = _format_kind(child.find("kind"))
                degree_str = "" if used_text else _format_degrees(child)
                bass_el = child.find("bass")
                bass_label = ""
                if bass_el is not None:
                    bstep = bass_el.findtext("bass-step", default="")
                    balter = bass_el.findtext("bass-alter", default=None)
                    if bstep:
                        bass_label = "/" + _step_with_alter(bstep, balter)
                label = f"{root_label}{kind_text}{degree_str}{bass_label}"
                label = _jazzify(label)
                chords.append(ChordSymbol(mnum, offset_in_m, label, raw_kind))
    return chords
