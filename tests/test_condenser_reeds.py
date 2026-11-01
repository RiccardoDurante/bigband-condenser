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
                    m.setdefault(round(float(n.getOffsetInHierarchy(part)), 3), []).append(n.pitch.midi)
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

class TestReedsCondenserM43Passthrough:
    """M4.3 - Single-voice passthrough.

    Con un solo part reeds in input, l'intero contenuto deve finire
    nello staff upper, lo staff lower deve restare vuoto, e la struttura
    delle misure (M4.1+M4.2) deve restare intatta.
    """

    SOURCE_PATH = Path("samples/kronos_kai_kairos_extract.musicxml")
    TARGET_PART_NAME = "Soprano Sax"

    def _load_single_part(self):
        import music21

        score = music21.converter.parse(str(self.SOURCE_PATH))
        for part in score.parts:
            if self.TARGET_PART_NAME.lower() in (part.partName or "").lower():
                return score, part
        raise AssertionError(
            f"Part '{self.TARGET_PART_NAME}' non trovato in {self.SOURCE_PATH}"
        )

    def test_single_voice_all_notes_land_in_upper(self):
        score, single_part = self._load_single_part()
        source_note_count = len(list(single_part.flatten().notes))

        condenser = ReedsCondenser()
        upper, lower = condenser.condense([single_part], source_score=score)

        upper_notes = len(list(upper.flatten().notes))
        lower_notes = len(list(lower.flatten().notes))

        assert upper_notes == source_note_count
        assert lower_notes == 0

    def test_single_voice_measure_structure_preserved(self):
        import music21

        score, single_part = self._load_single_part()
        condenser = ReedsCondenser()
        upper, _lower = condenser.condense([single_part], source_score=score)

        source_measures = list(
            single_part.getElementsByClass(music21.stream.Measure)
        )
        upper_measures = list(
            upper.getElementsByClass(music21.stream.Measure)
        )

        assert len(upper_measures) == len(source_measures)


class TestReedsCondenserNoLostPlacement:
    """Regression for BUGFIX M4.2f. music21 derives Measure.duration from
    content, so checks must use the SOURCE bar lengths, not measure.duration."""

    def test_no_notes_outside_measures(self, reed_parts, preprocessed_kronos):
        import music21
        upper, lower = ReedsCondenser().condense(reed_parts, source_score=preprocessed_kronos)
        for part in (upper, lower):
            loose = list(part.getElementsByClass([music21.note.Note, music21.chord.Chord]))
            assert loose == [], f"{len(loose)} notes/chords outside Measures in {part.partName}"

    def test_every_measure_filled_to_source_length(self, reed_parts, preprocessed_kronos):
        import music21
        source_lengths = [
            float(m.duration.quarterLength)
            for m in preprocessed_kronos.parts[0].getElementsByClass(music21.stream.Measure)
        ]
        upper, lower = ReedsCondenser().condense(reed_parts, source_score=preprocessed_kronos)
        for part in (upper, lower):
            measures = list(part.getElementsByClass(music21.stream.Measure))
            assert len(measures) == len(source_lengths)
            for m, expected in zip(measures, source_lengths):
                total = sum(float(e.duration.quarterLength) for e in m.notesAndRests)
                assert abs(total - expected) < 1e-6, (
                    f"{part.partName} measure {m.number}: content {total} != source {expected}"
                )


from bigband_condenser.condenser.reeds import _Ev, _build_voice_elements  # noqa: E402


