"""Regression tests for triplet-preserving snap (TK-Reeds-02)."""
from fractions import Fraction

from bigband_condenser.condenser._common import _snap


def test_triplet_points_are_preserved():
    assert _snap(8 / 3) == Fraction(8, 3)
    assert _snap(10 / 3) == Fraction(10, 3)
    assert _snap(2 / 3) == Fraction(2, 3)
    assert _snap(1 / 3) == Fraction(1, 3)


def test_binary_points_unchanged():
    assert _snap(2.5) == 2.5
    assert _snap(0.125) == 0.125
    assert _snap(3.0) == 3


def test_midi_noise_still_snaps_to_binary_grid():
    assert _snap(0.0625) == 0
    assert _snap(2.01) == 2
    assert _snap(1.49) == 1.5


def test_start_plus_duration_is_exact():
    assert _snap(69.0) + _snap(2 / 3) == _snap(69 + 2 / 3)
