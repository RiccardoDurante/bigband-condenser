"""Reeds section condenser (M4-R1 + M4.1 metadata + M4.2 measure structure).

Scope cumulative:
- M4.0: scaffold condenser/
- M4-R1: split 2+3 by pitch, treble/bass
- M4.1: preserve initial key/time/tempo from source_score
- M4.2: clone measure structure (count, pickup, barlines, numbers) from
  source_score by deepcopy of first Part + content purge. Metadata (M4.1)
  come with the skeleton for free.

  BUGFIX M4.2a: music21 Measure.duration.quarterLength is derived from the
  rhythmic content of the Measure (notes/rests), NOT a fixed property of the
  Measure itself. Purging all Note/Rest/Chord objects collapses every
  Measure's duration to 0.0. Fix: snapshot each Measure's quarterLength
  BEFORE purging, then explicitly restore it AFTER purging.

  BUGFIX M4.2b: notes/rests were being inserted whole into whichever Measure
  contained their START offset, with no check for whether their duration
  crossed the following barline. Fix: _insert_into_measure splits a note's
  (or chord's) span across every Measure it overlaps, inserting one
  fragment per Measure tied together (Tie start/continue/stop).

  BUGFIX M4.2c: generic part.makeRests(fillGaps=True) computes each
  Measure's "bar duration" from the active TimeSignature context, NOT from
  the real (possibly partial/pickup) duration restored in M4.2a. Fix:
  _fill_measure_rests fills gaps using each Measure's own restored
  duration, measure by measure, instead of calling makeRests at Part level.

  BUGFIX M4.2d (pulled forward from WBS M4.5 "chord notation"): when two or
  more reed instruments land in the same output voice at the same onset --
  the normal case for block chords and unisons -- each was being inserted
  as its own separate Note object at the same offset. Fix:
  _collapse_onset_group dedupes identical pitches (unison -> one Note) and
  merges distinct pitches at the same onset into a single
  music21.chord.Chord.

  BUGFIX M4.2e (Music Expert decision 2026-10-16, Option A): a sustained
  note/chord in one voice can still be running when a DIFFERENT instrument's
  onset lands in the same voice (a real mid-bar cast change per Charter P2,
  not yet handled by dedicated re-voicing logic -- that is WBS M4.6/M4.7
  scope). Until then, _clip_overlaps deterministically truncates the
  earlier event to end exactly where the later one starts, matching how a
  professional condensed-score re-voicing looks on paper. Logged as backlog
  item FR-M4-E: replace with tie-preserving re-voicing once cast-change
  detection (M4.6/M4.7) exists.

Pending WBS M4.3/M4.6/M4.7/M4.8: single-voice passthrough, omoritmia
detection, text directions (incl. per-instrument unison/crossing labels,
and FR-M4-E tie-preserving re-voicing), voice crossing markers.

Determinism: tie-breaking by partName order (Charter P1); within a merged
chord, pitches are ordered by descending MIDI for deterministic output.
"""
from __future__ import annotations

import copy
import warnings
from dataclasses import dataclass

from bigband_condenser.condenser.base import SectionCondenser

_OFFSET_EPS = 0.001
_GAP_EPS = 1e-6
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


def _build_skeleton_part(source_score, name: str, new_clef):
    """Deepcopy source_score.parts[0] with musical content purged.

    Preserved: Measure objects (numbers, pickup, barlines, inner time
    signatures), key signatures, tempo markings, and (via BUGFIX M4.2a)
    each Measure's original quarterLength duration.
    Purged: Note, Rest, Chord, ChordSymbol, Dynamic, TextExpression,
    Instrument, Clef (we insert our own).
    """
    import music21

    if not source_score.parts:
        return None

    source_part = source_score.parts[0]
    skeleton = copy.deepcopy(source_part)
    skeleton.partName = name

    measure_durations: dict[int, float] = {}
    for m in skeleton.getElementsByClass(music21.stream.Measure):
        measure_durations[id(m)] = float(m.duration.quarterLength)

    purge_classes = (
        music21.note.Note,
        music21.note.Rest,
        music21.chord.Chord,
        music21.harmony.ChordSymbol,
        music21.dynamics.Dynamic,
        music21.expressions.TextExpression,
        music21.instrument.Instrument,
        music21.clef.Clef,
    )
    for element in list(skeleton.recurse()):
        if isinstance(element, purge_classes):
            try:
                site = element.activeSite
                if site is not None:
                    site.remove(element)
            except Exception:
                pass

    for m in skeleton.getElementsByClass(music21.stream.Measure):
        saved = measure_durations.get(id(m))
        if saved:
            m.duration.quarterLength = saved

    skeleton.insert(0, new_clef)
    return skeleton


