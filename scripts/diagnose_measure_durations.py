"""Diagnose measure duration integrity in a MusicXML output file."""
from __future__ import annotations

import sys
from pathlib import Path
from music21 import converter, stream, meter

TOL = 1e-6


def voice_duration(container) -> float:
    total = 0.0
    for el in container.notesAndRests:
        total += float(el.duration.quarterLength)
    return total


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
                per_voice = [(v.id, voice_duration(v)) for v in voices]
            else:
                per_voice = [("(no voices)", voice_duration(m))]

            is_pickup = (mi == 0 and m.number == 0)
            is_last = (mi == n_measures - 1)

            for vid, actual in per_voice:
                delta = actual - expected
                flag = ""
                if abs(delta) > TOL:
                    if is_pickup and actual < expected:
                        flag = "  [PICKUP - short is legal]"
                    elif is_last and actual < expected:
                        flag = "  [FINAL - short may be legal]"
                    else:
                        flag = "  <-- BAD"
                        bad_count += 1
                print(
                    f"  M{m.number:>3} v{vid}: "
                    f"actual={actual:>6.3f}  "
                    f"expected={expected:>6.3f}  "
                    f"delta={delta:+.3f}"
                    f"{flag}"
                )
        print()

    print(f"TOTAL BAD measures (excluding legal pickup/final): {bad_count}")
    return 0 if bad_count == 0 else 2


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/diagnose_measure_durations.py <path.musicxml>")
        sys.exit(1)
    sys.exit(diagnose(Path(sys.argv[1])))
