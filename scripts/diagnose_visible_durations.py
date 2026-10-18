"""Diagnose VISIBLE duration (print-object=yes) per measure.

Reports measures where visible duration < barDuration, which Dorico renders
as an incomplete measure even though the full XML duration sums correctly.
"""
from __future__ import annotations

import sys
from pathlib import Path
from music21 import converter, stream, meter

TOL = 1e-6


def is_hidden(el) -> bool:
    """True if the element has print-object=no in MusicXML."""
    style = getattr(el, "style", None)
    if style is None:
        return False
    return getattr(style, "hideObjectOnPrint", False) is True


def split_durations(container):
    """Return (visible_qL, hidden_qL) for a Measure or Voice."""
    visible = 0.0
    hidden = 0.0
    for el in container.notesAndRests:
        q = float(el.duration.quarterLength)
        if is_hidden(el):
            hidden += q
        else:
            visible += q
    return visible, hidden


def diagnose(path: Path) -> int:
    score = converter.parse(str(path))
    parts = list(score.parts)
    print(f"File: {path.name}")
    print(f"Parts: {len(parts)}")
    print()

    bad_count = 0
    for pi, part in enumerate(parts):
        pname = part.partName or f"Part{pi}"
        print(f"=== Part {pi}: {pname} ===")
        measures = list(part.getElementsByClass(stream.Measure))
        if not measures:
            print("  (no measures)")
            continue

        last_ts = None
        n_measures = len(measures)

        for mi, m in enumerate(measures):
            ts_here = m.getElementsByClass(meter.TimeSignature)
            if ts_here:
                last_ts = ts_here[0]
            expected = (
                last_ts.barDuration.quarterLength
                if last_ts is not None
                else m.barDuration.quarterLength
            )

            voices = list(m.voices)
            if voices:
                items = [(f"v{v.id}", split_durations(v)) for v in voices]
            else:
                items = [("(no voices)", split_durations(m))]

            is_pickup = (mi == 0 and m.number == 0)

            for label, (vis, hid) in items:
                total = vis + hid
                flag = ""
                if abs(vis - expected) > TOL:
                    if is_pickup:
                        flag = "  [PICKUP]"
                    elif hid > TOL:
                        flag = f"  <-- VISIBLY SHORT (hidden={hid:.3f})"
                        bad_count += 1
                    else:
                        flag = "  <-- SHORT"
                        bad_count += 1
                print(
                    f"  M{m.number:>3} {label}: "
                    f"visible={vis:>6.3f}  hidden={hid:>6.3f}  "
                    f"total={total:>6.3f}  expected={expected:>6.3f}"
                    f"{flag}"
                )
        print()

    print(f"TOTAL visually-short measures: {bad_count}")
    return 0 if bad_count == 0 else 2


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/diagnose_visible_durations.py <path.musicxml>")
        sys.exit(1)
    sys.exit(diagnose(Path(sys.argv[1])))
