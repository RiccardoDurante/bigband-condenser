"""Reeds section condenser (M4-R1 + M4.1 metadata + M4.2 measure structure
+ M4.4 sounding-set segmentation).

Pipeline:
1. Collect every source note as an event (concert pitch, snapped to a 0.125
   grid, sub-semiquaver artifacts filtered: D-022).
2. Segment time at every note start/end. In each segment, rank the SOUNDING
   notes (including notes still held from earlier) by pitch: the top
   upper_voice_count go to the upper staff, the next lower_voice_count to the
   lower staff (D-028). Ties are broken by part name (Charter P1).
3. Per voice, merge consecutive segments with identical note sets (a held
   chord stays one long chord). Where the set changes, notes that continue
   are tied note-by-note; re-attacks of the same pitch are not tied.
4. Place the resulting chords in the cloned Measure skeleton, splitting them
   across barlines with ties (M4.2b), then fill gaps with explicit rests
   (M4.2c) using the measure lengths recorded from the SOURCE (M4.2f).

This replaces the onset-only ranking, same-onset collapse (max duration) and
cross-onset truncation (D-030) of earlier versions: they lost sustained
durations, held short notes too long and sent lone low entries to the upper
staff (found by scripts/check_fidelity.py, 5/33 measures failing).

M4.2f: music21 derives Measure.duration from content and recomputes it after
every insert(), so measure lengths are recorded ONCE from the source before
the purge and used as the single source of truth. A failed placement raises
RuntimeError instead of silently losing a note.

Known limitations (backlog):
- FR-M4-F: if a sustained note changes staff between segments (rank change),
  it is restated in the new staff without a tie (looks like a re-attack).
- FR-M4-A: no adaptive clef when a voice sits very low/high in its staff.
- FR-M4-B: enharmonic spelling is taken from the first part (by name) that
  sounds that pitch.

Determinism: all orderings use (pitch, part name, event id).
"""
from __future__ import annotations

import copy
import warnings
from bisect import bisect_right
from dataclasses import dataclass, replace

from bigband_condenser.condenser.base import SectionCondenser

_GAP_EPS = 1e-6
MIN_DURATION = 0.0625
_SNAP_GRID = 0.125


def _snap(value: float) -> float:
    return round(value / _SNAP_GRID) * _SNAP_GRID


@dataclass(frozen=True)
class _Ev:
    """One source note: sounds from start to end (quarter lengths, absolute)."""
    eid: int
    part_name: str
    midi: int
    pitch_name: str
    start: float
    end: float


@dataclass(frozen=True)
class _Slot:
    """One pitch inside an output chord, with tie continuity flags."""
    pitch_name: str
    midi: int
    cont_prev: bool
    cont_next: bool


def _collect_events(concert_parts) -> list[_Ev]:
    """One event per sounding pitch. Each source part is treated as monophonic
    per start time: an event overlapping the NEXT start of the same part is
    clipped there (legato overlaps and snap rounding are playback artifacts,
    D-022; a sax cannot sustain two successive notes)."""
    events: list[_Ev] = []
    eid = 0
    for p in concert_parts:
        part_name = p.partName or "<unnamed>"
        part_events: list[_Ev] = []
        for n in p.recurse().notes:
            ql_raw = float(n.duration.quarterLength)
            if ql_raw < MIN_DURATION:
                continue
            try:
                absolute = float(n.getOffsetInHierarchy(p))
            except Exception:
                absolute = float(n.offset)
            start = _snap(absolute)
            ql = _snap(ql_raw)
            if ql <= 0:
                continue
            for pitch in getattr(n, "pitches", ()):
                part_events.append(
                    _Ev(eid, part_name, pitch.midi, pitch.nameWithOctave, start, start + ql)
                )
                eid += 1
        starts = sorted({e.start for e in part_events})
        for e in part_events:
            i = bisect_right(starts, e.start)
            if i < len(starts) and e.end > starts[i] + _GAP_EPS:
                e = replace(e, end=starts[i])
            events.append(e)
    return events