def _collapse_onset_group(events: list[_OnsetNote]) -> tuple[list[str], float]:
    """Collapse simultaneous events destined for the same voice at the same
    onset (BUGFIX M4.2d). See module docstring.
    """
    by_pitch: dict[str, tuple[int, float]] = {}
    for e in events:
        prev = by_pitch.get(e.pitch_name)
        if prev is None or e.quarter_length > prev[1]:
            by_pitch[e.pitch_name] = (e.midi, e.quarter_length)

    duration = max(v[1] for v in by_pitch.values())
    pitches_sorted = sorted(by_pitch.keys(), key=lambda pn: by_pitch[pn][0], reverse=True)
    return pitches_sorted, duration


def _clip_overlaps(
    events: list[tuple[float, list[str], float]]
) -> list[tuple[float, list[str], float]]:
    """BUGFIX M4.2e: events is a time-ordered (ascending onset) list of
    (onset, pitch_names, duration) for ONE voice. If a later onset starts
    before the previous event's natural end, truncate the previous event
    so it ends exactly at the later onset (Option A, Music Expert decision
    2026-10-16). See module docstring for rationale and backlog FR-M4-E.
    """
    result: list[tuple[float, list[str], float]] = []
    for onset, pitches, duration in events:
        while result:
            prev_onset, prev_pitches, prev_duration = result[-1]
            prev_end = prev_onset + prev_duration
            if onset >= prev_end - _GAP_EPS:
                break
            new_prev_duration = onset - prev_onset
            if new_prev_duration > _GAP_EPS:
                result[-1] = (prev_onset, prev_pitches, new_prev_duration)
                break
            else:
                # Previous event fully devoured by the new onset; drop it
                # and re-check against what is now the last event.
                result.pop()
        result.append((onset, pitches, duration))
    return result


def _make_element(pitch_names: list[str]):
    import music21

    if len(pitch_names) == 1:
        return music21.note.Note(pitch_names[0])
    return music21.chord.Chord(pitch_names)


def _insert_into_measure(part, offset: float, quarter_length: float, pitch_names: list[str]) -> bool:
    """Insert a Note/Chord spanning [offset, offset + quarter_length) into
    part's Measures, SPLITTING it across every Measure it overlaps
    (BUGFIX M4.2b). offset is absolute in `part`.
    """
    import music21

    measures = sorted(
        part.getElementsByClass(music21.stream.Measure), key=lambda m: float(m.offset)
    )
    span_start = offset
    span_end = offset + quarter_length

    fragments = []
    for measure in measures:
        m_start = float(measure.offset)
        m_end = m_start + float(measure.duration.quarterLength)
        if m_end <= span_start + _GAP_EPS:
            continue
        if m_start >= span_end - _GAP_EPS:
            break
        frag_start = max(m_start, span_start)
        frag_end = min(m_end, span_end)
        frag_ql = frag_end - frag_start
        if frag_ql <= _GAP_EPS:
            continue
        fragments.append((measure, frag_start - m_start, frag_ql))

    if not fragments:
        return False

    multi = len(fragments) > 1
    for i, (measure, rel_offset, frag_ql) in enumerate(fragments):
        el = _make_element(pitch_names)
        el.duration.quarterLength = frag_ql
        if multi:
            if i == 0:
                el.tie = music21.tie.Tie("start")
            elif i == len(fragments) - 1:
                el.tie = music21.tie.Tie("stop")
            else:
                el.tie = music21.tie.Tie("continue")
        try:
            measure.insert(rel_offset, el)
        except Exception:
            return False
    return True


def _insert_part_level(part, offset: float, quarter_length: float, pitch_names: list[str]) -> None:
    el = _make_element(pitch_names)
    el.duration.quarterLength = quarter_length
    part.insert(offset, el)


