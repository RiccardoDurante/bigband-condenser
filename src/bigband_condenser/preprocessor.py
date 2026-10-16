"""Preprocessor for Big Band Condenser v1.

Applies all pre-write mitigations identified during Spike M2:
- R28: strip hidden parts (playback-only, must not reach condensed output)
- R30: force correct music21 instrument class pre-write (otherwise music21
  regenerates <transpose> from wrong class, corrupting output)
- R27: filter sub-semicroma events in drum parts (realistic playback MIDI
  artifacts, see D-022 principle: notation > MIDI playback)

Design: operates on a parsed music21 Score (in-memory), returning either a new
Score or mutating in-place. Does NOT touch condensation logic (M4-M6 scope).

API:
    preprocess(score, xml_path) -> ProcessedScore
        One-shot pipeline that applies all three mitigations.
    strip_hidden_parts(score, hidden_names) -> int
    force_instrument_classes(score) -> int
    filter_sub_semicroma_drums(score, threshold=0.25) -> int

Each individual function returns the count of elements changed, for logging
and verification.
"""
from __future__ import annotations

import warnings
from dataclasses import dataclass, field
from pathlib import Path

from bigband_condenser.classifier import detect_hidden_part_names
from bigband_condenser.instrument_mapping import get_music21_instrument_class


# Semicroma threshold: durations strictly less than this quarterLength are
# considered realistic-playback MIDI artifacts, not notation. See D-022.
SEMICROMA_QL = 0.25


@dataclass
class ProcessedScore:
    """Result of running preprocess() on a Score.

    Attributes:
        score: The (mutated) music21 Score object.
        hidden_names: Set of partNames stripped as hidden.
        parts_stripped: Count of music21 Part objects removed.
        classes_forced: Count of parts where instrument class was replaced.
        drum_notes_filtered: Count of sub-semicroma events removed from drum parts.
        warnings: Non-fatal issues to report.
    """
    score: object  # music21.stream.Score (not typed to avoid heavy import)
    hidden_names: set[str] = field(default_factory=set)
    parts_stripped: int = 0
    classes_forced: int = 0
    drum_notes_filtered: int = 0
    warnings: list[str] = field(default_factory=list)


def strip_hidden_parts(score, hidden_names: set[str]) -> int:
    """Remove parts whose partName is in hidden_names. Returns count removed."""
    to_remove = [p for p in score.parts if (p.partName or "") in hidden_names]
    for p in to_remove:
        score.remove(p)
    return len(to_remove)


def force_instrument_classes(score) -> int:
    """Replace music21 instrument class of each part with the correct one
    based on partName lookup. Returns count of parts modified.

    Mitigation for R30: music21.write() regenerates <transpose> from the
    internal instrument class. Mis-classified parts (R26) get corrupted output.
    By forcing the correct class before write, we ensure the right transpose
    tag is emitted.

    Parts whose partName is not in the mapping table are left untouched
    (music21 will preserve the source <transpose> tag if the inferred class
    has no default transposition).
    """
    import music21
    count = 0
    for part in score.parts:
        name = part.partName or ""
        correct_cls = get_music21_instrument_class(name)
        if correct_cls is None:
            continue
        # Remove existing Instrument objects and insert the correct one
        existing = list(part.getElementsByClass(music21.instrument.Instrument))
        for inst in existing:
            part.remove(inst)
        part.insert(0, correct_cls())
        count += 1
    return count


def filter_sub_semicroma_drums(score, threshold: float = SEMICROMA_QL) -> int:
    """Remove notes/rests with duration strictly < threshold from drum parts.

    Drum parts identified by partName containing 'drum' or 'percuss'
    (case-insensitive). Threshold defaults to semicroma (0.25 quarterLength),
    see D-022: notational drum values rarely go below semicroma; shorter
    durations in Finale export are realistic-playback MIDI artifacts.

    Returns count of events removed.
    """
    filtered = 0
    for part in score.parts:
        name = (part.partName or "").lower()
        if "drum" not in name and "percuss" not in name:
            continue
        for note_or_rest in list(part.recurse().notesAndRests):
            try:
                if note_or_rest.duration.quarterLength < threshold:
                    site = note_or_rest.activeSite
                    if site is not None:
                        site.remove(note_or_rest)
                        filtered += 1
            except Exception:
                continue
    return filtered


def preprocess(score, xml_path: Path | str) -> ProcessedScore:
    """Apply the full preprocessing pipeline to a parsed Score.

    Order matters:
    1. Detect hidden parts (via XML parse of source, NOT via music21)
    2. Strip hidden parts from Score
    3. Force correct instrument classes on remaining parts
    4. Filter sub-semicroma events from drum parts

    Args:
        score: Parsed music21 Score (will be mutated).
        xml_path: Path to the ORIGINAL MusicXML source file. Needed for
                  hidden detection, which reads XML directly (music21
                  does not expose <staff-details print-object="no"/>).

    Returns:
        ProcessedScore with the mutated Score and per-step counts.
    """
    result = ProcessedScore(score=score)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result.hidden_names = detect_hidden_part_names(xml_path)
        result.parts_stripped = strip_hidden_parts(score, result.hidden_names)
        result.classes_forced = force_instrument_classes(score)
        result.drum_notes_filtered = filter_sub_semicroma_drums(score)
    return result