def _merge_segments(segs):
    """segs: time-ordered (a, b, events). Merge contiguous segments whose
    event sets are identical. Returns (a, b, events, frozenset_of_ids)."""
    merged = []
    for a, b, evs in segs:
        ids = frozenset(e.eid for e in evs)
        if merged and merged[-1][1] == a and merged[-1][3] == ids:
            pa, _pb, pevs, pids = merged[-1]
            merged[-1] = (pa, b, pevs, pids)
        else:
            merged.append((a, b, evs, ids))
    return merged


def _to_elements(merged):
    """Turn merged segments into (onset, duration, slots) with tie flags."""
    out = []
    for i, (a, b, evs, _ids) in enumerate(merged):
        by_midi: dict[int, list[_Ev]] = {}
        for e in evs:
            by_midi.setdefault(e.midi, []).append(e)
        prev_contig = i > 0 and merged[i - 1][1] == a
        next_contig = i + 1 < len(merged) and merged[i + 1][0] == b
        slots = []
        for midi in sorted(by_midi, reverse=True):
            group = by_midi[midi]
            ids_here = {e.eid for e in group}
            cont_prev = prev_contig and any(
                e.eid in ids_here for e in merged[i - 1][2] if e.midi == midi
            )
            cont_next = next_contig and any(
                e.eid in ids_here for e in merged[i + 1][2] if e.midi == midi
            )
            name = min(group, key=lambda e: (e.part_name, e.eid)).pitch_name
            slots.append(_Slot(name, midi, cont_prev, cont_next))
        out.append((a, b - a, slots))
    return out


def _build_voice_elements(events: list[_Ev], upper_count: int, lower_count: int):
    """Sounding-set segmentation. Returns (upper_elements, lower_elements),
    each a time-ordered list of (onset, duration, slots)."""
    if not events:
        return [], []

    points = sorted({e.start for e in events} | {e.end for e in events})
    by_start = sorted(events, key=lambda e: (e.start, e.eid))
    active: list[_Ev] = []
    idx = 0
    upper_segs, lower_segs = [], []
    for a, b in zip(points, points[1:]):
        while idx < len(by_start) and by_start[idx].start <= a:
            active.append(by_start[idx])
            idx += 1
        active = [e for e in active if e.end > a]
        if not active:
            continue
        ranked = sorted(active, key=lambda e: (-e.midi, e.part_name, e.eid))
        top = ranked[:upper_count]
        bottom = ranked[upper_count : upper_count + lower_count]
        if top:
            upper_segs.append((a, b, tuple(top)))
        if bottom:
            lower_segs.append((a, b, tuple(bottom)))

    return (
        _to_elements(_merge_segments(upper_segs)),
        _to_elements(_merge_segments(lower_segs)),
    )


def _tie_type(has_prev: bool, has_next: bool):
    if has_prev and has_next:
        return "continue"
    if has_next:
        return "start"
    if has_prev:
        return "stop"
    return None


def _build_element(slots, frag_index: int = 0, frag_count: int = 1):
    """Note (1 slot) or Chord (several), with per-note ties. A note is tied to
    the previous fragment if this is not the first barline fragment or the
    slot continues from the previous chord; likewise for the next."""
    import music21

    names = [s.pitch_name for s in slots]
    el = music21.note.Note(names[0]) if len(names) == 1 else music21.chord.Chord(names)

    tie_by_midi = {}
    for s in slots:
        has_prev = frag_index > 0 or s.cont_prev
        has_next = frag_index < frag_count - 1 or s.cont_next
        t = _tie_type(has_prev, has_next)
        if t:
            tie_by_midi[s.midi] = t
    if tie_by_midi:
        members = [el] if len(names) == 1 else list(el.notes)
        for m in members:
            t = tie_by_midi.get(m.pitch.midi)
            if t:
                m.tie = music21.tie.Tie(t)
    return el


