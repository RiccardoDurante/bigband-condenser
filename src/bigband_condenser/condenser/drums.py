"""Drums section PRESERVER (not condenser).

The drum part is kept intact and copied through: all notes (unpitched),
text expressions, articulations, measure structure, dynamics. Only the
clef is swapped to PercussionClef. No ranking, no split, no cast labels,
no crossing markers.

Why PRESERVER and not CONDENSER (Music Expert decision 2026-11-01):
- The drum MusicXML has only unpitched notes, so we cannot classify
  kick/snare/hi-hat/ride without heuristics or a MIDI mapping that the
  source does not provide.
- All notes have notehead=normal in the Kronos extract, so slash vs
  rhythmic distinction is not encoded. The composer wrote drum rhythm
  explicitly; we respect that.
- There are no simultaneous drum chords in the extract (no kick+hihat
  stacked), so no multi-voice logic needed in v1.

Backlog (not scope v1):
- FR-M7-A: multi-part drums (Percussion congas, Mallets vibraphone),
  only Drum Set X supported in v1
- FR-M7-B: multi-voice drum (voice 1 cymbals / voice 2 bass drum),
  single voice assumed
- FR-M7-C: slash vs rhythmic auto-derivation (would need composer
  convention or MIDI mapping)
"""
from __future__ import annotations

import copy
import warnings

from bigband_condenser.condenser.base import SectionCondenser
from bigband_condenser.drum_normalizer import (
    collect_note_instrument_names_from_xml,
    normalize_drum_notation,
)


class DrumsCondenser(SectionCondenser):
    section_name = "Drums"

    def __init__(self, source_xml_path=None):
        """source_xml_path: optional path to the original MusicXML file,
        used to recover per-note instrument names (music21 collapses all
        percussion score-instruments into a generic 'Percussion' object)."""
        self.source_xml_path = source_xml_path

    def condense(self, parts: list, source_score=None):
        import music21

        if not parts:
            return (music21.stream.Part(), None)

        drum_part = parts[0]
        output = copy.deepcopy(drum_part)
        output.partName = "Drums"

        inst_names = None
        if self.source_xml_path is not None:
            try:
                inst_names = collect_note_instrument_names_from_xml(
                    self.source_xml_path, drum_part.partName or "Drum Set 1"
                )
            except Exception:
                inst_names = None

        # Z (M7): normalize composer drum notation to Weinberg/PAS standard,
        # using the raw-XML instrument-name list when available.
        normalize_drum_notation(output, instrument_names_by_order=inst_names)

        # Swap all clefs for PercussionClef
        for element in list(output.recurse().getElementsByClass(music21.clef.Clef)):
            try:
                site = element.activeSite
                if site is not None:
                    site.remove(element)
            except Exception:
                pass
        output.insert(0, music21.clef.PercussionClef())

        return (output, None)