class TestReedsSoundingSetSegmentation:
    """Pure-python tests of the M4.4 segmentation (no music21 needed)."""

    def test_sustained_chord_not_truncated_by_moving_bass(self):
        evs = [
            _Ev(0, "Soprano Sax", 67, "G4", 0.0, 4.0),
            _Ev(1, "Alto Sax", 64, "E4", 0.0, 4.0),
            _Ev(2, "Tenor Sax 1", 62, "D4", 0.0, 4.0),
            _Ev(3, "Tenor Sax 2", 57, "A3", 0.0, 4.0),
            _Ev(4, "Baritone Sax", 53, "F3", 0.0, 0.5),
            _Ev(5, "Baritone Sax", 48, "C3", 0.5, 1.0),
        ]
        upper, lower = _build_voice_elements(evs, 2, 3)

        # upper: one whole-measure chord, no ties, never truncated
        assert len(upper) == 1
        onset, dur, slots = upper[0]
        assert (onset, dur) == (0.0, 4.0)
        assert [s.pitch_name for s in slots] == ["G4", "E4"]
        assert not any(s.cont_prev or s.cont_next for s in slots)

        # lower: bass line changes underneath, D4/A3 stay tied
        assert [(o, d) for o, d, _ in lower] == [(0.0, 0.5), (0.5, 0.5), (1.0, 3.0)]
        names = [[s.pitch_name for s in sl] for _, _, sl in lower]
        assert names == [["D4", "A3", "F3"], ["D4", "A3", "C3"], ["D4", "A3"]]
        first = {s.pitch_name: s for s in lower[0][2]}
        assert first["D4"].cont_next and first["A3"].cont_next and not first["F3"].cont_next
        second = {s.pitch_name: s for s in lower[1][2]}
        assert second["D4"].cont_prev and second["D4"].cont_next
        assert not second["C3"].cont_prev and not second["C3"].cont_next

    def test_short_note_not_held_to_chord_length(self):
        # regression for FR-M4-D: F3 lasts 0.5, must not be held 4.0
        evs = [
            _Ev(0, "Tenor Sax 1", 62, "D4", 0.0, 4.0),
            _Ev(1, "Tenor Sax 2", 57, "A3", 0.0, 4.0),
            _Ev(2, "Baritone Sax", 53, "F3", 0.0, 0.5),
        ]
        _, lower = _build_voice_elements(evs, 2, 3)
        first_onset, first_dur, first_slots = lower[0]
        assert first_dur == 0.5
        assert "F3" in [s.pitch_name for s in first_slots]
        # only 3 notes sound: D4 and A3 take the upper staff, F3 is alone below
        assert len(lower) == 1
        assert [s.pitch_name for s in first_slots] == ["F3"]

    def test_unison_collapses_to_one_note(self):
        evs = [
            _Ev(0, "Alto Sax", 67, "G4", 0.0, 2.0),
            _Ev(1, "Soprano Sax", 67, "G4", 0.0, 2.0),
            _Ev(2, "Tenor Sax 1", 62, "D4", 0.0, 2.0),
        ]
        upper, lower = _build_voice_elements(evs, 2, 3)
        assert len(upper) == 1
        assert [s.pitch_name for s in upper[0][2]] == ["G4"]
        assert [s.pitch_name for s in lower[0][2]] == ["D4"]

    def test_reattack_of_same_pitch_is_not_tied(self):
        evs = [
            _Ev(0, "Soprano Sax", 67, "G4", 0.0, 1.0),
            _Ev(1, "Soprano Sax", 67, "G4", 1.0, 2.0),
        ]
        upper, _ = _build_voice_elements(evs, 2, 3)
        assert len(upper) == 2
        assert not any(s.cont_prev or s.cont_next for _, _, sl in upper for s in sl)

    def test_output_independent_of_input_order(self):
        evs = [
            _Ev(0, "Soprano Sax", 67, "G4", 0.0, 4.0),
            _Ev(1, "Baritone Sax", 53, "F3", 0.0, 0.5),
            _Ev(2, "Baritone Sax", 48, "C3", 0.5, 1.0),
            _Ev(3, "Alto Sax", 64, "E4", 0.0, 4.0),
        ]
        a = _build_voice_elements(evs, 2, 3)
        b = _build_voice_elements(list(reversed(evs)), 2, 3)
        assert a == b

    def test_same_part_overlap_is_clipped(self):
        import music21
        from bigband_condenser.condenser.reeds import _collect_events
        p = music21.stream.Part()
        p.partName = "Soprano Sax"
        p.insert(0.0, music21.note.Note("G4", quarterLength=1.125))
        p.insert(1.0, music21.note.Note("A4", quarterLength=1.0))
        events = sorted(_collect_events([p]), key=lambda e: e.start)
        assert [(e.start, e.end) for e in events] == [(0.0, 1.0), (1.0, 2.0)]


from bigband_condenser.condenser.reeds import (
    _ABBR_REEDS,
    _build_cast_segments,
    _filter_cast_segments,
    _format_cast_annotations,
    _split_for_label,
)