def _build_skeleton_part(source_score, name: str, new_clef):
    """Deepcopy source_score.parts[0] with musical content purged.

    Returns (skeleton, bounds); bounds = [(measure, absolute_start, length)]
    recorded BEFORE the purge (M4.2f). Preserved: Measures (numbers, pickup,
    barlines, inner time signatures), key signatures, tempo markings.
    Purged: notes, rests, chords, chord symbols, dynamics, text, instruments,
    clefs (we insert our own).
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


def _insert_into_measure(bounds, offset: float, quarter_length: float, slots) -> bool:
    """Insert a chord spanning [offset, offset + quarter_length) into the
    Measures in `bounds`, splitting across barlines with ties (M4.2b).
    Returns False if the span overlaps no Measure or an insert fails."""
    span_start = offset
    span_end = offset + quarter_length

    fragments = []
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

    frag_count = len(fragments)
    for i, (measure, rel_offset, frag_ql) in enumerate(fragments):
        el = _build_element(slots, i, frag_count)
        el.duration.quarterLength = frag_ql
        try:
            measure.insert(rel_offset, el)
        except Exception:
            return False
    return True


def _insert_part_level(part, offset: float, quarter_length: float, slots) -> None:
    el = _build_element(slots)
    el.duration.quarterLength = quarter_length
    part.insert(offset, el)


def _place_event(part, bounds, onset: float, duration: float, slots) -> None:
    """With a skeleton (bounds is a list) a failed placement is an error:
    silently dropping a note violates 'no note lost'."""
    if bounds is None:
        _insert_part_level(part, onset, duration, slots)
        return
    if not _insert_into_measure(bounds, onset, duration, slots):
        raise RuntimeError(
            f"Cannot place {[s.pitch_name for s in slots]} at offset {onset} "
            f"(ql={duration}) in {part.partName}: no matching measure"
        )


def _fill_measure_rests(measure, bar_len: float) -> None:
    """Fill gaps with explicit Rests up to bar_len, the length recorded from
    the source (NOT measure.duration) (M4.2c, M4.2f)."""
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

        # Step 1: concert pitch
        concert_parts = []
        for p in parts:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                concert_parts.append(p.toSoundingPitch(inPlace=False))

        # Step 2: events -> sounding-set segmentation -> per-voice chords
        events = _collect_events(concert_parts)
        upper_elems, lower_elems = _build_voice_elements(
            events, self.upper_voice_count, self.lower_voice_count
        )

        # Step 3: output parts (skeleton clones when source_score is given)
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

        # Step 4: place
        for onset, duration, slots in upper_elems:
            _place_event(upper, upper_bounds, onset, duration, slots)
        for onset, duration, slots in lower_elems:
            _place_event(lower, lower_bounds, onset, duration, slots)

        # Step 4.5 (M4.7): cast-change text directions on both staves
        if use_skeleton:
            parts_order = [p.partName or "<unnamed>" for p in parts]
            _annotate_cast_changes(
                upper, upper_bounds, lower, lower_bounds,
                events, parts_order,
                self.upper_voice_count, self.lower_voice_count,
            )

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
# ========== M4.7: cast-change text directions ==========

_ABBR_REEDS = {
    "Soprano Sax": "S.Sx",
    "Alto Sax": "A.Sx",
    "Tenor Sax 1": "T.Sx 1",
    "Tenor Sax 2": "T.Sx 2",
    "Baritone Sax": "Bar.Sx",
}
_MIN_CAST_DURATION_QL = 4.0  # one bar in 4/4; shorter segments annotated only when unison
_LABEL_FONT_SIZE = 4  # Music Expert: at least half the editor default (~10-12 pt)


def _cast_at(events, t):
    cast = set()
    midis = {}
    for e in events:
        if e.start <= t + _GAP_EPS and e.end > t + _GAP_EPS:
            cast.add(e.part_name)
            if e.part_name not in midis:
                midis[e.part_name] = e.midi
    return frozenset(cast), midis


def _build_cast_segments(events):
    if not events:
        return []
    points = sorted({e.start for e in events} | {e.end for e in events})
    raw = []
    for a, b in zip(points, points[1:]):
        if b - a <= _GAP_EPS:
            continue
        cast, midis = _cast_at(events, a + _GAP_EPS)
        if not cast:
            continue
        is_unison = len(midis) >= 2 and len(set(midis.values())) == 1
        raw.append((a, b, cast, is_unison, midis))
    merged = []
    for s in raw:
        if merged and abs(merged[-1][1] - s[0]) <= _GAP_EPS and merged[-1][2] == s[2]:
            pa, _pb, pc, pu, pm = merged[-1]
            merged[-1] = (pa, s[1], pc, pu, pm)
        else:
            merged.append(s)
    return merged


def _filter_cast_segments(segments, min_duration=_MIN_CAST_DURATION_QL):
    return [s for s in segments if (s[1] - s[0]) >= min_duration - _GAP_EPS or s[3]]


def _split_for_label(cast, midis, upper_count, lower_count):
    """Rank parts in cast by MIDI descending (ties by name) and partition
    them with the condenser 2+3 sizes. Returns (upper_tuple, lower_tuple)."""
    ranked = sorted(cast, key=lambda p: (-midis.get(p, 0), p))
    return tuple(ranked[:upper_count]), tuple(ranked[upper_count:upper_count + lower_count])


def _format_cast_annotations(cast, parts_order, is_unison, abbr,
                              upper_split, lower_split):
    """Return list of (staff, placement, label):
      - 1 part        -> [(upper, above, name)]
      - 5 parts, not unison -> [(upper, above, 'Tutti')]
      - else          -> column split BELOW upper + ABOVE lower.
    Within each half, names follow the Score part order."""
    ordered = [p for p in parts_order if p in cast]
    if len(ordered) == 1:
        return [("upper", "above", abbr.get(ordered[0], ordered[0]))]
    if len(ordered) == 5 and not is_unison:
        return [("upper", "above", "Tutti")]
    out = []
    upper_in_order = [p for p in parts_order if p in upper_split]
    lower_in_order = [p for p in parts_order if p in lower_split]
    if upper_in_order:
        out.append(("upper", "above", "\n".join(abbr.get(n, n) for n in upper_in_order)))
    if lower_in_order:
        out.append(("lower", "below", "\n".join(abbr.get(n, n) for n in lower_in_order)))
    return out


def _annotate_cast_changes(upper_part, upper_bounds, lower_part, lower_bounds,
                           events, parts_order, upper_count, lower_count,
                           abbr=None, min_duration=_MIN_CAST_DURATION_QL,
                           font_size=_LABEL_FONT_SIZE):
    """Insert cast-change TextExpressions on both staves. Column halves are
    placed below the upper staff and above the lower staff so the full
    column reads vertically between the two staves. Dorico should render
    newline-separated names as a column; if it does not, swap the join
    separator for ' / ' and the layout becomes inline."""
    import music21
    if abbr is None:
        abbr = _ABBR_REEDS
    segments = _filter_cast_segments(_build_cast_segments(events), min_duration)
    for a, _b, cast, is_unison, midis in segments:
        upper_split, lower_split = _split_for_label(cast, midis, upper_count, lower_count)
        annotations = _format_cast_annotations(
            cast, parts_order, is_unison, abbr, upper_split, lower_split
        )
        for staff, placement, label in annotations:
            if not label:
                continue
            target_part = upper_part if staff == "upper" else lower_part
            target_bounds = upper_bounds if staff == "upper" else lower_bounds
            for measure, m_start, m_len in target_bounds:
                if m_start - _GAP_EPS <= a < m_start + m_len - _GAP_EPS:
                    te = music21.expressions.TextExpression(label)
                    te.placement = placement
                    try:
                        te.style.fontSize = font_size
                    except Exception:
                        pass
                    try:
                        measure.insert(a - m_start, te)
                    except Exception:
                        pass
                    break
