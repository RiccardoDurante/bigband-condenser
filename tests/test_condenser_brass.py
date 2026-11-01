"""Pure-python tests for brass family-based routing (no music21 required)."""
from bigband_condenser.condenser.reeds import _Ev  # dataclass re-exported
from bigband_condenser.condenser._common import _build_voice_elements
from bigband_condenser.condenser.brass import (
    _ABBR_BRASS,
    _FAMILY_MAP_BRASS,
    _DEFAULT_RANK_BRASS,
)


class TestBrassFamilyRouting:
    def test_trumpet_always_treble_even_if_lower_than_trombone(self):
        # Trumpet 4 is pitch-grave (G3 midi 55), Trombone is pitch-acute (G4 midi 67).
        # Pitch-based would put trombone upper + trumpet lower. Family-based keeps
        # the trumpet in treble and the trombone in bass regardless.
        evs = [
            _Ev(0, "Trumpet in Bb 4", 55, "G3", 0.0, 4.0),
            _Ev(1, "Trombone",         67, "G4", 0.0, 4.0),
        ]
        upper, lower = _build_voice_elements(evs, 99, 99, family_map=_FAMILY_MAP_BRASS)
        upper_names = [s.pitch_name for _, _, slots in upper for s in slots]
        lower_names = [s.pitch_name for _, _, slots in lower for s in slots]
        assert upper_names == ["G3"]
        assert lower_names == ["G4"]

    def test_horns_go_to_treble(self):
        evs = [
            _Ev(0, "Horn in F 1", 60, "C4", 0.0, 2.0),
            _Ev(1, "Bass Trombone", 40, "E2", 0.0, 2.0),
        ]
        upper, lower = _build_voice_elements(evs, 99, 99, family_map=_FAMILY_MAP_BRASS)
        upper_names = [s.pitch_name for _, _, slots in upper for s in slots]
        lower_names = [s.pitch_name for _, _, slots in lower for s in slots]
        assert upper_names == ["C4"]
        assert lower_names == ["E2"]

    def test_treble_ranked_by_pitch_descending(self):
        evs = [
            _Ev(0, "Trumpet in Bb 1", 72, "C5", 0.0, 2.0),
            _Ev(1, "Trumpet in Bb 2", 69, "A4", 0.0, 2.0),
            _Ev(2, "Horn in F 1",     65, "F4", 0.0, 2.0),
            _Ev(3, "Trumpet in Bb 4", 60, "C4", 0.0, 2.0),
        ]
        upper, _ = _build_voice_elements(evs, 99, 99, family_map=_FAMILY_MAP_BRASS)
        names_in_order = [s.pitch_name for s in upper[0][2]]
        assert names_in_order == ["C5", "A4", "F4", "C4"]

    def test_abbr_and_rank_cover_all_known_parts(self):
        for part in _FAMILY_MAP_BRASS:
            assert part in _ABBR_BRASS
            assert part in _DEFAULT_RANK_BRASS

    def test_unknown_part_is_filtered_out(self):
        evs = [
            _Ev(0, "Tuba", 40, "E2", 0.0, 2.0),  # not in family map
            _Ev(1, "Trumpet in Bb 1", 70, "A#4", 0.0, 2.0),
        ]
        upper, lower = _build_voice_elements(evs, 99, 99, family_map=_FAMILY_MAP_BRASS)
        upper_names = [s.pitch_name for _, _, slots in upper for s in slots]
        lower_names = [s.pitch_name for _, _, slots in lower for s in slots]
        assert upper_names == ["A#4"]
        assert lower_names == []
