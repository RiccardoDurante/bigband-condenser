"""Post-process a condensed Part by coalescing adjacent same-pitch notes.

The time-segmentation algorithm used by `_collect_events` / `_build_voice_elements`
opens a new segment whenever ANY source voice changes note. When two source
voices hold the same pitch across such a segment boundary (e.g. Soprano and
Alto both on D4 while Tenor 2 changes note), the result is TWO adjacent notes
with the same pitch that should have been ONE sustained note.

This post-processor fixes that by merging consecutive notes in the same
Voice (or at measure level) when:
  - end(n1) == start(n2)  (adjacent, no gap)
  - pitch set is identical
  - they are in the same containing stream

A real repeated-note articulation (tremolo, rearticulation) in the source
survives because it typically carries explicit sub-beat gaps or articulation
marks; the condenser output artefacts have exact-adjacent offsets which is
the signature we match on.
"""
from __future__ import annotations

_EPS = 1e-3


def _coalesce_notes_in_stream(stream):
    import music21
    notes = sorted(
        [n for n in stream.getElementsByClass(("Note", "Chord"))],
        key=lambda n: float(n.offset),
    )
    i = 0
    to_remove = []
    while i < len(notes) - 1:
        n1, n2 = notes[i], notes[i + 1]
        end1 = float(n1.offset) + float(n1.duration.quarterLength)
        start2 = float(n2.offset)
        if abs(end1 - start2) > _EPS:
            i += 1
            continue
        p1 = frozenset(p.midi for p in n1.pitches)
        p2 = frozenset(p.midi for p in n2.pitches)
        if p1 != p2 or not p1:
            i += 1
            continue
        new_dur = (start2 + float(n2.duration.quarterLength)) - float(n1.offset)
        n1.duration.quarterLength = new_dur
        to_remove.append(n2)
        notes.pop(i + 1)
    for n in to_remove:
        try:
            stream.remove(n)
        except Exception:
            pass


def coalesce_tied_pitches(part):
    """Coalesce adjacent same-pitch notes in every measure/voice of part.

    Returns the same part object (modified in place) for chaining.
    """
    for measure in part.recurse().getElementsByClass("Measure"):
        for voice in measure.getElementsByClass("Voice"):
            _coalesce_notes_in_stream(voice)
        _coalesce_notes_in_stream(measure)
    return part



def filter_micro_notes(part, min_duration=0.125):
    """Remove notes with quarter-length < min_duration.

    The time-segmentation algorithm can produce sub-32nd 'splinter' notes
    when multiple source voices change on sub-beat offsets. These are
    musical noise, never intentional in big band jazz (no real 32nds).
    Removing them before coalesce_tied_pitches lets coalesce properly
    merge the surviving notes into clean sustained durations.

    Returns the same part (modified in place) for chaining.
    """
    for measure in part.recurse().getElementsByClass("Measure"):
        for voice in measure.getElementsByClass("Voice"):
            _filter_in_stream(voice, min_duration)
        _filter_in_stream(measure, min_duration)
    return part


def _filter_in_stream(stream, min_duration):
    to_remove = []
    for n in stream.getElementsByClass(("Note", "Chord")):
        if float(n.duration.quarterLength) < min_duration - 1e-6:
            to_remove.append(n)
    for n in to_remove:
        try:
            stream.remove(n)
        except Exception:
            pass
