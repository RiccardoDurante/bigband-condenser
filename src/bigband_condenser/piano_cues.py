"""M6-A1: extract piano ensemble figure cues.

Finale marks ensemble figure cues on the piano part with <cue/> element
inside <note>. These are the figures the brass/reeds are playing that
the pianist uses as reference. We extract (measure, offset, duration)
and the RhythmCondenser inserts them as slash-head cue notes above the
treble staff (position A5, stem up) analogous to the M4.7/M4.8 drum
convention.

Chord-attached cue notes (multiple pitches at the same onset) are
deduplicated to one entry per onset: the visual cue is rhythmic, not
pitch-specific."""
from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass


@dataclass(frozen=True)
class EnsembleCue:
    measure_number: int
    offset_quarter: float
    duration_quarter: float


def extract_piano_ensemble_cues(xml_path, part_id):
    tree = ET.parse(str(xml_path))
    root = tree.getroot()
    part = next((p for p in root.iter("part") if p.get("id") == part_id), None)
    if part is None:
        return []

    cues = []
    divisions = 10080  # default; updated from <attributes>
    for m in part.iter("measure"):
        try:
            mnum = int(m.get("number"))
        except Exception:
            continue
        for attr in m.iter("attributes"):
            d = attr.findtext("divisions")
            if d:
                try:
                    divisions = int(d)
                except Exception:
                    pass
        offset_in_m = 0
        for child in m:
            if child.tag == "note":
                is_chord = child.find("chord") is not None
                is_cue = child.find("cue") is not None
                dur_text = child.findtext("duration", default="0")
                try:
                    dur = int(dur_text)
                except Exception:
                    dur = 0
                if is_cue:
                    offset_q = offset_in_m / divisions if divisions else 0.0
                    dur_q = dur / divisions if divisions else 0.0
                    cues.append(EnsembleCue(mnum, offset_q, dur_q))
                if not is_chord:
                    offset_in_m += dur
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

    # Deduplicate: multiple chord cues at same onset -> one entry
    seen = set()
    unique = []
    for c in cues:
        key = (c.measure_number, round(c.offset_quarter, 3))
        if key in seen:
            continue
        seen.add(key)
        unique.append(c)
    return unique
