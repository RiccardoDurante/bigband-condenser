"""Reeds section condenser (M4-R1 + M4.1 metadata + M4.2 measure structure).

Scope cumulative:
- M4.0: scaffold condenser/
- M4-R1: split 2+3 by pitch, treble/bass
- M4.1: preserve initial key/time/tempo from source_score
- M4.2: clone measure structure (count, pickup, barlines, numbers) from
  source_score by deepcopy of first Part + content purge. Metadata (M4.1)
  come with the skeleton for free.

  M4.2b: notes crossing a barline are split into tied fragments, one per
  Measure (_insert_into_measure).
  M4.2c: gaps are filled per Measure with explicit Rests (_fill_measure_rests)
  instead of part.makeRests(fillGaps=True), which uses the TimeSignature bar
  length and ignores partial/pickup bars.
  M4.2d: simultaneous events in one voice at the same onset collapse into one
  Note (unison) or one Chord (_collapse_onset_group).
  M4.2e (D-030): a later onset in the same voice truncates the previous event
  (_clip_overlaps). Known lossy simplification, backlog FR-M4-E.

  BUGFIX M4.2f: Measure.duration is DERIVED from content by music21 and is
  recomputed after every insert(), so a duration restored with
  `m.duration.quarterLength = x` does not survive. Symptom: the first (short)
  event inserted into a Measure made it "short", every later event in that
  Measure was rejected and silently fell back to a Part-level insert (notes
  invisible inside the measure, no rests added). Fix: record
  (measure, start, length) ONCE from the source before purging and use that
  table as the single source of truth for placement and rest filling. A
  failed placement now raises RuntimeError instead of silently losing a note.

Known open issues (see WBS_M4 / CHANGE_LOG):
- FR-M4-D: events at the same onset with different durations are merged into
  one chord with the MAX duration, so shorter notes are held too long.
- Ranking considers only notes that START at an onset (not notes still
  sounding), so a lone low entry can land in the upper staff.

Determinism: tie-breaking by partName order (Charter P1); within a merged
chord, pitches are ordered by descending MIDI.
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

    Returns (skeleton, bounds). bounds is a list of
    (measure, absolute_start, length) for every Measure, recorded BEFORE the
    purge (BUGFIX M4.2f). It is the single source of truth for measure
    boundaries: never read measure.duration after content has been inserted.

    Preserved: Measure objects (numbers, pickup, barlines, inner time
    signatures), key signatures, tempo markings.
    Purged: Note, Rest, Chord, ChordSymbol, Dynamic, TextExpression,
    Instrument, Clef (we insert our own).
    """
    import music21

    if not source_score.parts:
        return None, []

    source_part = source_score.parts[0]
    skeleton = copy.deepcopy(source_part)
    skeleton.partName = name

    bounds = [
        (m, float(m.offset), float(m.duration.quarterLength))
        for m in skeleton.getElementsByClass(music21.stream.Measure)
    ]

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

    skeleton.insert(0, new_clef)
    return skeleton, bounds


def _collapse_onset_group(events: list[_OnsetNote]) -> tuple[list[str], float]:
    """Collapse simultaneous events destined for the same voice at the same
    onset (M4.2d). Identical pitches collapse to one; distinct pitches become
    one chord. Duration = max of the group (known limitation FR-M4-D).
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
    """M4.2e (D-030): events is a time-ordered list of (onset, pitch_names,
    duration) for ONE voice. If a later onset starts before the previous
    event ends, truncate the previous event at the later onset.
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
                result.pop()
        result.append((onset, pitches, duration))
    return result


def _make_element(pitch_names: list[str]):
    import music21

    if len(pitch_names) == 1:
        return music21.note.Note(pitch_names[0])
    return music21.chord.Chord(pitch_names)


def _insert_into_measure(bounds, offset: float, quarter_length: float, pitch_names: list[str]) -> bool:
    """Insert a Note/Chord spanning [offset, offset + quarter_length) into the
    Measures listed in `bounds`, splitting it across every Measure it overlaps
    with ties (M4.2b). offset is absolute in the Part.

    Returns True if at least one fragment was inserted, False if the span
    overlaps no Measure or an insert failed.
    """
    import music21

    span_start = offset
    span_end = offset + quarter_length

    fragments = []  # (measure, relative_offset, fragment_length)
    for measure, m_start, m_len in bounds:
        m_end = m_start + m_len
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


def _place_event(part, bounds, onset: float, duration: float, pitch_names: list[str]) -> None:
    """Place one event. With a skeleton (bounds is a list) a failed placement
    is an error: silently dropping a note violates 'no note lost'.
    """
    if bounds is None:
        _insert_part_level(part, onset, duration, pitch_names)
        return
    if not _insert_into_measure(bounds, onset, duration, pitch_names):
        raise RuntimeError(
            f"Cannot place {pitch_names} at offset {onset} (ql={duration}) in "
            f"{part.partName}: no matching measure in the skeleton"
        )


def _fill_measure_rests(measure, bar_len: float) -> None:
    """Fill the gaps in `measure` with explicit Rests up to bar_len (the length
    recorded from the source, NOT measure.duration) (M4.2c, M4.2f).
    """
    import music21

    if bar_len <= _GAP_EPS:
        return

    notes = sorted(measure.notes, key=lambda n: float(n.offset))
    cursor = 0.0
    for n in notes:
        n_start = float(n.offset)
        if n_start > cursor + _GAP_EPS:
            r = music21.note.Rest()
            r.duration.quarterLength = n_start - cursor
            measure.insert(cursor, r)
        n_end = n_start + float(n.duration.quarterLength)
        if n_end > cursor:
            cursor = n_end

    if cursor < bar_len - _GAP_EPS:
        r = music21.note.Rest()
        r.duration.quarterLength = bar_len - cursor
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

        # Step 4: distribute 2+3, collapse same-onset events per voice,
        # clip cross-onset overlaps per voice, then place.
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
            _place_event(upper, upper_bounds, onset, duration, pitch_names)
        for onset, pitch_names, duration in lower_events:
            _place_event(lower, lower_bounds, onset, duration, pitch_names)

        # Step 5: finalize notation
        if use_skeleton:
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
