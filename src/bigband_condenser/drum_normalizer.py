"""Drum notation normalizer (M7 Z — simplified heuristic, Opzione 1).

Does NOT remap display positions (no composer-specific mapping table).
Only applies notehead and stem conventions based on display octave:

  display octave >= 5           -> notehead=x, stem=up    (cymbal / hi-hat zone)
  display octave <= 4           -> notehead=normal         (drum zone)
  size="full" (any position)   -> notehead=slash, stem=up (ensemble cue;
                                   overrides the octave rule)

Rationale (Music Expert decision 2026-11-01, Opzione 1):
A full composer->Weinberg mapping would need per-display translation
which we do not have. The simplified heuristic puts an X head on the
cymbal/hi-hat zone and a slash head on cues, which is the Weinberg
convention; drum-zone notes keep their written position so the drummer
reads the figure the composer wrote. Imperfect: if a cymbal in the source
is written in a low position, it still appears low (with X head).
A proper mapping is backlog FR-M7-D for post-v1.

Idempotent: a non-normal notehead signals "already normalized".
"""
from __future__ import annotations


def _is_cue_sized(note):
    try:
        return bool(note.style and note.style.noteSize == "full")
    except Exception:
        return False


def normalize_drum_notation(drum_part):
    """In-place application of the simplified heuristic.
    Timing (offset, duration) and display position are preserved."""
    import music21

    changed = 0
    for n in drum_part.recurse().notes:
        if not isinstance(n, music21.note.Unpitched):
            continue
        current_nh = getattr(n, "notehead", "normal")
        if current_nh and current_nh != "normal":
            continue
        octave = n.displayOctave
        if octave is None:
            continue

        if _is_cue_sized(n):
            try:
                n.notehead = "slash"
            except Exception:
                pass
            try:
                n.stemDirection = "up"
            except Exception:
                pass
            try:
                if n.style and n.style.noteSize is not None:
                    n.style.noteSize = None
            except Exception:
                pass
            changed += 1
        elif octave >= 5:
            try:
                n.notehead = "x"
            except Exception:
                pass
            try:
                n.stemDirection = "up"
            except Exception:
                pass
            changed += 1
        # octave <= 4: leave notehead=normal (default), do not touch
    return changed
