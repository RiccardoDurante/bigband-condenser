"""Brass section condenser.

Family-based routing: trumpets+horns always treble, trombones always bass
(not pitch-based like reeds, by Music Expert decision). Pitch ordering
within each staff. Voice counts are effectively unlimited (99); the
family_map does the filtering - no notes dropped if the organ fits the
staff capacity.

No in-staff crossing markers (family routing is rigid, so a trumpet never
lands in the bass staff by design). Cross-staff pitch inversion (a
trombone playing higher than a trumpet, each on its own staff) is a
different notational issue, logged as FR-M5-A for future work.

Supported instruments:
  Trumpets 1-4   -> Tp.1-4, treble
  Horns 1-2      -> Cor.1-2, treble
  Trombone       -> Tbn, bass
  Bass Trombone  -> B.Tbn, bass
Unknown part names are not routed by this map; the condenser leaves them
out of both staves rather than silently placing them somewhere wrong.
Add them to _ABBR_BRASS and _FAMILY_MAP_BRASS to support more instruments.
"""
from __future__ import annotations

import warnings

from bigband_condenser.condenser.base import SectionCondenser
from bigband_condenser.condenser._common import (
    _annotate_cast_changes,
    _build_skeleton_part,
    _build_voice_elements,
    _collect_events,
    _fill_measure_rests,
    _place_event,
)

_ABBR_BRASS = {
    "Trumpet in Bb 1": "Tp.1",
    "Trumpet in Bb 2": "Tp.2",
    "Trumpet in Bb 3": "Tp.3",
    "Trumpet in Bb 4": "Tp.4",
    "Horn in F 1": "Cor.1",
    "Horn in F 2": "Cor.2",
    "Trombone": "Tbn",
    "Bass Trombone": "B.Tbn",
}

_FAMILY_MAP_BRASS = {
    "Trumpet in Bb 1": "treble",
    "Trumpet in Bb 2": "treble",
    "Trumpet in Bb 3": "treble",
    "Trumpet in Bb 4": "treble",
    "Horn in F 1": "treble",
    "Horn in F 2": "treble",
    "Trombone": "bass",
    "Bass Trombone": "bass",
}

_DEFAULT_RANK_BRASS = {
    "Trumpet in Bb 1": 1,
    "Trumpet in Bb 2": 2,
    "Trumpet in Bb 3": 3,
    "Trumpet in Bb 4": 4,
    "Horn in F 1": 5,
    "Horn in F 2": 6,
    "Trombone": 7,
    "Bass Trombone": 8,
}

_LARGE = 99  # effectively unlimited; family_map does the routing


class BrassCondenser(SectionCondenser):
    section_name = "Brass"
    upper_voice_count = _LARGE
    lower_voice_count = _LARGE
    family_map = _FAMILY_MAP_BRASS
    abbr = _ABBR_BRASS
    default_rank = _DEFAULT_RANK_BRASS

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
            events, self.upper_voice_count, self.lower_voice_count,
            family_map=self.family_map,
        )

        use_skeleton = source_score is not None and bool(source_score.parts)
        if use_skeleton:
            upper, upper_bounds = _build_skeleton_part(
                source_score, "Brass (upper)", music21.clef.TrebleClef()
            )
            lower, lower_bounds = _build_skeleton_part(
                source_score, "Brass (lower)", music21.clef.BassClef()
            )
        else:
            upper = music21.stream.Part()
            upper.partName = "Brass (upper)"
            upper.insert(0, music21.clef.TrebleClef())
            upper_bounds = None
            lower = music21.stream.Part()
            lower.partName = "Brass (lower)"
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
                abbr=self.abbr, default_rank=self.default_rank,
                enable_crossings=False,
                family_map=self.family_map,
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
