"""M4.3 - Single-voice passthrough preview.

Isola la pipeline di scrittura (metadata + skeleton + measure-fill +
sanitizer) dal comportamento di split 2+3 del ReedsCondenser. Passando
UN SOLO part reeds come source, il comportamento esistente del
condenser gia' instrada tutto il contenuto nello staff upper e lascia
il lower vuoto (solo pause) — nessuna modifica a reeds.py necessaria.

Verifica: numero di note nello staff upper == numero di note nel part
sorgente, struttura misure preservata (M4.1+M4.2), nessuna misura
visivamente corta.
"""
from __future__ import annotations

import sys
from pathlib import Path

import music21

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bigband_condenser.condenser.reeds import ReedsCondenser
from bigband_condenser.musicxml_sanitizer import unhide_rests

SOURCE_PATH = Path("samples/kronos_kai_kairos_extract.musicxml")
OUT_PATH = Path("samples/preview_single_voice_m43.musicxml")
TARGET_PART_NAME = "Soprano Sax"


def find_part_by_name(score: music21.stream.Score, name: str) -> music21.stream.Part:
    for part in score.parts:
        pname = part.partName or ""
        if name.lower() in pname.lower():
            return part
    available = [p.partName for p in score.parts]
    raise ValueError(
        f"Part '{name}' non trovato. Part disponibili: {available}"
    )


def count_notes(container) -> int:
    return len(list(container.flatten().notes))


def main() -> int:
    if not SOURCE_PATH.exists():
        print(f"ERRORE: source non trovato: {SOURCE_PATH}")
        return 1

    print(f"Carico source: {SOURCE_PATH}")
    score = music21.converter.parse(str(SOURCE_PATH))

    single_part = find_part_by_name(score, TARGET_PART_NAME)
    source_note_count = count_notes(single_part)
    print(f"Part isolato: '{single_part.partName}' — {source_note_count} note/eventi")

    condenser = ReedsCondenser()
    upper_part, lower_part = condenser.condense([single_part], source_score=score)

    upper_notes = count_notes(upper_part)
    lower_notes = count_notes(lower_part)

    print(f"Upper staff: {upper_notes} note")
    print(f"Lower staff: {lower_notes} note (atteso: 0)")

    out = music21.stream.Score()
    out.insert(0, upper_part)
    out.insert(0, lower_part)
    out.write("musicxml", fp=str(OUT_PATH))
    print(f"Scritto: {OUT_PATH}")

    fixed = unhide_rests(OUT_PATH)
    if fixed:
        print(f"sanitizer: unhid {fixed} rest(s)")

    print()
    print("=== VERIFICA M4.3 ===")
    ok = True
    if upper_notes != source_note_count:
        print(f"FAIL: upper_notes ({upper_notes}) != source_note_count ({source_note_count})")
        ok = False
    else:
        print(f"OK: upper_notes == source_note_count ({upper_notes})")

    if lower_notes != 0:
        print(f"FAIL: lower_notes ({lower_notes}) != 0 (atteso vuoto con 1 solo input)")
        ok = False
    else:
        print("OK: lower_notes == 0")

    print()
    print("PASSTHROUGH OK" if ok else "PASSTHROUGH FALLITO - vedi sopra")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
