"""Rhythm section condenser (M6).

Scope v1 (Opzione D with staff-style awareness):
- Rigo treble: Guitar as source. For each measure where Guitar has a slash
  region active (from <measure-style><slash/></measure-style> in source
  MusicXML), replace note content with slash notation. Elsewhere preserve
  Guitar's written notes.
- Rigo bass: Bass as source, same rule.
- Chord symbols: extracted from Piano (authoritative source, 120 chords
  in the full Kronos). Piano's actual notes are IGNORED (Piano is hidden
  in the source: the conductor reads chord symbols only, not piano notes).

Known limitations (backlog):
- FR-M6-A: ensemble figure cues on Piano (size='full') not propagated
- FR-M6-B: beat-repeat and measure-repeat <measure-style> not supported
- FR-M6-C: guitar notehead='x' muted comping not special-cased
- FR-M6-D: multi-voice Piano (voices 2-4) not handled
"""
from __future__ import annotations

import copy
import warnings

from bigband_condenser.condenser.base import SectionCondenser
from bigband_condenser.rhythm_staff_style import extract_slash_measures
from bigband_condenser.chord_extractor import extract_chord_symbols
from bigband_condenser.piano_cues import extract_piano_ensemble_cues


def _find_part(parts, keyword):
    for p in parts:
        if keyword in (p.partName or "").lower():
            return p
    return None


def _xml_id_for_part_name(xml_path, part_name):
    """Return the part id (e.g. 'P14') whose part-name matches."""
    import xml.etree.ElementTree as ET
    tree = ET.parse(str(xml_path))
    root = tree.getroot()
    for sp in root.iter("score-part"):
        pname = (sp.findtext("part-name", default="") or "").strip()
        if pname == part_name:
            return sp.get("id")
    return None


def _measure_quarter_length(measure):
    try:
        return float(measure.duration.quarterLength)
    except Exception:
        return 4.0


def _replace_measure_with_slashes(measure, display_step="B", display_octave=4):
    """Strip the measure's notes/rests and insert N slash quarter-notes,
    where N = ceil(measure.quarterLength). Slash head on the center line."""
    import music21
    bar_len = _measure_quarter_length(measure)
    purge_classes = (music21.note.Note, music21.note.Rest, music21.chord.Chord)
    for el in list(measure.recurse()):
        if isinstance(el, purge_classes):
            try:
                site = el.activeSite
                if site is not None:
                    site.remove(el)
            except Exception:
                pass
    beats = max(1, int(round(bar_len)))
    for i in range(beats):
        slash = music21.note.Unpitched()
        slash.displayStep = display_step
        slash.displayOctave = display_octave
        slash.duration.quarterLength = 1.0
        try:
            slash.notehead = "slash"
        except Exception:
            pass
        try:
            slash.stemDirection = "noStem"
        except Exception:
            pass
        measure.insert(float(i), slash)


