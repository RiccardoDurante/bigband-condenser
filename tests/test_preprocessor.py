"""Tests for bigband_condenser.preprocessor."""
import warnings
from pathlib import Path

import pytest

from bigband_condenser.preprocessor import (
    SEMICROMA_QL,
    preprocess,
    strip_hidden_parts,
    force_instrument_classes,
    filter_sub_semicroma_drums,
    ProcessedScore,
)


class TestStripHiddenParts:
    def test_removes_matching_parts(self, kronos_extract_score):
        count = strip_hidden_parts(kronos_extract_score, {"Drum Set 2"})
        assert count == 1
        names_after = {p.partName for p in kronos_extract_score.parts}
        assert "Drum Set 2" not in names_after

    def test_empty_set_removes_nothing(self, kronos_extract_score):
        before = len(list(kronos_extract_score.parts))
        count = strip_hidden_parts(kronos_extract_score, set())
        assert count == 0
        assert len(list(kronos_extract_score.parts)) == before


class TestForceInstrumentClasses:
    def test_known_partnames_get_forced(self, kronos_extract_score):
        count = force_instrument_classes(kronos_extract_score)
        # All 19 music21 Part objects have known partName -> all forced
        assert count == 19

    def test_bass_class_corrected(self, kronos_extract_score):
        """R30 mitigation check: Acoustic Bass should become AcousticBass, not SopranoSaxophone."""
        import music21.instrument as inst
        force_instrument_classes(kronos_extract_score)
        for part in kronos_extract_score.parts:
            if part.partName == "Acoustic Bass":
                insts = list(part.getElementsByClass(inst.Instrument))
                assert len(insts) >= 1
                assert isinstance(insts[0], inst.AcousticBass)
                return
        pytest.fail("Acoustic Bass part not found in Kronos extract")


class TestFilterSubSemicromaDrums:
    def test_filters_157_in_kronos_extract(self, kronos_extract_score):
        count = filter_sub_semicroma_drums(kronos_extract_score)
        # From Spike M2 Q4: 157 sub-semicroma events in Drum Set 1 after strip hidden
        # BEFORE strip hidden: both drum parts contribute -> 157 + 153 = 310
        # Here we call filter WITHOUT prior strip, so expect 310
        assert count == 310

    def test_only_drum_parts_affected(self, kronos_extract_score):
        """Non-drum parts should keep all their notes."""
        reed_notes_before = sum(
            1 for p in kronos_extract_score.parts
            if "sax" in (p.partName or "").lower()
            for _ in p.recurse().notes
        )
        filter_sub_semicroma_drums(kronos_extract_score)
        reed_notes_after = sum(
            1 for p in kronos_extract_score.parts
            if "sax" in (p.partName or "").lower()
            for _ in p.recurse().notes
        )
        assert reed_notes_before == reed_notes_after


class TestPreprocessEndToEnd:
    def test_preprocess_returns_processed_score(self, kronos_extract_score, kronos_extract_path):
        result = preprocess(kronos_extract_score, kronos_extract_path)
        assert isinstance(result, ProcessedScore)
        assert result.hidden_names == {"Drum Set 2"}
        assert result.parts_stripped == 1
        assert result.classes_forced == 18  # after strip, 18 parts remain
        assert result.drum_notes_filtered == 157  # only Drum Set 1 remains to filter

    def test_write_after_preprocess_succeeds(self, kronos_extract_score, kronos_extract_path, tmp_path):
        """R27 mitigation check: music21.write() should succeed after preprocess."""
        result = preprocess(kronos_extract_score, kronos_extract_path)
        out_file = tmp_path / "preprocessed.musicxml"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result.score.write("musicxml", fp=str(out_file))
        assert out_file.exists()
        assert out_file.stat().st_size > 100_000  # non-trivial output
