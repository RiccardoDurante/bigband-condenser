"""Tests for bigband_condenser.classifier."""
import pytest

from bigband_condenser.classifier import (
    classify_section,
    detect_hidden_part_names,
    classify_score,
    summarize,
    SECTION_REEDS, SECTION_BRASS, SECTION_RHYTHM, SECTION_DRUMS, SECTION_UNKNOWN,
    PartClassification,
)


class TestClassifySection:
    def test_reeds(self):
        assert classify_section("Alto Sax") == SECTION_REEDS
        assert classify_section("Soprano Sax") == SECTION_REEDS
        assert classify_section("Baritone Sax") == SECTION_REEDS
        assert classify_section("Clarinet") == SECTION_REEDS
        assert classify_section("Flute") == SECTION_REEDS

    def test_brass(self):
        assert classify_section("Trumpet in Bb 1") == SECTION_BRASS
        assert classify_section("Horn in F 1") == SECTION_BRASS
        assert classify_section("Trombone") == SECTION_BRASS
        assert classify_section("Bass Trombone") == SECTION_BRASS
        assert classify_section("Flugelhorn") == SECTION_BRASS

    def test_rhythm(self):
        assert classify_section("Piano") == SECTION_RHYTHM
        assert classify_section("Electric Guitar") == SECTION_RHYTHM
        assert classify_section("Acoustic Bass") == SECTION_RHYTHM

    def test_drums(self):
        assert classify_section("Drum Set 1") == SECTION_DRUMS
        assert classify_section("Drum Set 2") == SECTION_DRUMS
        assert classify_section("Percussion") == SECTION_DRUMS

    def test_unknown(self):
        assert classify_section("Theremin") == SECTION_UNKNOWN
        assert classify_section("") == SECTION_UNKNOWN
        assert classify_section("   ") == SECTION_UNKNOWN

    def test_case_insensitive(self):
        assert classify_section("ALTO SAX") == SECTION_REEDS
        assert classify_section("trumpet") == SECTION_BRASS


class TestDetectHiddenParts:
    def test_kronos_extract_hides_drum_set_2(self, kronos_extract_path):
        hidden = detect_hidden_part_names(kronos_extract_path)
        assert hidden == {"Drum Set 2"}


class TestClassifyScore:
    def test_kronos_extract_18_parts(self, kronos_extract_path):
        results = classify_score(kronos_extract_path)
        assert len(results) == 18
        assert all(isinstance(r, PartClassification) for r in results)

    def test_kronos_extract_sections(self, kronos_extract_path):
        results = classify_score(kronos_extract_path)
        by_section = {}
        for r in results:
            by_section.setdefault(r.section, []).append(r.part_name)
        assert len(by_section[SECTION_REEDS]) == 5
        assert len(by_section[SECTION_BRASS]) == 8
        assert len(by_section[SECTION_RHYTHM]) == 3
        assert len(by_section[SECTION_DRUMS]) == 2
        assert SECTION_UNKNOWN not in by_section

    def test_drum_set_2_flagged_hidden(self, kronos_extract_path):
        results = classify_score(kronos_extract_path)
        hidden = [r for r in results if r.is_hidden]
        assert len(hidden) == 1
        assert hidden[0].part_name == "Drum Set 2"


class TestSummarize:
    def test_kronos_summary_matches_spike(self, kronos_extract_path):
        results = classify_score(kronos_extract_path)
        s = summarize(results)
        assert s["total_xml_parts"] == 18
        assert s["hidden_count"] == 1
        assert s["total_logical_visible"] == 17
        assert s["logical_visible"][SECTION_REEDS] == 5
        assert s["logical_visible"][SECTION_BRASS] == 8
        assert s["logical_visible"][SECTION_RHYTHM] == 3
        assert s["logical_visible"][SECTION_DRUMS] == 1
