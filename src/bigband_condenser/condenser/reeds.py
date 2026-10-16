"""Reeds section condenser (M4-R1 + M4.1 metadata preservation).

Scope cumulative:
- M4.0: scaffold condenser/
- M4-R1 (deprecated by WBS retro): split 2+3 by pitch, treble/bass
- M4.1 (THIS): preserve initial key signature + time signature + tempo marking
  from source_score. Score-level metadata (title/composer) is handled by caller
  (preview script or future assembler, see WBS M4.1 scope).

Pending WBS M4.2-M4.8: measure structure (pickup, barlines), single-voice
passthrough, chord notation, omoritmia, text directions, voice crossing.

Determinism: tie-breaking by partName order (Charter P1).
"""
from __future__ import annotations

import warnings
from dataclasses import dataclass

from bigband_condenser.condenser.base import SectionCondenser


_OFFSET_EPS = 0.001
MIN_DURATION = 0.0625
_SNAP_GRID = 0.125


def _snap(value: float) -> float:
    return round(value / _SNAP_GRID) * _SNAP_GRID


@dataclass(frozen=True, order=True)
class _OnsetNote:
    sort_key: tuple
    midi: int
    pitch_name: str
    quarter_length: float
    part_name: str
    offset: float


def _extract_initial_metadata(source_score):
    """Extract (key, time_signature, tempo) from the first occurrence in source.

    Returns a tuple (key_obj, ts_obj, tempo_obj) where each item is either
    a music21 element to be cloned, or None if not found.
    """
    if source_score is None:
        return (None, None, None)
    import music21

    initial_key = None
    initial_time = None
    initial_tempo = None
    try:
        flat = source_score.flatten()
        # Try music21.key.Key first (richer: tonic + mode), fallback to KeySignature
        keys = list(flat.getElementsByClass(music21.key.Key))
        if not keys:
            keys = list(flat.getElementsByClass(music21.key.KeySignature))
        if keys:
            initial_key = keys[0]

        times = list(flat.getElementsByClass(music21.meter.TimeSignature))
        if times:
            initial_time = times[0]

        tempos = list(flat.getElementsByClass(music21.tempo.MetronomeMark))
        if tempos:
            initial_tempo = tempos[0]
    except Exception:
        pass
    return (initial_key, initial_time, initial_tempo)


def _clone_metadata_into(part, initial_key, initial_time, initial_tempo):
    """Insert fresh clones of (key, time_sig, tempo) at offset 0 of part.

    Fresh clones to avoid aliasing: the same object inserted in both upper
    and lower would make music21 unhappy on write.
    """
    import music21
    if initial_key is not None:
        try:
            if isinstance(initial_key, music21.key.Key):
                clone = music21.key.Key(initial_key.tonic.name, initial_key.mode)
            else:
                clone = music21.key.KeySignature(initial_key.sharps)
            part.insert(0, clone)
        except Exception:
            pass
    if initial_time is not None:
        try:
            part.insert(0, music21.meter.TimeSignature(initial_time.ratioString))
        except Exception:
            pass
    if initial_tempo is not None:
        try:
            mm = music21.tempo.MetronomeMark(
                number=initial_tempo.number,
                text=initial_tempo.text,
            )
            part.insert(0, mm)
        except Exception:
            pass


class ReedsCondenser(SectionCondenser):
    section_name = "Reeds"
    upper_voice_count = 2
    lower_voice_count = 3

    def condense(self, parts: list, source_score=None):
        import music21

        if not parts:
            return (music21.stream.Part(), music21.stream.Part())

        # M4.1: extract initial metadata from source_score (if provided)
        initial_key, initial_time, initial_tempo = _extract_initial_metadata(source_score)

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

        # Step 3: build output parts with clefs + M4.1 metadata
        upper = music21.stream.Part()
        upper.partName = "Reeds (upper)"
        upper.insert(0, music21.clef.TrebleClef())
        _clone_metadata_into(upper, initial_key, initial_time, initial_tempo)

        lower = music21.stream.Part()
        lower.partName = "Reeds (lower)"
        lower.insert(0, music21.clef.BassClef())
        _clone_metadata_into(lower, initial_key, initial_time, initial_tempo)

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

        # Step 5: finalize notation
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
