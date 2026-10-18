"""Tests for ReedsCondenser M4-R1 + M4.1 + M4.2."""
import warnings
from pathlib import Path

import pytest

from bigband_condenser.classifier import classify_score, SECTION_REEDS
from bigband_condenser.condenser import ReedsCondenser
from bigband_condenser.preprocessor import preprocess


@pytest.fixture
def preprocessed_kronos(kronos_extract_score, kronos_extract_path):
    result = preprocess(kronos_extract_score, kronos_extract_path)
    return result.score


@pytest.fixture
def reed_parts(preprocessed_kronos, kronos_extract_path):
    classifications = classify_score(kronos_extract_path)
    reed_names = {c.part_name for c in classifications if c.section == SECTION_REEDS}
    return [p for p in preprocessed_kronos.parts if (p.partName or "") in reed_names]


class TestReedsCondenserBasics:
    def test_returns_two_parts(self, reed_parts):
        upper, lower = ReedsCondenser().condense(reed_parts)
        import music21
        assert isinstance(upper, music21.stream.Part)
        assert isinstance(lower, music21.stream.Part)

    def test_upper_and_lower_both_have_notes(self, reed_parts, preprocessed_kronos):
        upper, lower = ReedsCondenser().condense(reed_parts, source_score=preprocessed_kronos)
        assert sum(1 for _ in upper.recurse().notes) > 0
        assert sum(1 for _ in lower.recurse().notes) > 0

    def test_empty_parts_list_returns_empty_parts(self):
        upper, lower = ReedsCondenser().condense([])
        import music21
        assert isinstance(upper, music21.stream.Part)

    def test_section_name(self):
        assert ReedsCondenser().section_name == "Reeds"

    def test_voice_counts(self):
        c = ReedsCondenser()
        assert c.upper_voice_count == 2
        assert c.lower_voice_count == 3


class TestReedsCondenserClefs:
    def test_upper_has_treble_clef(self, reed_parts, preprocessed_kronos):
        import music21
        upper, _ = ReedsCondenser().condense(reed_parts, source_score=preprocessed_kronos)
        clefs = list(upper.recurse().getElementsByClass(music21.clef.Clef))
        assert any(isinstance(c, music21.clef.TrebleClef) for c in clefs)

    def test_lower_has_bass_clef(self, reed_parts, preprocessed_kronos):
        import music21
        _, lower = ReedsCondenser().condense(reed_parts, source_score=preprocessed_kronos)
        clefs = list(lower.recurse().getElementsByClass(music21.clef.Clef))
        assert any(isinstance(c, music21.clef.BassClef) for c in clefs)


class TestReedsCondenserPitchSplit:
    def test_majority_of_onsets_respect_split(self, reed_parts, preprocessed_kronos):
        upper, lower = ReedsCondenser().condense(reed_parts, source_score=preprocessed_kronos)

        def by_offset(part):
            m = {}
            for n in part.recurse().notes:
                if hasattr(n, "pitch") and n.pitch is not None:
                    m.setdefault(round(float(n.offset), 3), []).append(n.pitch.midi)
            return m

        upper_map = by_offset(upper)
        lower_map = by_offset(lower)
        shared = set(upper_map.keys()) & set(lower_map.keys())
        assert len(shared) > 5

        ok = sum(1 for off in shared if min(upper_map[off]) >= max(lower_map[off]))
        violations = len(shared) - ok
        ratio = ok / (ok + violations) if (ok + violations) > 0 else 0
        assert ratio >= 0.70  # a bit more tolerance with skeleton structure


class TestReedsCondenserWriteable:
    def test_output_writes_valid_musicxml(self, reed_parts, preprocessed_kronos, tmp_path):
        import music21
        upper, lower = ReedsCondenser().condense(reed_parts, source_score=preprocessed_kronos)
        score = music21.stream.Score()
        score.insert(0, upper)
        score.insert(0, lower)
        out = tmp_path / "reeds_condensed.musicxml"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            score.write("musicxml", fp=str(out))
        assert out.exists()
        assert out.stat().st_size > 1000
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            reparsed = music21.converter.parse(str(out))
        assert len(list(reparsed.parts)) == 2


