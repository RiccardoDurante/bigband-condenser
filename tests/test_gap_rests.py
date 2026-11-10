"""Regression tests for partial-bar rests (TK-Reeds-03)."""
import music21

from bigband_condenser.condenser._common import _fill_measure_rests


def _bar(ts: str, bar_len: float):
    m = music21.stream.Measure(number=1)
    m.insert(0, music21.meter.TimeSignature(ts))
    m.insert(0, music21.chord.Chord(["G4", "D4"], quarterLength=1))
    _fill_measure_rests(m, bar_len)
    return m


def _rest_lengths(m):
    return [float(r.duration.quarterLength) for r in m.getElementsByClass(music21.note.Rest)]


def test_partial_gap_of_four_quarters_is_not_a_whole_rest():
    assert _rest_lengths(_bar("5/4", 5.0)) == [2.0, 2.0]


def test_short_gaps_are_unchanged():
    assert _rest_lengths(_bar("4/4", 4.0)) == [3.0]


def test_empty_bar_keeps_single_full_bar_rest():
    m = music21.stream.Measure(number=1)
    _fill_measure_rests(m, 5.0)
    assert _rest_lengths(m) == [5.0]


def test_bar_length_survives_musicxml_round_trip(tmp_path):
    part = music21.stream.Part()
    part.append(_bar("5/4", 5.0))
    second = music21.stream.Measure(number=2)
    second.insert(0, music21.note.Note("A4", quarterLength=5))
    part.append(second)
    fp = tmp_path / "roundtrip.musicxml"
    part.write("musicxml", fp=str(fp))
    back = music21.converter.parse(str(fp))
    measures = list(back.parts[0].getElementsByClass(music21.stream.Measure))
    assert float(measures[1].offset) == 5.0
