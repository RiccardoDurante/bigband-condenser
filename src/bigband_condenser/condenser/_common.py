"""Shared infrastructure for section condensers.

All generic helpers live here. Section-specific modules (reeds.py,
brass.py, ...) import from this module and add:
- abbreviation dict (part_name -> short label)
- default rank table (part_name -> int, for crossing detection when applicable)
- family_map dict (part_name -> "treble"|"bass") when the section wants
  family-based routing instead of pitch-based global ranking
- a SectionCondenser subclass with the right upper_voice_count /
  lower_voice_count and the call into _annotate_cast_changes with the
  right abbr / default_rank / enable_crossings.
"""
from __future__ import annotations

import copy
import warnings
from bisect import bisect_right
from dataclasses import dataclass, replace

_GAP_EPS = 1e-6
MIN_DURATION = 0.0625
_SNAP_GRID = 0.125
_MIN_CAST_DURATION_QL = 4.0
_LABEL_FONT_SIZE = 4


def _snap(value: float) -> float:
    return round(value / _SNAP_GRID) * _SNAP_GRID


@dataclass(frozen=True)
class _Ev:
    eid: int
    part_name: str
    midi: int
    pitch_name: str
    start: float
    end: float


@dataclass(frozen=True)
class _Slot:
    pitch_name: str
    midi: int
    cont_prev: bool
    cont_next: bool


def _collect_events(concert_parts) -> list[_Ev]:
    """One event per sounding pitch. Each source part is treated as monophonic
    per start time: an event overlapping the NEXT start of the same part is
    clipped there (D-022: notation > MIDI playback artifacts)."""
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


def _build_voice_elements(events, upper_count, lower_count, family_map=None):
    """Sounding-set segmentation. Two routing modes:
    - family_map None: global pitch ranking (reeds). upper_count/lower_count
      pick the top-K sounding voices.
    - family_map dict (part_name -> 'treble'|'bass'): routing by family.
      Within each staff the active voices are pitch-ranked, then truncated
      at upper_count/lower_count. Use a large count to preserve everyone."""
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
        if family_map is None:
            ranked = sorted(active, key=lambda e: (-e.midi, e.part_name, e.eid))
            top = ranked[:upper_count]
            bottom = ranked[upper_count : upper_count + lower_count]
        else:
            treble = [e for e in active if family_map.get(e.part_name) == "treble"]
            bass = [e for e in active if family_map.get(e.part_name) == "bass"]
            top = sorted(treble, key=lambda e: (-e.midi, e.part_name, e.eid))[:upper_count]
            bottom = sorted(bass, key=lambda e: (-e.midi, e.part_name, e.eid))[:lower_count]
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
    Returns (skeleton, bounds); bounds = [(measure, start, length)] from BEFORE
    the purge (M4.2f: measure.duration is derived from content and collapses)."""
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
    """Insert spanning element with barline splitting + ties (M4.2b)."""
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
    if bounds is None:
        _insert_part_level(part, onset, duration, slots)
        return
    if not _insert_into_measure(bounds, onset, duration, slots):
        raise RuntimeError(
            f"Cannot place {[s.pitch_name for s in slots]} at offset {onset} "
            f"(ql={duration}) in {part.partName}: no matching measure"
        )


def _fill_measure_rests(measure, bar_len: float) -> None:
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


# ========== M4.7 + M4.8: cast tracking, labels, crossing markers ==========

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


def _split_for_label(cast, midis, upper_count, lower_count, family_map=None):
    if family_map is None:
        ranked = sorted(cast, key=lambda p: (-midis.get(p, 0), p))
        return (tuple(ranked[:upper_count]),
                tuple(ranked[upper_count:upper_count + lower_count]))
    treble = sorted(
        [p for p in cast if family_map.get(p) == "treble"],
        key=lambda p: (-midis.get(p, 0), p),
    )
    bass = sorted(
        [p for p in cast if family_map.get(p) == "bass"],
        key=lambda p: (-midis.get(p, 0), p),
    )
    return tuple(treble[:upper_count]), tuple(bass[:lower_count])


def _format_cast_annotations(cast, parts_order, is_unison, abbr,
                              upper_split, lower_split, family_map=None):
    ordered = [p for p in parts_order if p in cast]
    if len(ordered) == 1:
        name = ordered[0]
        label = abbr.get(name, name)
        if family_map is not None and family_map.get(name) == "bass":
            return [("lower", "below", label)]
        return [("upper", "above", label)]
    if len(ordered) == len(parts_order) and not is_unison:
        return [("upper", "above", "Tutti")]
    out = []
    upper_in_order = [p for p in parts_order if p in upper_split]
    lower_in_order = [p for p in parts_order if p in lower_split]
    if upper_in_order:
        out.append(("upper", "above", "\n".join(abbr.get(n, n) for n in upper_in_order)))
    if lower_in_order:
        out.append(("lower", "below", "\n".join(abbr.get(n, n) for n in lower_in_order)))
    return out


def _detect_crossings(upper_split, lower_split, default_rank, upper_count):
    out = []
    for p in upper_split:
        rank = default_rank.get(p)
        if rank is not None and rank > upper_count:
            out.append((p, "up"))
    for p in lower_split:
        rank = default_rank.get(p)
        if rank is not None and rank <= upper_count:
            out.append((p, "down"))
    return out


def _format_crossing_marker(part_name, direction, abbr):
    arrow = ">" if direction == "up" else "<"
    return f"{abbr.get(part_name, part_name)}{arrow}"


def _insert_text_direction(part, bounds, abs_offset, text, placement, font_size):
    import music21
    for measure, m_start, m_len in bounds:
        if m_start - _GAP_EPS <= abs_offset < m_start + m_len - _GAP_EPS:
            te = music21.expressions.TextExpression(text)
            te.placement = placement
            try:
                te.style.fontSize = font_size
            except Exception:
                pass
            try:
                measure.insert(abs_offset - m_start, te)
            except Exception:
                pass
            return True
    return False


def _annotate_cast_changes(upper_part, upper_bounds, lower_part, lower_bounds,
                           events, parts_order, upper_count, lower_count,
                           abbr, default_rank,
                           min_duration=_MIN_CAST_DURATION_QL,
                           font_size=_LABEL_FONT_SIZE,
                           enable_crossings=True,
                           family_map=None):
    """M4.7 cast-change labels + M4.8 voice-crossing markers (optional).
    When family-based routing is used (brass), set enable_crossings=False."""
    segments = _filter_cast_segments(_build_cast_segments(events), min_duration)
    for a, _b, cast, is_unison, midis in segments:
        upper_split, lower_split = _split_for_label(cast, midis, upper_count, lower_count, family_map)
        for staff, placement, label in _format_cast_annotations(
            cast, parts_order, is_unison, abbr, upper_split, lower_split, family_map
        ):
            if not label:
                continue
            if staff == "upper":
                _insert_text_direction(upper_part, upper_bounds, a, label, placement, font_size)
            else:
                _insert_text_direction(lower_part, lower_bounds, a, label, placement, font_size)
        if enable_crossings and len(cast) >= 2:
            for part_name, direction in _detect_crossings(
                upper_split, lower_split, default_rank, upper_count
            ):
                marker = _format_crossing_marker(part_name, direction, abbr)
                if direction == "up":
                    _insert_text_direction(upper_part, upper_bounds, a, marker, "above", font_size)
                else:
                    _insert_text_direction(lower_part, lower_bounds, a, marker, "below", font_size)