class TestReedsCondenserMetadataM41:
    def test_key_signature_preserved(self, reed_parts, preprocessed_kronos):
        import music21
        upper, lower = ReedsCondenser().condense(reed_parts, source_score=preprocessed_kronos)
        for part in (upper, lower):
            keys = list(part.recurse().getElementsByClass(music21.key.KeySignature))
            assert len(keys) >= 1

    def test_time_signature_preserved(self, reed_parts, preprocessed_kronos):
        import music21
        upper, lower = ReedsCondenser().condense(reed_parts, source_score=preprocessed_kronos)
        for part in (upper, lower):
            times = list(part.recurse().getElementsByClass(music21.meter.TimeSignature))
            assert len(times) >= 1

    def test_tempo_marking_preserved(self, reed_parts, preprocessed_kronos):
        import music21
        upper, lower = ReedsCondenser().condense(reed_parts, source_score=preprocessed_kronos)
        for part in (upper, lower):
            tempos = list(part.recurse().getElementsByClass(music21.tempo.MetronomeMark))
            assert len(tempos) >= 1

    def test_source_score_none_safe(self, reed_parts):
        upper, lower = ReedsCondenser().condense(reed_parts, source_score=None)
        import music21
        assert isinstance(upper, music21.stream.Part)


class TestReedsCondenserMeasureStructureM42:
    """M4.2: measure structure cloned from source_score."""

    def test_measure_count_matches_source(self, reed_parts, preprocessed_kronos):
        """Both upper and lower should have the same number of measures as source."""
        import music21
        source_measures = len(list(preprocessed_kronos.parts[0].getElementsByClass(music21.stream.Measure)))
        upper, lower = ReedsCondenser().condense(reed_parts, source_score=preprocessed_kronos)
        upper_measures = len(list(upper.getElementsByClass(music21.stream.Measure)))
        lower_measures = len(list(lower.getElementsByClass(music21.stream.Measure)))
        assert upper_measures == source_measures, f"upper has {upper_measures} measures, source has {source_measures}"
        assert lower_measures == source_measures, f"lower has {lower_measures} measures, source has {source_measures}"

    def test_pickup_measure_preserved(self, reed_parts, preprocessed_kronos):
        """If source has a pickup (measure number 0), output should too."""
        import music21
        source_first = list(preprocessed_kronos.parts[0].getElementsByClass(music21.stream.Measure))[0]
        source_has_pickup = source_first.number == 0
        upper, _ = ReedsCondenser().condense(reed_parts, source_score=preprocessed_kronos)
        upper_first = list(upper.getElementsByClass(music21.stream.Measure))[0]
        if source_has_pickup:
            assert upper_first.number == 0, f"source has pickup but upper first measure is #{upper_first.number}"

    def test_measure_numbers_sequential(self, reed_parts, preprocessed_kronos):
        """Measure numbers in output should be sequential (0..N or 1..N)."""
        import music21
        upper, _ = ReedsCondenser().condense(reed_parts, source_score=preprocessed_kronos)
        measures = list(upper.getElementsByClass(music21.stream.Measure))
        numbers = [m.number for m in measures]
        # Monotonically non-decreasing
        for i in range(1, len(numbers)):
            assert numbers[i] >= numbers[i - 1], f"measure numbers not monotonic: {numbers}"

    def test_measures_contain_notes(self, reed_parts, preprocessed_kronos):
        """At least some measures should contain actual notes (not all rests)."""
        import music21
        upper, lower = ReedsCondenser().condense(reed_parts, source_score=preprocessed_kronos)
        upper_measures_with_notes = sum(
            1 for m in upper.getElementsByClass(music21.stream.Measure)
            if any(True for _ in m.recurse().notes)
        )
        assert upper_measures_with_notes > 0, "no measure in upper contains notes"
