"""Drum notation normalizer (M7 Z — Opzione 3, by instrument name).

The source MusicXML exported by Finale contains explicit instrument
names in <score-instrument> declarations, and every <note> references
its instrument via <instrument id="..."/>. music21 exposes this as
note.getInstrument().instrumentName. Z uses this as the ground truth
and ignores display-step / display-octave of the source (which were
set by Finale's percussion map for its own visual rendering, not
expressed in a standard MusicXML way).

The target staff positions follow the Weinberg/PAS Guide to Standardized
Drumset Notation.
"""
from __future__ import annotations

# instrument_name (as exported by Finale) -> (step, octave, notehead, stem)
_WEINBERG_BY_NAME = {
    "Bass Drum":          ("F", 4, "normal",  "down"),
    "Kick Drum":          ("F", 4, "normal",  "down"),
    "Snare Drum":         ("C", 5, "normal",  "up"),
    "Snare Ghost Stroke": ("C", 5, "normal",  "up"),  # Dorico adds parens for ghost
    "Snare Rim Shot":     ("C", 5, "x",       "up"),  # rim shot = cross head on snare line
    "Side Stick":         ("C", 5, "x",       "up"),
    "High Tom":           ("E", 5, "normal",  "up"),
    "Mid Tom":            ("D", 5, "normal",  "up"),
    "Low-Mid Tom":        ("C", 5, "normal",  "up"),
    "Low Tom":            ("A", 4, "normal",  "up"),
    "Floor Tom":          ("A", 4, "normal",  "up"),
    "Hi-Hat Closed":      ("G", 5, "x",       "up"),
    "Hi-Hat Open":        ("G", 5, "x",       "up"),  # +articulation 'o' handled separately
    "Hi-Hat Pedal":       ("D", 4, "x",       "down"),
    "Hi-Hat Foot":        ("D", 4, "x",       "down"),
    "Ride Cymbal":        ("F", 5, "x",       "up"),
    "Ride Bell":          ("F", 5, "diamond", "up"),
    "Crash Cymbal":       ("A", 5, "x",       "up"),
    "Crash Cymbal 2":     ("A", 5, "x",       "up"),
    "Splash Cymbal":      ("B", 5, "x",       "up"),
    "China Cymbal":       ("B", 5, "x",       "up"),
    # Big-band specific
    "Rhythm Cues":        ("A", 5, "slash",   "up"),  # ensemble figure cue
}

# Normalize instrument name: Finale uses "%g" as separator token, strip spaces/case.
def _normalize_name(name):
    if not name:
        return ""
    s = name.replace("%g", " ").strip()
    while "  " in s:
        s = s.replace("  ", " ")
    return s


def _resolve_by_name(instrument_name):
    key = _normalize_name(instrument_name)
    if key in _WEINBERG_BY_NAME:
        return _WEINBERG_BY_NAME[key]
    # Case-insensitive fallback
    low = key.lower()
    for k, v in _WEINBERG_BY_NAME.items():
        if k.lower() == low:
            return v
    return None


def normalize_drum_notation(drum_part, instrument_names_by_order=None):
    """In-place normalization: for each Unpitched note in drum_part, read its
    associated Instrument name and remap displayStep/displayOctave/notehead/
    stem to the Weinberg target. Notes whose instrument name is not in the
    table are left untouched (defensive)."""
    import music21

    changed = 0
    note_index = -1
    for n in drum_part.recurse().notes:
        note_index += 1
        if not isinstance(n, music21.note.Unpitched):
            continue
        current_nh = getattr(n, "notehead", "normal")
        if current_nh and current_nh != "normal":
            continue  # idempotence

        name = None
        if instrument_names_by_order is not None and note_index < len(instrument_names_by_order):
            name = instrument_names_by_order[note_index]
        if name is None:
            inst = None
            try:
                inst = n.getInstrument(returnDefault=False)
            except Exception:
                try:
                    inst = n.getContextByClass("Instrument")
                except Exception:
                    inst = None
            name = getattr(inst, "instrumentName", None) if inst else None
        target = _resolve_by_name(name) if name else None
        if target is None:
            continue

        new_step, new_octave, new_nh, new_stem = target
        try:
            n.displayStep = new_step
            n.displayOctave = new_octave
        except Exception:
            pass
        try:
            n.notehead = new_nh
        except Exception:
            pass
        try:
            n.stemDirection = new_stem
        except Exception:
            pass
        try:
            if n.style and n.style.noteSize is not None:
                n.style.noteSize = None
        except Exception:
            pass
        changed += 1
    return changed


def collect_note_instrument_names_from_xml(xml_path, part_name):
    """Parse the source MusicXML and return a list of instrument names in
    document order, one per <note> element in the named part (both pitched
    and unpitched, EXCLUDING <rest>). Used because music21 collapses all
    percussion score-instruments into a single generic "Percussion"
    Instrument, losing the per-note mapping.

    Returns [] if the part is not found. Returns None for notes that have
    no <instrument id="..."/> reference."""
    import xml.etree.ElementTree as ET

    tree = ET.parse(str(xml_path))
    root = tree.getroot()

    id_to_name = {}
    target_part_id = None
    for score_part in root.iter("score-part"):
        pid = score_part.get("id")
        pname = (score_part.findtext("part-name", default="") or "").strip()
        if pname == part_name:
            target_part_id = pid
        for si in score_part.iter("score-instrument"):
            iid = si.get("id")
            iname = (si.findtext("instrument-name", default="") or "").strip()
            id_to_name[iid] = iname

    if target_part_id is None:
        return []

    names = []
    for part in root.iter("part"):
        if part.get("id") != target_part_id:
            continue
        for note in part.iter("note"):
            if note.find("rest") is not None:
                continue
            # Skip notes hidden at <note print-object="no">: music21
            # filters these out when parsing, so including them here
            # misaligns the per-note index between XML and the music21 Part.
            if note.get("print-object") == "no":
                continue
            inst_ref = note.find("instrument")
            iid = inst_ref.get("id") if inst_ref is not None else None
            names.append(id_to_name.get(iid))
    return names

