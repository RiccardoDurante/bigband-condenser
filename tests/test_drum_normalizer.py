"""Tests for drum_normalizer (Opzione 1 heuristic)."""


class TestDrumNormalizer:
    def _mk(self, step, octave, size=None):
        import music21
        n = music21.note.Unpitched()
        n.displayStep = step
        n.displayOctave = octave
        if size:
            n.style.noteSize = size
        return n

    def test_high_octave_becomes_x_notehead(self):
        import music21
        from bigband_condenser.drum_normalizer import normalize_drum_notation
        part = music21.stream.Part()
        for s, o in (("A", 5), ("B", 5), ("F", 5), ("G", 5)):
            part.insert(part.highestTime, self._mk(s, o))
        normalize_drum_notation(part)
        for n in part.recurse().notes:
            assert n.notehead == "x"
            assert n.stemDirection == "up"

    def test_low_octave_keeps_normal(self):
        import music21
        from bigband_condenser.drum_normalizer import normalize_drum_notation
        part = music21.stream.Part()
        for s, o in (("D", 3), ("E", 3), ("F", 3), ("A", 3), ("B", 1), ("D", 2)):
            part.insert(part.highestTime, self._mk(s, o))
        normalize_drum_notation(part)
        for n in part.recurse().notes:
            assert n.notehead == "normal"

    def test_cue_full_becomes_slash_stem_up(self):
        import music21
        from bigband_condenser.drum_normalizer import normalize_drum_notation
        part = music21.stream.Part()
        part.insert(0, self._mk("B", 5, size="full"))
        normalize_drum_notation(part)
        n = list(part.recurse().notes)[0]
        assert n.notehead == "slash"
        assert n.stemDirection == "up"
        assert n.style.noteSize is None  # marker cleared

    def test_cue_overrides_octave_rule(self):
        """size=full on a high-octave note yields slash, NOT x."""
        import music21
        from bigband_condenser.drum_normalizer import normalize_drum_notation
        part = music21.stream.Part()
        part.insert(0, self._mk("A", 5, size="full"))
        normalize_drum_notation(part)
        assert list(part.recurse().notes)[0].notehead == "slash"

    def test_cue_on_low_octave_still_slash(self):
        """size=full works regardless of octave."""
        import music21
        from bigband_condenser.drum_normalizer import normalize_drum_notation
        part = music21.stream.Part()
        part.insert(0, self._mk("D", 3, size="full"))
        normalize_drum_notation(part)
        assert list(part.recurse().notes)[0].notehead == "slash"

    def test_display_position_preserved(self):
        """Opzione 1: positions are NEVER remapped."""
        import music21
        from bigband_condenser.drum_normalizer import normalize_drum_notation
        part = music21.stream.Part()
        samples = [("E", 3), ("B", 5), ("D", 3), ("A", 5), ("F", 3)]
        for s, o in samples:
            part.insert(part.highestTime, self._mk(s, o))
        normalize_drum_notation(part)
        notes = list(part.recurse().notes)
        got = [(n.displayStep, n.displayOctave) for n in notes]
        assert got == samples

    def test_timing_preserved(self):
        import music21
        from bigband_condenser.drum_normalizer import normalize_drum_notation
        part = music21.stream.Part()
        n1 = self._mk("E", 3)
        n1.duration.quarterLength = 2.0
        n2 = self._mk("B", 5)
        n2.duration.quarterLength = 0.5
        part.insert(0.0, n1)
        part.insert(2.0, n2)
        normalize_drum_notation(part)
        notes = list(part.recurse().notes)
        assert float(notes[0].offset) == 0.0 and float(notes[0].duration.quarterLength) == 2.0
        assert float(notes[1].offset) == 2.0 and float(notes[1].duration.quarterLength) == 0.5

    def test_idempotent(self):
        import music21
        from bigband_condenser.drum_normalizer import normalize_drum_notation
        part = music21.stream.Part()
        for s, o, sz in (("E", 3, None), ("F", 3, None), ("B", 5, "full"),
                         ("B", 5, None), ("A", 5, None)):
            part.insert(part.highestTime, self._mk(s, o, size=sz))
        normalize_drum_notation(part)
        snap = [(n.displayStep, n.displayOctave, n.notehead, n.stemDirection)
                for n in part.recurse().notes]
        normalize_drum_notation(part)
        again = [(n.displayStep, n.displayOctave, n.notehead, n.stemDirection)
                 for n in part.recurse().notes]
        assert snap == again
