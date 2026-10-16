"""Instrument mapping for Big Band Condenser v1.

Maps partName strings (as they appear in MusicXML <part-name>) to:
  1. Transposition in semitones (concert = written + semitones)
  2. music21.instrument class for forcing correct instrument pre-write

Rationale (from Spike M2 FINDINGS):
- R26: music21.getInstruments() returns WRONG classes on Finale export
  (Soprano Sax -> Sampler, Acoustic Bass -> SopranoSaxophone, etc.).
- R30 (critical): music21.write() REGENERATES <transpose> from internal class,
  silently corrupting output for mis-classified parts (e.g. Acoustic Bass
  gets written with -2 st tag like a Soprano Sax instead of -12 st octave).

Mitigation: before calling music21.write(), replace the wrong instrument class
with the correct one using this table. Preprocessor.force_instrument_classes()
does this lookup.

Table extended from bigband-ai/backend/dorico_bridge/musicxml_writer.py
(_INSTRUMENT_TRANSPOSITIONS). Additions for v1: Soprano Sax, Horn in F,
Electric Guitar, Acoustic Bass, Piano, Drums.

Lookup order: exact match first (case-insensitive), then substring match.
First-match-wins -> declare specific variants before generic fallbacks.
"""
from __future__ import annotations

# (partName_pattern, transposition_semitones, music21_instrument_class_name)
# Transposition: concert_pitch = written_pitch + semitones.
# Positive = written is below concert (rare); negative = written is above concert.
_INSTRUMENT_SPECS: list[tuple[str, int, str]] = [
    # ---------------- Reeds ----------------
    ("Soprano Sax", -2, "SopranoSaxophone"),
    ("Alto Sax 1", -9, "AltoSaxophone"),
    ("Alto Sax 2", -9, "AltoSaxophone"),
    ("Alto Sax", -9, "AltoSaxophone"),
    ("Tenor Sax 1", -14, "TenorSaxophone"),
    ("Tenor Sax 2", -14, "TenorSaxophone"),
    ("Tenor Sax", -14, "TenorSaxophone"),
    ("Baritone Sax", -21, "BaritoneSaxophone"),
    ("Clarinet in Bb", -2, "Clarinet"),
    ("Clarinet", -2, "Clarinet"),
    ("Bass Clarinet", -14, "BassClarinet"),
    ("Flute", 0, "Flute"),
    ("Alto Flute", -5, "AltoFlute"),

    # ---------------- Brass ----------------
    ("Trumpet in Bb 1", -2, "Trumpet"),
    ("Trumpet in Bb 2", -2, "Trumpet"),
    ("Trumpet in Bb 3", -2, "Trumpet"),
    ("Trumpet in Bb 4", -2, "Trumpet"),
    ("Trumpet in Bb", -2, "Trumpet"),
    ("Trumpet", -2, "Trumpet"),  # Bb assumed in big band context
    ("Flugelhorn", -2, "Flugelhorn"),
    ("Horn in F 1", -7, "Horn"),
    ("Horn in F 2", -7, "Horn"),
    ("Horn in F 3", -7, "Horn"),
    ("Horn in F 4", -7, "Horn"),
    ("Horn in F", -7, "Horn"),
    ("Horn", -7, "Horn"),  # F assumed
    ("Trombone 1", 0, "Trombone"),
    ("Trombone 2", 0, "Trombone"),
    ("Trombone 3", 0, "Trombone"),
    ("Bass Trombone", 0, "BassTrombone"),
    ("Trombone", 0, "Trombone"),
    ("Tuba", 0, "Tuba"),

    # ---------------- Rhythm ----------------
    # Guitar and Bass are OCTAVE-TRANSPOSING by convention:
    # notated 1 octave above sounding pitch (see R29).
    ("Electric Guitar", -12, "ElectricGuitar"),
    ("Guitar", -12, "ElectricGuitar"),
    ("Acoustic Bass", -12, "AcousticBass"),
    ("Electric Bass", -12, "ElectricBass"),
    ("Bass Guitar", -12, "ElectricBass"),
    ("Bass", -12, "AcousticBass"),  # fallback for bass variants
    ("Piano", 0, "Piano"),
    ("Vibraphone", 0, "Vibraphone"),

    # ---------------- Drums ----------------
    # Drums are unpitched: transposition is meaningless.
    # We use 0 as a sentinel and Percussion as a generic class.
    ("Drum Set 1", 0, "Percussion"),
    ("Drum Set 2", 0, "Percussion"),
    ("Drum Set", 0, "Percussion"),
    ("Drums", 0, "Percussion"),
    ("Percussion", 0, "Percussion"),
]


def _lookup(part_name: str) -> tuple[int | None, str | None]:
    """Return (semitones, music21_class_name) for a partName, or (None, None) if unknown.

    Lookup strategy:
    1. Exact match (case-insensitive) against _INSTRUMENT_SPECS patterns
    2. Fallback: substring match (first-match-wins, so declare specific variants first)
    """
    if not part_name:
        return None, None
    pname_lower = part_name.strip().lower()

    # Exact match pass
    for pattern, semitones, cls in _INSTRUMENT_SPECS:
        if pattern.lower() == pname_lower:
            return semitones, cls

    # Substring match pass
    for pattern, semitones, cls in _INSTRUMENT_SPECS:
        if pattern.lower() in pname_lower:
            return semitones, cls

    return None, None


def get_transposition_semitones(part_name: str) -> int | None:
    """Return transposition semitones for a partName, or None if unknown.

    concert_pitch = written_pitch + returned_value

    Examples:
        >>> get_transposition_semitones("Alto Sax")
        -9
        >>> get_transposition_semitones("Tenor Sax 2")
        -14
        >>> get_transposition_semitones("Trombone")
        0
        >>> get_transposition_semitones("Theremin")  # unknown
        # Returns None
    """
    semitones, _ = _lookup(part_name)
    return semitones


def get_music21_instrument_class(part_name: str):
    """Return the music21 instrument class for a partName, or None if unknown.

    Returns the class itself (not an instance). Caller instantiates:
        cls = get_music21_instrument_class("Alto Sax")
        if cls is not None:
            part.insert(0, cls())

    If the mapped class name does not exist in music21.instrument (version
    differences), returns music21.instrument.Instrument as a safe fallback.
    """
    _, cls_name = _lookup(part_name)
    if cls_name is None:
        return None
    import music21.instrument as inst
    cls = getattr(inst, cls_name, None)
    if cls is None:
        return inst.Instrument  # safe generic fallback
    return cls


def is_known_instrument(part_name: str) -> bool:
    """Check whether a partName is in the mapping table (either match type)."""
    semitones, _ = _lookup(part_name)
    return semitones is not None
