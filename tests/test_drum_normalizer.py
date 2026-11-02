"""Tests for drum_normalizer (Opzione 3, by instrument name)."""


class TestDrumNormalizerByName:
    def _make_part_with_instrument(self, inst_name, display_step="D", display_octave=3):
        """Helper: create a Part containing one Unpitched note associated with
        a music21.instrument.Instrument whose instrumentName is set."""
        import music21
        part = music21.stream.Part()
        inst = music21.instrument.UnpitchedPercussion()
        inst.instrumentName = inst_name
        part.insert(0, inst)
        n = music21.note.Unpitched()
        n.displayStep = display_step
        n.displayOctave = display_octave
        part.insert(0, n)
        return part

    def test_bass_drum_to_f4_down(self):
        from bigband_condenser.drum_normalizer import normalize_drum_notation
        part = self._make_part_with_instrument("Bass Drum")
        normalize_drum_notation(part)
        import music21
        n = next(x for x in part.recurse().notes if isinstance(x, music21.note.Unpitched))
        assert (n.displayStep, n.displayOctave) == ("F", 4)
        assert n.notehead == "normal"
        assert n.stemDirection == "down"

    def test_snare_to_c5_up(self):
        from bigband_condenser.drum_normalizer import normalize_drum_notation
        part = self._make_part_with_instrument("Snare Drum")
        normalize_drum_notation(part)
        import music21
        n = next(x for x in part.recurse().notes if isinstance(x, music21.note.Unpitched))
        assert (n.displayStep, n.displayOctave) == ("C", 5)
        assert n.notehead == "normal"
        assert n.stemDirection == "up"

    def test_hihat_closed_to_g5_x(self):
        from bigband_condenser.drum_normalizer import normalize_drum_notation
        part = self._make_part_with_instrument("Hi-Hat Closed")
        normalize_drum_notation(part)
        import music21
        n = next(x for x in part.recurse().notes if isinstance(x, music21.note.Unpitched))
        assert (n.displayStep, n.displayOctave) == ("G", 5)
        assert n.notehead == "x"

    def test_ride_to_f5_x(self):
        from bigband_condenser.drum_normalizer import normalize_drum_notation
        part = self._make_part_with_instrument("Ride Cymbal")
        normalize_drum_notation(part)
        import music21
        n = next(x for x in part.recurse().notes if isinstance(x, music21.note.Unpitched))
        assert (n.displayStep, n.displayOctave) == ("F", 5)
        assert n.notehead == "x"

    def test_crash_to_a5_x(self):
        from bigband_condenser.drum_normalizer import normalize_drum_notation
        part = self._make_part_with_instrument("Crash Cymbal")
        normalize_drum_notation(part)
        import music21
        n = next(x for x in part.recurse().notes if isinstance(x, music21.note.Unpitched))
        assert (n.displayStep, n.displayOctave) == ("A", 5)
        assert n.notehead == "x"

    def test_rhythm_cues_to_slash(self):
        from bigband_condenser.drum_normalizer import normalize_drum_notation
        part = self._make_part_with_instrument("Rhythm Cues")
        normalize_drum_notation(part)
        import music21
        n = next(x for x in part.recurse().notes if isinstance(x, music21.note.Unpitched))
        assert n.notehead == "slash"
        assert (n.displayStep, n.displayOctave) == ("A", 5)

    def test_ride_bell_diamond(self):
        from bigband_condenser.drum_normalizer import normalize_drum_notation
        part = self._make_part_with_instrument("Ride Bell")
        normalize_drum_notation(part)
        import music21
        n = next(x for x in part.recurse().notes if isinstance(x, music21.note.Unpitched))
        assert n.notehead == "diamond"

    def test_finale_percent_g_separator_handled(self):
        """Finale uses '%g' as word separator in instrument names (e.g. 'Hi-Hat%g Closed')."""
        from bigband_condenser.drum_normalizer import normalize_drum_notation
        part = self._make_part_with_instrument("Hi-Hat%g Closed")
        normalize_drum_notation(part)
        import music21
        n = next(x for x in part.recurse().notes if isinstance(x, music21.note.Unpitched))
        assert (n.displayStep, n.displayOctave) == ("G", 5)
        assert n.notehead == "x"

    def test_unknown_instrument_left_alone(self):
        """Defensive: unknown names must NOT be rewritten."""
        from bigband_condenser.drum_normalizer import normalize_drum_notation
        part = self._make_part_with_instrument("Vibraphone", display_step="C", display_octave=5)
        normalize_drum_notation(part)
        import music21
        n = next(x for x in part.recurse().notes if isinstance(x, music21.note.Unpitched))
        assert (n.displayStep, n.displayOctave) == ("C", 5)  # unchanged

    def test_idempotent(self):
        from bigband_condenser.drum_normalizer import normalize_drum_notation
        part = self._make_part_with_instrument("Snare Drum")
        normalize_drum_notation(part)
        import music21
        snap_notes = list(part.recurse().notes)
        before = [(n.displayStep, n.displayOctave, n.notehead, n.stemDirection) for n in snap_notes]
        normalize_drum_notation(part)
        after = [(n.displayStep, n.displayOctave, n.notehead, n.stemDirection) for n in snap_notes]
        assert before == after
