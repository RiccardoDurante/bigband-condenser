"""Tests for bigband_condenser.instrument_mapping."""
from bigband_condenser.instrument_mapping import (
    get_transposition_semitones,
    get_music21_instrument_class,
    is_known_instrument,
)


class TestTranspositionSemitones:
    def test_saxes_correct_transposition(self):
        assert get_transposition_semitones("Soprano Sax") == -2
        assert get_transposition_semitones("Alto Sax") == -9
        assert get_transposition_semitones("Tenor Sax 1") == -14
        assert get_transposition_semitones("Tenor Sax 2") == -14
        assert get_transposition_semitones("Baritone Sax") == -21

    def test_brass_correct_transposition(self):
        assert get_transposition_semitones("Trumpet in Bb 1") == -2
        assert get_transposition_semitones("Trumpet in Bb 4") == -2
        assert get_transposition_semitones("Horn in F 1") == -7
        assert get_transposition_semitones("Horn in F 2") == -7
        assert get_transposition_semitones("Trombone") == 0
        assert get_transposition_semitones("Bass Trombone") == 0

    def test_octave_transposing_rhythm(self):
        # Guitar and Bass are notated 1 octave above sounding (R29 convention)
        assert get_transposition_semitones("Electric Guitar") == -12
        assert get_transposition_semitones("Acoustic Bass") == -12

    def test_non_transposing_rhythm(self):
        assert get_transposition_semitones("Piano") == 0

    def test_drums_sentinel_zero(self):
        assert get_transposition_semitones("Drum Set 1") == 0
        assert get_transposition_semitones("Drum Set 2") == 0

    def test_unknown_returns_none(self):
        assert get_transposition_semitones("Theremin") is None
        assert get_transposition_semitones("Harpsichord") is None

    def test_empty_returns_none(self):
        assert get_transposition_semitones("") is None
        assert get_transposition_semitones("   ") is None

    def test_substring_fallback(self):
        # "Tenor Sax 5" is not an exact entry; substring "Tenor Sax" should match
        assert get_transposition_semitones("Tenor Sax 5") == -14


class TestMusic21InstrumentClass:
    def test_known_classes_resolve(self):
        import music21.instrument as inst
        assert get_music21_instrument_class("Alto Sax") is inst.AltoSaxophone
        assert get_music21_instrument_class("Trumpet in Bb 1") is inst.Trumpet
        assert get_music21_instrument_class("Horn in F 1") is inst.Horn
        assert get_music21_instrument_class("Bass Trombone") is inst.BassTrombone
        assert get_music21_instrument_class("Piano") is inst.Piano

    def test_unknown_returns_none(self):
        assert get_music21_instrument_class("Theremin") is None


class TestIsKnown:
    def test_known_returns_true(self):
        assert is_known_instrument("Alto Sax") is True
        assert is_known_instrument("Horn in F 1") is True

    def test_unknown_returns_false(self):
        assert is_known_instrument("Theremin") is False
        assert is_known_instrument("") is False
