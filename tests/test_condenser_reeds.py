"""Tests for ReedsCondenser M4-R1 (dynamic split 2+3 by pitch, treble/bass)."""
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

    def test_upper_and_lower_both_have_notes(self, reed_parts):
        upper, lower = ReedsCondenser().condense(reed_parts)
        upper_notes = sum(1 for _ in upper.recurse().notes)
        lower_notes = sum(1 for _ in lower.recurse().notes)
        assert upper_notes > 0
        assert lower_notes > 0

    def test_empty_parts_list_returns_empty_parts(self):
        upper, lower = ReedsCondenser().condense([])
        import music21
        assert isinstance(upper, music21.stream.Part)
        assert isinstance(lower, music21.stream.Part)

    def test_section_name(self):
        assert ReedsCondenser().section_name == "Reeds"

    def test_voice_counts(self):
        """Verify the spec 2+3 (D-028 variant)."""
        c = ReedsCondenser()
        assert c.upper_voice_count == 2
        assert c.lower_voice_count == 3


class TestReedsCondenserClefs:
    def test_upper_has_treble_clef(self, reed_parts):
        import music21
        upper, _ = ReedsCondenser().condense(reed_parts)
        clefs = list(upper.recurse().getElementsByClass(music21.clef.Clef))
        assert any(isinstance(c, music21.clef.TrebleClef) for c in clefs)

    def test_lower_has_bass_clef(self, reed_parts):
        import music21
        _, lower = ReedsCondenser().condense(reed_parts)
        clefs = list(lower.recurse().getElementsByClass(music21.clef.Clef))
        assert any(isinstance(c, music21.clef.BassClef) for c in clefs)


class TestReedsCondenserPitchSplit:
    def test_majority_of_onsets_respect_split(self, reed_parts):
        """For onsets WHERE BOTH staves have notes, upper min >= lower max
        in the majority of cases. makeNotation() can riaggregate notes
        with sustained tails, so a tolerance is allowed."""
        upper, lower = ReedsCondenser().condense(reed_parts)

        def by_offset(part):
            m = {}
            for n in part.recurse().notes:
                if hasattr(n, "pitch") and n.pitch is not None:
                    m.setdefault(round(float(n.offset), 3), []).append(n.pitch.midi)
            return m

        upper_map = by_offset(upper)
        lower_map = by_offset(lower)
        shared = set(upper_map.keys()) & set(lower_map.keys())
        assert len(shared) > 10

        ok = 0
        violations = 0
        for off in shared:
            if min(upper_map[off]) >= max(lower_map[off]):
                ok += 1
            else:
                violations += 1
        ratio = ok / (ok + violations) if (ok + violations) > 0 else 0
        # R1 tolerance: at least 80% of shared offsets respect split
        assert ratio >= 0.80, f"only {ratio:.1%} of shared offsets respect pitch split"


class TestReedsCondenserWriteable:
    def test_output_writes_valid_musicxml(self, reed_parts, tmp_path):
        """End-to-end: condense -> write -> re-parse OK."""
        import music21
        upper, lower = ReedsCondenser().condense(reed_parts)
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
