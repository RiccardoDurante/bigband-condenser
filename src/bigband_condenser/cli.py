"""Big Band Condenser - command-line entry point (M8.1).

Usage:
    bbcondenser input.musicxml -o output.musicxml

Pipeline:
    1. Parse MusicXML source
    2. preprocess() - strip hidden parts, force instrument classes, filter MIDI artifacts
    3. classify_score() - identify Reeds / Brass / Rhythm / Drums parts
    4. Condense each section:
         Reeds   -> treble + bass staves
         Brass   -> treble + bass staves (family-based routing)
         Rhythm  -> treble + bass staves (with chord symbols + slash notation
                   from <measure-style> + piano ensemble cues)
         Drums   -> single percussion staff (Weinberg/PAS standard)
    5. Assemble all output Parts into a single Score (up to 7 Parts: 3 x 2 + 1)
    6. Write MusicXML + run post-write sanitizer
"""
from __future__ import annotations

import argparse
import sys
import warnings
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="bbcondenser",
        description="Transform a big band MusicXML score into a condensed 4-system score.",
    )
    parser.add_argument(
        "input", type=Path,
        help="Path to the input big band MusicXML file.",
    )
    parser.add_argument(
        "-o", "--output", type=Path, required=True,
        help="Path to the output condensed MusicXML file.",
    )
    args = parser.parse_args(argv)

    if not args.input.exists():
        print(f"ERROR: input file not found: {args.input}", file=sys.stderr)
        return 2

    _log(f"Loading {args.input.name} ...")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        from music21 import converter
        score = converter.parse(str(args.input))

    _log("Preprocessing ...")
    from bigband_condenser.preprocessor import preprocess
    result = preprocess(score, args.input)
    _log(
        f"  parts stripped: {result.parts_stripped}, "
        f"classes forced: {result.classes_forced}, "
        f"drum notes filtered: {result.drum_notes_filtered}"
    )

    _log("Classifying parts ...")
    from bigband_condenser.classifier import (
        classify_score,
        SECTION_REEDS, SECTION_BRASS, SECTION_RHYTHM, SECTION_DRUMS,
    )
    classifications = classify_score(args.input)

    def pick(section):
        names = {c.part_name for c in classifications
                 if c.section == section and not c.is_hidden}
        return [p for p in result.score.parts if (p.partName or "") in names]

    reed_parts = pick(SECTION_REEDS)
    brass_parts = pick(SECTION_BRASS)
    rhythm_parts = pick(SECTION_RHYTHM)
    drum_parts = pick(SECTION_DRUMS)

    # Piano may be hidden in the source (= lead sheet convention: only chord
    # symbols matter) but still provides the chord source for Rhythm.
    piano_parts = [p for p in result.score.parts
                   if "piano" in (p.partName or "").lower()]
    for p in piano_parts:
        if p not in rhythm_parts:
            rhythm_parts.append(p)

    _log(
        f"  reeds: {len(reed_parts)}, brass: {len(brass_parts)}, "
        f"rhythm: {len(rhythm_parts)}, drums: {len(drum_parts)}"
    )

    _log("Condensing sections ...")
    from bigband_condenser.condenser import (
        ReedsCondenser, BrassCondenser, RhythmCondenser, DrumsCondenser,
    )
    output_parts = []

    if reed_parts:
        upper, lower = ReedsCondenser().condense(reed_parts, source_score=result.score)
        output_parts.extend([upper, lower])
        _log(f"  Reeds: {_count_notes(upper)} + {_count_notes(lower)} notes")

    if brass_parts:
        upper, lower = BrassCondenser().condense(brass_parts, source_score=result.score)
        output_parts.extend([upper, lower])
        _log(f"  Brass: {_count_notes(upper)} + {_count_notes(lower)} notes")

    if rhythm_parts:
        upper, lower = RhythmCondenser(source_xml_path=args.input).condense(
            rhythm_parts, source_score=result.score
        )
        output_parts.extend([upper, lower])
        _log(f"  Rhythm: {_count_notes(upper)} + {_count_notes(lower)} notes")

    if drum_parts:
        upper, _ = DrumsCondenser(source_xml_path=args.input).condense(
            drum_parts, source_score=result.score
        )
        output_parts.append(upper)
        _log(f"  Drums: {_count_notes(upper)} notes")

    if not output_parts:
        print("ERROR: no parts were produced (no sections matched)", file=sys.stderr)
        return 3

    _log(f"Assembling output score with {len(output_parts)} parts ...")
    from music21 import stream, metadata
    out = stream.Score()
    if score.metadata is not None:
        out.metadata = metadata.Metadata()
        out.metadata.title = score.metadata.title or args.input.stem
        if getattr(score.metadata, "movementName", None):
            out.metadata.movementName = f"{score.metadata.movementName} - Condensed"
        if getattr(score.metadata, "composer", None):
            out.metadata.composer = score.metadata.composer
    for p in output_parts:
        out.insert(0, p)

    _log(f"Writing {args.output.name} ...")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        out.write("musicxml", fp=str(args.output))

    # Post-write MusicXML sanitizer (R32 fix: unhide rests mangled by music21 writer)
    try:
        from bigband_condenser import musicxml_sanitizer as ms
        unhid = None
        for fname in ("sanitize", "sanitize_file", "unhide_rests",
                      "fix_rest_visibility", "apply", "run"):
            fn = getattr(ms, fname, None)
            if callable(fn):
                unhid = fn(args.output)
                break
        if unhid is not None:
            _log(f"  sanitizer: unhid {unhid} rest(s)")
    except Exception as e:
        _log(f"  sanitizer skipped: {e}")

    size_kb = args.output.stat().st_size / 1024
    _log(f"DONE: {args.output} ({size_kb:.1f} KB)")
    return 0


def _log(msg):
    print(msg, file=sys.stderr, flush=True)


def _count_notes(part):
    if part is None:
        return 0
    try:
        return sum(1 for _ in part.recurse().notes)
    except Exception:
        return 0


if __name__ == "__main__":
    sys.exit(main())
