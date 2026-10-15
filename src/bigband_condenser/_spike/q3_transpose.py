"""Q3 - Concert pitch transposition verification.

For each part, extracts the first pitched note and compares written pitch vs
concert pitch (via music21 `.toSoundingPitch()`). Also computes the transposition
interval in semitones and checks against expected values.

Rationale: music21 reads the explicit `<transpose>` tag in MusicXML and applies
the right transposition even when `part.getInstruments()` returns a wrong class
(see Q2). The transposition logic lives in the XML tag, not the instrument class.

Expected (from cloud FINDINGS v0.2 section 4):
- Soprano Sax (Bb):      -2 st
- Alto Sax (Eb):         -9 st
- Tenor Sax (Bb):       -14 st (M9 down with octave-change)
- Baritone Sax (Eb):    -21 st (M13 down with octave-change)
- Trumpet in Bb:         -2 st
- Horn in F:             -7 st
- Trombone/Bass Trombone/Piano/Guitar/Bass: 0 st (concert instruments)
- Drum Set: skipped (unpitched)
"""
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from bigband_condenser._spike.common import setup_logging, KRONOS_EXTRACT  # noqa: E402

EXPECTED_TRANSPOSITIONS = {
    "Soprano Sax": -2,
    "Alto Sax": -9,
    "Tenor Sax 1": -14,
    "Tenor Sax 2": -14,
    "Baritone Sax": -21,
    "Trumpet in Bb 1": -2,
    "Trumpet in Bb 2": -2,
    "Trumpet in Bb 3": -2,
    "Trumpet in Bb 4": -2,
    "Horn in F 1": -7,
    "Horn in F 2": -7,
    "Trombone": 0,
    "Bass Trombone": 0,
    "Electric Guitar": -12,  # notated 1 octave above sounding pitch (convention)
    "Piano": 0,
    "Acoustic Bass": -12,  # notated 1 octave above sounding pitch (convention)
    # Drum Set 1/2 intentionally omitted (unpitched - skipped from verification)
}


def get_first_pitched_note_midi(part):
    """Return midi number of the first pitched note in a part, or None if unpitched/empty."""
    for n in part.recurse().notes:
        try:
            if hasattr(n, "pitch") and n.pitch is not None and hasattr(n.pitch, "midi"):
                return n.pitch.midi, n.pitch.nameWithOctave
            if hasattr(n, "pitches") and n.pitches:
                p0 = n.pitches[0]
                if hasattr(p0, "midi"):
                    return p0.midi, p0.nameWithOctave
        except Exception:
            continue
    return None


def analyze_sample(sample_path, logger):
    from music21 import converter

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        score = converter.parse(str(sample_path))

    results = []
    for p in score.parts:
        name = p.partName or "<unnamed>"
        written_info = get_first_pitched_note_midi(p)

        if written_info is None:
            results.append({
                "name": name, "written": None, "concert": None,
                "delta_st": None, "note": "no pitched notes (likely unpitched)",
            })
            continue

        written_midi, written_name = written_info

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                sounding = p.toSoundingPitch(inPlace=False)
            concert_info = get_first_pitched_note_midi(sounding)
            if concert_info is None:
                concert_midi, concert_name = None, None
                delta = None
            else:
                concert_midi, concert_name = concert_info
                delta = concert_midi - written_midi
        except Exception as e:
            logger.warning(f"toSoundingPitch failed for {name}: {e}")
            concert_name, delta = None, None

        results.append({
            "name": name, "written": written_name, "concert": concert_name,
            "delta_st": delta,
        })

    return results


def main():
    logger = setup_logging()
    logger.info("=" * 76)
    logger.info("Q3 CONCERT PITCH TRANSPOSITION - LOCAL VERIFICATION")
    logger.info("=" * 76)

    if not KRONOS_EXTRACT.exists():
        logger.error(f"Extract not found: {KRONOS_EXTRACT}")
        return 2

    logger.info(f"Parsing: {KRONOS_EXTRACT.name}")
    results = analyze_sample(KRONOS_EXTRACT, logger)

    logger.info("")
    header = f"{'Part':<22}{'Written':<10}{'Concert':<10}{'Δst':<6}{'Expected':<10}{'Verdict':<10}"
    logger.info(header)
    logger.info("-" * len(header))

    failures = []
    skips = []
    for r in results:
        name = r["name"]
        expected = EXPECTED_TRANSPOSITIONS.get(name)

        if expected is None:
            verdict = "SKIP"
            skips.append(name)
        elif r["delta_st"] is None:
            verdict = "NO DATA"
            failures.append(name)
        elif r["delta_st"] == expected:
            verdict = "OK"
        else:
            verdict = "FAIL"
            failures.append(name)

        written_str = r["written"] or "-"
        concert_str = r["concert"] or "-"
        delta_str = str(r["delta_st"]) if r["delta_st"] is not None else "-"
        exp_str = str(expected) if expected is not None else "N/A"
        logger.info(f"{name[:21]:<22}{written_str:<10}{concert_str:<10}{delta_str:<6}{exp_str:<10}{verdict:<10}")

    logger.info("")
    logger.info(f"Skipped (unpitched or N/A): {len(skips)} ({skips})")

    logger.info("")
    logger.info("=" * 76)
    if not failures:
        verified = sum(1 for r in results if r["name"] in EXPECTED_TRANSPOSITIONS)
        logger.info(f"Q3 VERDICT: PASS - {verified}/{verified} verified parts have correct transposition")
        return 0
    else:
        logger.warning(f"Q3 VERDICT: FAIL - {len(failures)} mismatches: {failures}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

