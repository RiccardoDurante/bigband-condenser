"""Reeds section condenser.

Section-specific wrapper around the generic infrastructure in
`condenser/_common`. Only reeds-specific bits here:
- 5-saxophone abbreviations and default rank (S.Sx, A.Sx, T.Sx 1, T.Sx 2, Bar.Sx)
- pitch-based global 2+3 ranking (not family-based)
- crossing markers enabled (an alto landing in lower is notable)
"""
from __future__ import annotations

import warnings

from bigband_condenser.condenser.base import SectionCondenser
from bigband_condenser.condenser._common import (
    MIN_DURATION,
    _Ev,
    _annotate_cast_changes,
    _build_cast_segments,
    _build_skeleton_part,
    _build_voice_elements,
    _collect_events,
    _detect_crossings,
    _fill_measure_rests,
    _filter_cast_segments,
    _format_cast_annotations,
    _format_crossing_marker,
    _insert_text_direction,
    _place_event,
    _split_for_label,
)

_ABBR_REEDS = {
    "Soprano Sax": "S.Sx",
    "Alto Sax": "A.Sx",
    "Tenor Sax 1": "T.Sx 1",
    "Tenor Sax 2": "T.Sx 2",
    "Baritone Sax": "Bar.Sx",
}
_DEFAULT_RANK_REEDS = {
    "Soprano Sax": 1,
    "Alto Sax": 2,
    "Tenor Sax 1": 3,
    "Tenor Sax 2": 4,
    "Baritone Sax": 5,
}


class ReedsCondenser(SectionCondenser):
    section_name = "Reeds"
    upper_voice_count = 2
    lower_voice_count = 3

    def condense(self, parts: list, source_score=None):
        import music21

        if not parts:
            return (music21.stream.Part(), music21.stream.Part())

        concert_parts = []
        for p in parts:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                concert_parts.append(p.toSoundingPitch(inPlace=False))

        events = _collect_events(concert_parts)
        upper_elems, lower_elems = _build_voice_elements(
            events, self.upper_voice_count, self.lower_voice_count
        )

        use_skeleton = source_score is not None and bool(source_score.parts)
        if use_skeleton:
            upper, upper_bounds = _build_skeleton_part(
                source_score, "Reeds (upper)", music21.clef.TrebleClef()
            )
            lower, lower_bounds = _build_skeleton_part(
                source_score, "Reeds (lower)", music21.clef.BassClef()
            )
        else:
            upper = music21.stream.Part()
            upper.partName = "Reeds (upper)"
            upper.insert(0, music21.clef.TrebleClef())
            upper_bounds = None
            lower = music21.stream.Part()
            lower.partName = "Reeds (lower)"
            lower.insert(0, music21.clef.BassClef())
            lower_bounds = None

        for onset, duration, slots in upper_elems:
            _place_event(upper, upper_bounds, onset, duration, slots)
        for onset, duration, slots in lower_elems:
            _place_event(lower, lower_bounds, onset, duration, slots)

        if use_skeleton:
            parts_order = [p.partName or "<unnamed>" for p in parts]
            _annotate_cast_changes(
                upper, upper_bounds, lower, lower_bounds,
                events, parts_order,
                self.upper_voice_count, self.lower_voice_count,
                abbr=_ABBR_REEDS, default_rank=_DEFAULT_RANK_REEDS,
                enable_crossings=True,
            )
            for part_obj, bounds in ((upper, upper_bounds), (lower, lower_bounds)):
                for measure, _start, length in bounds:
                    _fill_measure_rests(measure, length)
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    try:
                        part_obj.makeBeams(inPlace=True)
                    except Exception:
                        pass
        else:
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