class RhythmCondenser(SectionCondenser):
    section_name = "Rhythm"

    def __init__(self, source_xml_path=None):
        self.source_xml_path = source_xml_path

    def condense(self, parts: list, source_score=None):
        import music21

        guitar = _find_part(parts, "guitar")
        bass = _find_part(parts, "bass")
        piano = _find_part(parts, "piano")

        if guitar is None and bass is None:
            return (music21.stream.Part(), None)

        xml_path = self.source_xml_path
        guitar_slash = {}
        bass_slash = {}
        chords = []
        if xml_path is not None:
            if guitar is not None:
                gid = _xml_id_for_part_name(xml_path, guitar.partName)
                if gid:
                    guitar_slash = extract_slash_measures(xml_path, gid)
            if bass is not None:
                bid = _xml_id_for_part_name(xml_path, bass.partName)
                if bid:
                    bass_slash = extract_slash_measures(xml_path, bid)
            # Chord source: Piano > Guitar fallback
            chord_source = piano or guitar
            if chord_source is not None:
                cid = _xml_id_for_part_name(xml_path, chord_source.partName)
                if cid:
                    chords = extract_chord_symbols(xml_path, cid)

        # Build output parts (deepcopy + modify)
        if guitar is not None:
            upper = copy.deepcopy(guitar)
            upper.partName = "Rhythm (treble)"
            # swap any existing clef for TrebleClef
            for cl in list(upper.recurse().getElementsByClass(music21.clef.Clef)):
                try:
                    site = cl.activeSite
                    if site is not None:
                        site.remove(cl)
                except Exception:
                    pass
            upper.insert(0, music21.clef.TrebleClef())
            # apply slash regions
            guitar_measures_slash = set()
            for staff_set in guitar_slash.values():
                guitar_measures_slash |= staff_set
            for m in upper.getElementsByClass(music21.stream.Measure):
                if m.number in guitar_measures_slash:
                    _replace_measure_with_slashes(m, "B", 4)
        else:
            upper = music21.stream.Part()
            upper.partName = "Rhythm (treble)"
            upper.insert(0, music21.clef.TrebleClef())

        if bass is not None:
            lower = copy.deepcopy(bass)
            lower.partName = "Rhythm (bass)"
            for cl in list(lower.recurse().getElementsByClass(music21.clef.Clef)):
                try:
                    site = cl.activeSite
                    if site is not None:
                        site.remove(cl)
                except Exception:
                    pass
            lower.insert(0, music21.clef.BassClef())
            bass_measures_slash = set()
            for staff_set in bass_slash.values():
                bass_measures_slash |= staff_set
            for m in lower.getElementsByClass(music21.stream.Measure):
                if m.number in bass_measures_slash:
                    _replace_measure_with_slashes(m, "D", 3)
        else:
            lower = music21.stream.Part()
            lower.partName = "Rhythm (bass)"
            lower.insert(0, music21.clef.BassClef())

        # Insert chord symbols above the upper staff
        for ch in chords:
            try:
                cs = music21.harmony.ChordSymbol(ch.label)
            except Exception:
                continue
            try:
                cs.writeAsChord = False
            except Exception:
                pass
            # Find the target measure in upper by number and insert at (approx) offset 0
            # (precise sub-measure offset requires divisions; v1 keeps all chord
            # symbols at the start of their measure for simplicity).
            for m in upper.getElementsByClass(music21.stream.Measure):
                if m.number == ch.measure_number:
                    try:
                        m.insert(0, cs)
                    except Exception:
                        pass
                    break

        # M6-X: big-band hit pattern decomposition for measures with piano
        # ensemble cues. Replace uniform slashes with the standard chart figure
        # [quarter, quarter, dotted-quarter, eighth tied]. The eighth tie
        # extends to beat 1 of the following measure (if it is also a slash
        # region), expressing the anticipated chord entry.
        if xml_path is not None and piano is not None:
            try:
                pid_piano = _xml_id_for_part_name(xml_path, piano.partName)
            except Exception:
                pid_piano = None
            if pid_piano:
                try:
                    piano_cues = extract_piano_ensemble_cues(xml_path, pid_piano)
                except Exception:
                    piano_cues = []
                cue_measures = set(c.measure_number for c in piano_cues)
                upper_measures_by_num = {m.number: m for m in upper.getElementsByClass(music21.stream.Measure)}
                guitar_slash_set = set()
                for staff_set in guitar_slash.values():
                    guitar_slash_set |= staff_set
                for mnum in sorted(cue_measures):
                    m = upper_measures_by_num.get(mnum)
                    if m is None:
                        continue
                    # Clear existing content (uniform slashes etc.)
                    for el in list(m.notesAndRests):
                        try:
                            m.remove(el)
                        except Exception:
                            pass
                    # Insert the big-band hit pattern.
                    # Entries: (offset, duration, is_tied, stem).
                    # stem='noStem' on quarters and dotted-quarter -> plain slash
                    # (comping); stem='up' on the eighth -> rhythmic notation
                    # with visible stem + flag, carrying the tie.
                    pattern = [
                        (0.0, 1.0, False, "noStem"),
                        (1.0, 1.0, False, "noStem"),
                        (2.0, 1.5, False, "noStem"),
                        (3.5, 0.5, True,  "up"),
                    ]
                    for offset, dur, is_tied, stem in pattern:
                        slash = music21.note.Unpitched()
                        slash.displayStep = "B"
                        slash.displayOctave = 4
                        slash.duration.quarterLength = dur
                        try:
                            slash.notehead = "slash"
                        except Exception:
                            pass
                        try:
                            slash.stemDirection = stem
                        except Exception:
                            pass
                        if is_tied:
                            try:
                                slash.tie = music21.tie.Tie("start")
                            except Exception:
                                pass
                        m.insert(offset, slash)
                    # Close the tie on the following measure's first beat
                    next_m = upper_measures_by_num.get(mnum + 1)
                    if next_m is not None:
                        first_note = None
                        for el in sorted(next_m.notes, key=lambda n: float(n.offset)):
                            first_note = el
                            break
                        if first_note is not None:
                            try:
                                existing_tie = getattr(first_note, "tie", None)
                                if existing_tie is None:
                                    first_note.tie = music21.tie.Tie("stop")
                                elif existing_tie.type == "start":
                                    first_note.tie = music21.tie.Tie("continue")
                            except Exception:
                                pass

        return (upper, lower)
