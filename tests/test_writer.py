"""Tests for bigband_condenser.writer."""
import warnings
from pathlib import Path

import pytest

from bigband_condenser.writer import write_musicxml, CondenserWriteError
from bigband_condenser.preprocessor import preprocess


class TestWriterHappyPath:
    def test_write_after_preprocess_succeeds(
        self, kronos_extract_score, kronos_extract_path, tmp_path
    ):
        result = preprocess(kronos_extract_score, kronos_extract_path)
        out = write_musicxml(result.score, tmp_path / "out.musicxml")
        assert out.exists()
        assert out.stat().st_size > 100_000

    def test_write_sets_title(self, kronos_extract_score, kronos_extract_path, tmp_path):
        result = preprocess(kronos_extract_score, kronos_extract_path)
        out = write_musicxml(
            result.score,
            tmp_path / "titled.musicxml",
            title="Condensed Score Test",
        )
        # Re-parse to check metadata
        from music21 import converter
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            reparsed = converter.parse(str(out))
        assert reparsed.metadata.title == "Condensed Score Test"

    def test_write_creates_parent_dir(self, kronos_extract_score, kronos_extract_path, tmp_path):
        result = preprocess(kronos_extract_score, kronos_extract_path)
        nested = tmp_path / "nested" / "dir" / "out.musicxml"
        out = write_musicxml(result.score, nested)
        assert out.exists()


class TestWriterR27Diagnostic:
    def test_write_without_preprocess_raises_with_hint(
        self, kronos_extract_score, tmp_path
    ):
        """Without preprocess, Finale drum sub-32th durations cause music21.write() to fail.
        Writer must raise CondenserWriteError with a hint pointing to preprocess()."""
        with pytest.raises(CondenserWriteError) as exc_info:
            write_musicxml(kronos_extract_score, tmp_path / "bad.musicxml")
        assert "preprocess" in str(exc_info.value).lower() or "r27" in str(exc_info.value).lower()
