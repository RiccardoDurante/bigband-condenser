"""Reeds section condenser (M4-R1: dynamic split 2+3 by pitch, treble/bass).

Scope R1 (first iteration):
- Take N reed parts, convert each to concert pitch
- Collect note-start events across parts, grouped by snapped offset
- For each onset group:
  * Sort notes by MIDI pitch descending (acute to grave)
  * Top 2 notes -> upper staff (treble clef)
  * Remaining 3 (max) -> lower staff (bass clef)
- Quantize offset and duration to 0.125 ql grid (R1 safe quantization)
- Skip notes with duration < MIN_DURATION (D-022 playback artifacts)
- Finalize with makeNotation()

Scope R1 EXCLUDES (R2/R3): omoritmia, soli text, voice-crossing markers,
chord analysis, adaptive clef (FR-M4-A).

Determinism: tie-breaking by partName order (Charter P1).
"""
from __future__ import annotations

import warnings
from dataclasses import dataclass

from bigband_condenser.condenser.base import SectionCondenser


_OFFSET_EPS = 0.001
# Below this quarter_length, treat as realistic-playback artifact (D-022).
MIN_DURATION = 0.0625
# Quantization grid for offset and duration (R1 safe snapping).
# 0.125 = thirty-second note; fine enough to preserve most notation,
# coarse enough to avoid "inexpressible" rests from triplet artifacts.
_SNAP_GRID = 0.125


def _snap(value: float) -> float:
    """Snap a float to the nearest _SNAP_GRID multiple."""
    return round(value / _SNAP_GRID) * _SNAP_GRID


@dataclass(frozen=True, order=True)
class _OnsetNote:
    sort_key: tuple
    midi: int
    pitch_name: str
    quarter_length: float
    part_name: str
    offset: float


class ReedsCondenser(SectionCondenser):
    section_name = "Reeds"
    upper_voice_count = 2  # D-028 variant: 2 acute voices to upper (treble)
    lower_voice_count = 3  # 3 grave voices to lower (bass clef)

    def condense(self, parts: list):
        import music21

        if not parts:
            return (music21.stream.Part(), music21.stream.Part())

        # Step 1: convert each input part to concert pitch
        concert_parts = []
        for p in parts:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                concert_parts.append(p.toSoundingPitch(inPlace=False))

        # Step 2: collect note-start events, grouped by snapped offset
        onset_groups: dict[float, list[_OnsetNote]] = {}
        for p in concert_parts:
            part_name = p.partName or "<unnamed>"
            for n in p.recurse().notes:
                if not hasattr(n, "pitch") or n.pitch is None:
                    continue
                ql_raw = float(n.duration.quarterLength)
                if ql_raw < MIN_DURATION:
                    continue
                # Snap offset and duration to grid for safe MusicXML export
                offset = _snap(float(n.offset))
                ql_snapped = _snap(ql_raw)
                if ql_snapped <= 0:
                    continue
                offset_key = round(offset / _OFFSET_EPS) * _OFFSET_EPS
                event = _OnsetNote(
                    sort_key=(-n.pitch.midi, part_name),
                    midi=n.pitch.midi,
                    pitch_name=n.pitch.nameWithOctave,
                    quarter_length=ql_snapped,
                    part_name=part_name,
                    offset=offset,
                )
                onset_groups.setdefault(offset_key, []).append(event)

        # Step 3: build output parts with treble/bass clefs
        upper = music21.stream.Part()
        upper.partName = "Reeds (upper)"
        upper.insert(0, music21.clef.TrebleClef())

        lower = music21.stream.Part()
        lower.partName = "Reeds (lower)"
        lower.insert(0, music21.clef.BassClef())

        # Step 4: distribute 2+3 by pitch rank
        for offset_key in sorted(onset_groups.keys()):
            events = sorted(onset_groups[offset_key])
            top = events[: self.upper_voice_count]
            bottom = events[self.upper_voice_count : self.upper_voice_count + self.lower_voice_count]

            for e in top:
                n = music21.note.Note(e.pitch_name)
                n.duration.quarterLength = e.quarter_length
                upper.insert(e.offset, n)

            for e in bottom:
                n = music21.note.Note(e.pitch_name)
                n.duration.quarterLength = e.quarter_length
                lower.insert(e.offset, n)

        # Step 5: finalize notation (makeMeasures + makeTies + makeRests)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                upper.makeNotation(inPlace=True)
            except Exception:
                pass
            try:
                lower.makeNotation(inPlace=True)
            except Exception:
                pass

        return (upper, lower)
