"""Tests for DrumsCondenser (preserver, M7)."""
import warnings


class TestDrumsPreserver:
    def test_output_has_percussion_clef(self):
        import music21
        from bigband_condenser.condenser import DrumsCondenser
        part = music21.stream.Part()
        part.partName = "Drum Set 1"
        part.insert(0, music21.clef.TrebleClef())  # wrong clef, should be swapped
        m = music21.stream.Measure(number=1)
        n = music21.note.Unpitched()
        n.duration.quarterLength = 1.0
        m.insert(0, n)
        part.insert(0, m)
        score = music21.stream.Score()
        score.insert(0, part)
        output, lower = DrumsCondenser().condense([part], source_score=score)
        assert lower is None
        clefs = list(output.recurse().getElementsByClass(music21.clef.Clef))
        assert any(isinstance(c, music21.clef.PercussionClef) for c in clefs)
        assert not any(isinstance(c, music21.clef.TrebleClef) for c in clefs)

    def test_output_preserves_note_count(self):
        import music21
        from bigband_condenser.condenser import DrumsCondenser
        part = music21.stream.Part()
        part.partName = "Drum Set 1"
        m = music21.stream.Measure(number=1)
        for i in range(4):
            n = music21.note.Unpitched()
            n.duration.quarterLength = 1.0
            m.insert(i, n)
        part.insert(0, m)
        score = music21.stream.Score()
        score.insert(0, part)
        output, _ = DrumsCondenser().condense([part], source_score=score)
        assert sum(1 for _ in output.recurse().notes) == 4

    def test_empty_parts_returns_empty(self):
        import music21
        from bigband_condenser.condenser import DrumsCondenser
        output, lower = DrumsCondenser().condense([], source_score=None)
        assert sum(1 for _ in output.recurse().notes) == 0
        assert lower is None

    def test_text_expression_preserved(self):
        import music21
        from bigband_condenser.condenser import DrumsCondenser
        from music21 import expressions
        part = music21.stream.Part()
        part.partName = "Drum Set 1"
        m = music21.stream.Measure(number=1)
        te = expressions.TextExpression("Conducted")
        m.insert(0, te)
        n = music21.note.Unpitched()
        n.duration.quarterLength = 2.0
        m.insert(0, n)
        part.insert(0, m)
        score = music21.stream.Score()
        score.insert(0, part)
        output, _ = DrumsCondenser().condense([part], source_score=score)
        tes = list(output.recurse().getElementsByClass(expressions.TextExpression))
        assert len(tes) == 1
        assert tes[0].content == "Conducted"