def _fill_measure_rests(measure) -> None:
    """Fill the gaps in `measure` with explicit Rest objects, using the
    Measure's OWN restored duration as the bar length (BUGFIX M4.2c).
    """
    import music21

    bar_len = float(measure.duration.quarterLength)
    if bar_len <= _GAP_EPS:
        return

    notes = sorted(measure.notes, key=lambda n: float(n.offset))
    cursor = 0.0
    for n in notes:
        n_start = float(n.offset)
        if n_start > cursor + _GAP_EPS:
            gap = n_start - cursor
            r = music21.note.Rest()
            r.duration.quarterLength = gap
            measure.insert(cursor, r)
        n_end = n_start + float(n.duration.quarterLength)
        if n_end > cursor:
            cursor = n_end

    if cursor < bar_len - _GAP_EPS:
        gap = bar_len - cursor
        r = music21.note.Rest()
        r.duration.quarterLength = gap
        measure.insert(cursor, r)


class ReedsCondenser(SectionCondenser):
    section_name = "Reeds"
    upper_voice_count = 2
    lower_voice_count = 3

    def condense(self, parts: list, source_score=None):
        import music21

        if not parts:
            return (music21.stream.Part(), music21.stream.Part())

        # Step 1: convert to concert pitch
        concert_parts = []
        for p in parts:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                concert_parts.append(p.toSoundingPitch(inPlace=False))

        # Step 2: collect note-start events, grouped by snapped ABSOLUTE offset
        onset_groups: dict[float, list[_OnsetNote]] = {}
        for p in concert_parts:
            part_name = p.partName or "<unnamed>"
            for n in p.recurse().notes:
                if not hasattr(n, "pitch") or n.pitch is None:
                    continue
                ql_raw = float(n.duration.quarterLength)
                if ql_raw < MIN_DURATION:
                    continue
                try:
                    absolute_offset = float(n.getOffsetInHierarchy(p))
                except Exception:
                    absolute_offset = float(n.offset)
                offset = _snap(absolute_offset)
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

        # Step 3: build output parts
        use_skeleton = source_score is not None and bool(source_score.parts)
        if use_skeleton:
            upper = _build_skeleton_part(source_score, "Reeds (upper)", music21.clef.TrebleClef())
            lower = _build_skeleton_part(source_score, "Reeds (lower)", music21.clef.BassClef())
        else:
            upper = music21.stream.Part()
            upper.partName = "Reeds (upper)"
            upper.insert(0, music21.clef.TrebleClef())
            lower = music21.stream.Part()
            lower.partName = "Reeds (lower)"
            lower.insert(0, music21.clef.BassClef())

        # Step 4: distribute 2+3, collapse same-onset events per voice
        # (M4.2d), clip cross-onset overlaps per voice (M4.2e), then insert.
        upper_events: list[tuple[float, list[str], float]] = []
        lower_events: list[tuple[float, list[str], float]] = []
        for offset_key in sorted(onset_groups.keys()):
            events = sorted(onset_groups[offset_key])
            top = events[: self.upper_voice_count]
            bottom = events[self.upper_voice_count : self.upper_voice_count + self.lower_voice_count]

            if top:
                pitch_names, duration = _collapse_onset_group(top)
                upper_events.append((top[0].offset, pitch_names, duration))
            if bottom:
                pitch_names, duration = _collapse_onset_group(bottom)
                lower_events.append((bottom[0].offset, pitch_names, duration))

        upper_events = _clip_overlaps(upper_events)
        lower_events = _clip_overlaps(lower_events)

        for onset, pitch_names, duration in upper_events:
            if use_skeleton:
                if not _insert_into_measure(upper, onset, duration, pitch_names):
                    _insert_part_level(upper, onset, duration, pitch_names)
            else:
                _insert_part_level(upper, onset, duration, pitch_names)

        for onset, pitch_names, duration in lower_events:
            if use_skeleton:
                if not _insert_into_measure(lower, onset, duration, pitch_names):
                    _insert_part_level(lower, onset, duration, pitch_names)
            else:
                _insert_part_level(lower, onset, duration, pitch_names)

        # Step 5: finalize notation
        if use_skeleton:
            for part_obj in (upper, lower):
                for measure in part_obj.getElementsByClass(music21.stream.Measure):
                    _fill_measure_rests(measure)
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