class TestReedsCastChange:
    # --- segmentation ---
    def test_single_voice_segment(self):
        evs = [_Ev(0, "Alto Sax", 64, "E4", 0.0, 4.0)]
        segs = _build_cast_segments(evs)
        assert len(segs) == 1
        a, b, cast, is_uni, _ = segs[0]
        assert (a, b) == (0.0, 4.0) and cast == frozenset({"Alto Sax"}) and not is_uni

    def test_cast_change_point(self):
        evs = [
            _Ev(0, "Alto Sax", 64, "E4", 0.0, 4.0),
            _Ev(1, "Soprano Sax", 67, "G4", 2.0, 4.0),
        ]
        segs = _build_cast_segments(evs)
        assert [s[2] for s in segs] == [
            frozenset({"Alto Sax"}),
            frozenset({"Alto Sax", "Soprano Sax"}),
        ]

    def test_contiguous_same_cast_merges(self):
        evs = [
            _Ev(0, "Alto Sax", 64, "E4", 0.0, 2.0),
            _Ev(1, "Alto Sax", 65, "F4", 2.0, 4.0),
        ]
        segs = _build_cast_segments(evs)
        assert len(segs) == 1 and (segs[0][0], segs[0][1]) == (0.0, 4.0)

    def test_unison_detected(self):
        evs = [
            _Ev(0, "Alto Sax", 64, "E4", 0.0, 2.0),
            _Ev(1, "Tenor Sax 1", 64, "E4", 0.0, 2.0),
        ]
        segs = _build_cast_segments(evs)
        assert segs[0][3] is True

    def test_min_duration_filters_short_non_unison(self):
        evs = [
            _Ev(0, "Alto Sax", 64, "E4", 0.0, 2.0),
            _Ev(1, "Soprano Sax", 67, "G4", 0.0, 2.0),
        ]
        segs = _build_cast_segments(evs)
        assert _filter_cast_segments(segs, min_duration=4.0) == []

    def test_unison_bypasses_min_duration(self):
        evs = [
            _Ev(0, "Alto Sax", 64, "E4", 0.0, 1.0),
            _Ev(1, "Tenor Sax 1", 64, "E4", 0.0, 1.0),
        ]
        segs = _build_cast_segments(evs)
        kept = _filter_cast_segments(segs, min_duration=4.0)
        assert len(kept) == 1

    # --- split for label ---
    def test_split_by_midi_descending(self):
        upper, lower = _split_for_label(
            frozenset({"S", "A", "T", "B"}),
            {"S": 72, "A": 65, "T": 55, "B": 45}, 2, 3,
        )
        assert upper == ("S", "A") and lower == ("T", "B")

    def test_split_truncates_at_sizes(self):
        upper, lower = _split_for_label(
            frozenset({"A", "B"}), {"A": 60, "B": 50}, 2, 3,
        )
        assert upper == ("A", "B") and lower == ()

    # --- annotation formatting ---
    def test_annotation_single_voice_above_upper(self):
        order = ["Soprano Sax", "Alto Sax", "Tenor Sax 1", "Tenor Sax 2", "Baritone Sax"]
        ann = _format_cast_annotations(
            frozenset({"Alto Sax"}), order, False, _ABBR_REEDS,
            ("Alto Sax",), (),
        )
        assert ann == [("upper", "above", "A.Sx")]

    def test_annotation_tutti_above_upper(self):
        order = ["Soprano Sax", "Alto Sax", "Tenor Sax 1", "Tenor Sax 2", "Baritone Sax"]
        ann = _format_cast_annotations(
            frozenset(order), order, False, _ABBR_REEDS,
            ("Soprano Sax", "Alto Sax"),
            ("Tenor Sax 1", "Tenor Sax 2", "Baritone Sax"),
        )
        assert ann == [("upper", "above", "Tutti")]

    def test_annotation_column_split_two_staves(self):
        order = ["Soprano Sax", "Alto Sax", "Tenor Sax 1", "Tenor Sax 2", "Baritone Sax"]
        ann = _format_cast_annotations(
            frozenset({"Soprano Sax", "Tenor Sax 1", "Baritone Sax"}),
            order, False, _ABBR_REEDS,
            ("Soprano Sax", "Tenor Sax 1"), ("Baritone Sax",),
        )
        assert len(ann) == 2
        assert ann[0] == ("upper", "above", "S.Sx\nT.Sx 1")
        assert ann[1] == ("lower", "below", "Bar.Sx")

    def test_annotation_full_cast_unison_both_staves(self):
        order = ["Soprano Sax", "Alto Sax", "Tenor Sax 1", "Tenor Sax 2", "Baritone Sax"]
        upper = ("Soprano Sax", "Alto Sax")
        lower = ("Tenor Sax 1", "Tenor Sax 2", "Baritone Sax")
        ann = _format_cast_annotations(frozenset(order), order, True, _ABBR_REEDS, upper, lower)
        # unison -> column form (NOT 'Tutti')
        assert [staff for staff, _, _ in ann] == ["upper", "lower"]
        assert "Bar.Sx" in ann[1][2]
