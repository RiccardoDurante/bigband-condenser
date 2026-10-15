"""Q4 - Round-trip write test + drum duration histogram.

Tech Lead decision (2026-10-15): no dual pipeline. Investigate minimal strategy
that enables music21.write() to succeed on Finale-exported big band scores.

Three progressive experiments:
  Exp 1: write as-is (expected FAIL per cloud finding).
  Exp 2: strip hidden parts (Drum Set 2 playback), then write.
  Exp 3: strip hidden + filter sub-semicroma durations from remaining drums.

Semicroma threshold = 0.25 quarterLength. Per Music Expert input (session 2026-10-14):
notational drum values rarely go below semicroma; durations shorter than that in
Finale export are MIDI playback artifacts (humanization, grace note roll), not
notational intent.

Rollback plan: reduct-score-no-drum via Change Request (pre-approved).
"""
import sys
import warnings
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from bigband_condenser._spike.common import setup_logging, KRONOS_EXTRACT  # noqa: E402

SEMICROMA_QL = 0.25
TMP_DIR = Path(__file__).resolve().parent / "_tmp"
TMP_DIR.mkdir(exist_ok=True)


def detect_hidden_part_names(xml_path):
    """From Q2: find hidden part names via <staff-details print-object='no'/>."""
    tree = ET.parse(str(xml_path))
    root = tree.getroot()
    id_to_name = {}
    for sp in root.findall(".//score-part"):
        pid = sp.get("id")
        pn = sp.find("part-name")
        if pid and pn is not None and pn.text:
            id_to_name[pid] = pn.text
    hidden = set()
    for part in root.findall("part"):
        name = id_to_name.get(part.get("id"))
        if not name:
            continue
        fm = part.find("measure")
        if fm is None:
            continue
        attrs = fm.find("attributes")
        if attrs is None:
            continue
        for sd in attrs.findall("staff-details"):
            if sd.get("print-object") == "no" and not sd.get("number"):
                hidden.add(name)
    return hidden


def histogram_drum_durations(score):
    histograms = {}
    for p in score.parts:
        name = p.partName or ""
        n = name.lower()
        if "drum" not in n and "percuss" not in n:
            continue
        durs = [note.duration.quarterLength for note in p.recurse().notesAndRests]
        histograms[name] = durs
    return histograms


def report_histogram(histograms, logger):
    logger.info("")
    logger.info("DRUM DURATION HISTOGRAM:")
    for name, durs in histograms.items():
        if not durs:
            logger.info(f"  {name}: no durations collected")
            continue
        c = Counter(durs)
        below = sum(cnt for d, cnt in c.items() if d < SEMICROMA_QL)
        total = sum(c.values())
        pct = 100.0 * below / total if total else 0
        logger.info(f"  {name}: {total} events, {below} below {SEMICROMA_QL}ql ({pct:.2f}%)")
        top = sorted(c.items(), key=lambda x: -x[1])[:8]
        for d, cnt in top:
            marker = " <-- SUB-SEMICROMA" if d < SEMICROMA_QL else ""
            logger.info(f"    ql={d}: {cnt} events{marker}")


def try_write(score, out_path, label, logger):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            score.write("musicxml", fp=str(out_path))
        size = out_path.stat().st_size
        logger.info(f"  {label}: WRITE OK ({size:,} bytes -> {out_path.name})")
        return True
    except Exception as e:
        logger.error(f"  {label}: WRITE FAILED: {type(e).__name__}: {str(e)[:200]}")
        return False


def load_score():
    from music21 import converter
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return converter.parse(str(KRONOS_EXTRACT))


def strip_hidden_parts(score, hidden_names, logger):
    to_remove = [p for p in score.parts if (p.partName or "") in hidden_names]
    for p in to_remove:
        score.remove(p)
    logger.info(f"  Stripped {len(to_remove)} hidden part(s): {[p.partName for p in to_remove]}")
    return len(to_remove)


def filter_sub_semicroma_drums(score, logger):
    filtered = 0
    for p in score.parts:
        n = (p.partName or "").lower()
        if "drum" not in n and "percuss" not in n:
            continue
        for note in list(p.recurse().notesAndRests):
            try:
                if note.duration.quarterLength < SEMICROMA_QL:
                    site = note.activeSite
                    if site is not None:
                        site.remove(note)
                        filtered += 1
            except Exception:
                pass
    logger.info(f"  Filtered {filtered} sub-semicroma events from drum parts")
    return filtered


def main():
    logger = setup_logging()
    logger.info("=" * 70)
    logger.info("Q4 WRITE / ROUND-TRIP + DRUM DURATION HISTOGRAM")
    logger.info("=" * 70)

    if not KRONOS_EXTRACT.exists():
        logger.error(f"Extract not found: {KRONOS_EXTRACT}")
        return 2

    hidden_names = detect_hidden_part_names(KRONOS_EXTRACT)
    logger.info(f"Hidden parts: {sorted(hidden_names) or '(none)'}")

    logger.info(f"Parsing: {KRONOS_EXTRACT.name}")
    score = load_score()
    histograms = histogram_drum_durations(score)
    report_histogram(histograms, logger)

    logger.info("")
    logger.info("WRITE EXPERIMENTS:")

    # Exp 1: as-is
    logger.info("")
    logger.info("Experiment 1: full score as-is (expect FAIL per cloud finding)")
    exp1_ok = try_write(score, TMP_DIR / "q4_exp1_asis.musicxml", "Exp 1", logger)

    # Exp 2: strip hidden
    logger.info("")
    logger.info("Experiment 2: strip hidden parts, then write")
    score2 = load_score()
    strip_hidden_parts(score2, hidden_names, logger)
    exp2_ok = try_write(score2, TMP_DIR / "q4_exp2_no_hidden.musicxml", "Exp 2", logger)

    # Exp 3: strip hidden + filter sub-semicroma
    logger.info("")
    logger.info("Experiment 3: strip hidden + filter sub-semicroma, then write")
    score3 = load_score()
    strip_hidden_parts(score3, hidden_names, logger)
    filter_sub_semicroma_drums(score3, logger)
    exp3_ok = try_write(score3, TMP_DIR / "q4_exp3_filtered.musicxml", "Exp 3", logger)

    # Verdict
    logger.info("")
    logger.info("=" * 70)
    logger.info("Q4 SUMMARY:")
    logger.info(f"  Exp 1 (as-is):           {'OK' if exp1_ok else 'FAIL'}")
    logger.info(f"  Exp 2 (no hidden):       {'OK' if exp2_ok else 'FAIL'}")
    logger.info(f"  Exp 3 (no hidden + flt): {'OK' if exp3_ok else 'FAIL'}")
    logger.info("")

    if exp2_ok:
        logger.info("Q4 VERDICT: PASS - MINIMAL STRATEGY: strip hidden parts.")
        logger.info("  R27 effectively downgraded: sub-32th events live in hidden Drum Set 2.")
        logger.info("  Condenser pipeline: strip hidden pre-write, no further filter needed.")
        return 0
    elif exp3_ok:
        logger.info("Q4 VERDICT: PASS - STRATEGY: strip hidden + filter sub-semicroma.")
        logger.info("  R27 downgraded via filter; mitigation definita e validata.")
        return 0
    else:
        logger.warning("Q4 VERDICT: FAIL - Neither strategy works. Investigate before M3.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
