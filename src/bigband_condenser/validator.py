"""Validation for the condensed output.

For each section (Reeds, Brass, Rhythm, Drums) compares the source parts
and the output parts and computes:
  - total note count source vs output
  - per-pitch, per-measure interval coverage
  - missing  = source sounding time not matched by output (pitch-quarters)
  - extra    = output sounding time not matched by source (pitch-quarters)
  - out_of_tolerance_measures = measures where missing or extra > tolerance

Pitched sections (Reeds, Brass, Rhythm): compare at concert pitch using
getSoundingPitch(). Unpitched section (Drums): compare only timing
(offset + duration) since there is no pitch to match.

Rhythm is treated specially:
  - Piano source is excluded from the fidelity comparison (Piano is
    hidden in the source by convention: its notes are never meant to
    be transcribed, only its chord symbols are used)
  - Only Guitar + Acoustic Bass are compared against the output
"""
from __future__ import annotations

import warnings
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path


_EPS = 1e-6

# Per-section default tolerances (quarter-lengths per bar).
# Brass is more permissive because edge anticipations and short ties
# across bar lines produce legitimate sub-quarter diffs.
# Reeds stays tight because it is a transcription fidelity gate.
DEFAULT_TOLERANCES = {"Reeds": 0.25, "Brass": 0.75, "Rhythm": 0.25}


@dataclass
class SectionReport:
    name: str
    source_note_count: int
    output_note_count: int
    missing_quarters: float
    extra_quarters: float
    source_total_quarters: float
    bars_out_of_tolerance: int
    bars_checked: int
    tolerance_per_bar: float
    details: list[str] = field(default_factory=list)

    bar_pass_pct_threshold: float = 0.02  # 2% default

    @property
    def passed(self) -> bool:
        if self.bars_checked == 0:
            return self.bars_out_of_tolerance == 0
        bad_pct = self.bars_out_of_tolerance / self.bars_checked
        return bad_pct <= self.bar_pass_pct_threshold

    @property
    def strict_passed(self) -> bool:
        return self.bars_out_of_tolerance == 0

    @property
    def missing_pct(self) -> float:
        if self.source_total_quarters <= _EPS:
            return 0.0
        return 100.0 * self.missing_quarters / self.source_total_quarters

    @property
    def extra_pct(self) -> float:
        if self.source_total_quarters <= _EPS:
            return 0.0
        return 100.0 * self.extra_quarters / self.source_total_quarters


@dataclass
class ValidationReport:
    sections: list[SectionReport] = field(default_factory=list)
    source_path: str = ""
    condensed_path: str = ""

    @property
    def passed(self) -> bool:
        return all(s.passed for s in self.sections)

    @property
    def total_source_notes(self) -> int:
        return sum(s.source_note_count for s in self.sections)

    @property
    def total_output_notes(self) -> int:
        return sum(s.output_note_count for s in self.sections)


def _merge(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1] + _EPS:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


def _total(intervals):
    return sum(e - s for s, e in intervals)


def _clip(intervals, lo, hi):
    res = []
    for s, e in intervals:
        s2, e2 = max(s, lo), min(e, hi)
        if e2 > s2 + _EPS:
            res.append([s2, e2])
    return res


def _intersect(a, b):
    i = j = 0
    res = []
    while i < len(a) and j < len(b):
        s = max(a[i][0], b[j][0])
        e = min(a[i][1], b[j][1])
        if e > s + _EPS:
            res.append([s, e])
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return res


def _collect_pitched(part):
    """Return {midi: [(start, end)]} absolute intervals for all notes in part."""
    acc = defaultdict(list)
    for n in part.recurse().notes:
        try:
            start = float(n.getOffsetInHierarchy(part))
        except Exception:
            start = float(n.offset)
        end = start + float(n.duration.quarterLength)
        for p in n.pitches:
            acc[p.midi].append((start, end))
    return acc


def _collect_unpitched(part):
    """Return sorted list of (offset_rounded, duration_rounded) for drum notes."""
    recs = []
    for n in part.recurse().notes:
        try:
            start = float(n.getOffsetInHierarchy(part))
        except Exception:
            start = float(n.offset)
        dur = float(n.duration.quarterLength)
        recs.append((round(start, 3), round(dur, 3)))
    return sorted(recs)


def _measure_bounds(score):
    """Measure numbers and absolute (start, end) from parts[0] of the source."""
    import music21
    if not score.parts:
        return []
    p0 = score.parts[0]
    bounds = []
    for m in p0.getElementsByClass(music21.stream.Measure):
        start = float(m.offset)
        end = start + float(m.duration.quarterLength)
        bounds.append((m.number, start, end))
    return bounds


def _fidelity_pitched(name, source_parts, output_parts, bounds, tolerance,
                     to_concert=True, exclude_measures=None):
    """Compare pitched note coverage source vs output, bar by bar."""
    source_pitched = defaultdict(list)
    output_pitched = defaultdict(list)
    for p in source_parts:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sp = p.toSoundingPitch(inPlace=False) if to_concert else p
        for midi, intervals in _collect_pitched(sp).items():
            source_pitched[midi].extend(intervals)
    for p in output_parts:
        for midi, intervals in _collect_pitched(p).items():
            output_pitched[midi].extend(intervals)
    src_m = {k: _merge(v) for k, v in source_pitched.items()}
    out_m = {k: _merge(v) for k, v in output_pitched.items()}

    source_total = sum(_total(v) for v in src_m.values())
    source_note_count = sum(sum(1 for _ in p.recurse().notes) for p in source_parts)
    output_note_count = sum(sum(1 for _ in p.recurse().notes) for p in output_parts)

    missing_total = extra_total = 0.0
    bars_bad = 0
    details = []
    excl = exclude_measures or set()
    bars_checked = 0
    for num, ms, me in bounds:
        if num in excl:
            continue
        bars_checked += 1
        missing = extra = 0.0
        for midi in set(src_m) | set(out_m):
            s_i = _clip(src_m.get(midi, []), ms, me)
            o_i = _clip(out_m.get(midi, []), ms, me)
            inter = _total(_intersect(s_i, o_i))
            missing += _total(s_i) - inter
            extra += _total(o_i) - inter
        missing_total += missing
        extra_total += extra
        if missing > tolerance or extra > tolerance:
            bars_bad += 1
            details.append(f"m{num}: missing={missing:.2f} extra={extra:.2f}")

    return SectionReport(
        name=name,
        source_note_count=source_note_count,
        output_note_count=output_note_count,
        missing_quarters=missing_total,
        extra_quarters=extra_total,
        source_total_quarters=source_total,
        bars_out_of_tolerance=bars_bad,
        bars_checked=bars_checked,
        tolerance_per_bar=tolerance,
        details=details[:100],
    )


def _fidelity_unpitched(name, source_parts, output_parts, tolerance):
    """Drums: compare exact (offset, duration) set equality (no pitch)."""
    source_set = set()
    for p in source_parts:
        source_set.update(_collect_unpitched(p))
    output_set = set()
    for p in output_parts:
        output_set.update(_collect_unpitched(p))

    missing = source_set - output_set
    extra = output_set - source_set
    source_note_count = sum(sum(1 for _ in p.recurse().notes) for p in source_parts)
    output_note_count = sum(sum(1 for _ in p.recurse().notes) for p in output_parts)

    bars_bad = 1 if (missing or extra) else 0
    details = []
    for m in list(missing)[:10]:
        details.append(f"missing @{m[0]} dur={m[1]}")
    for e in list(extra)[:10]:
        details.append(f"extra @{e[0]} dur={e[1]}")

    return SectionReport(
        name=name,
        source_note_count=source_note_count,
        output_note_count=output_note_count,
        missing_quarters=float(len(missing)),
        extra_quarters=float(len(extra)),
        source_total_quarters=float(len(source_set)),
        bars_out_of_tolerance=bars_bad,
        bars_checked=1,
        tolerance_per_bar=tolerance,
        details=details,
    )


def validate(source_path, condensed_path, tolerance_per_bar=0.25):
    """Full validation of a condensed MusicXML against its source."""
    from music21 import converter
    from bigband_condenser.classifier import (
        classify_score,
        SECTION_REEDS, SECTION_BRASS, SECTION_RHYTHM, SECTION_DRUMS,
    )
    from bigband_condenser.preprocessor import preprocess

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        source_score = converter.parse(str(source_path))
        condensed_score = converter.parse(str(condensed_path))
    result = preprocess(source_score, source_path)
    cls = classify_score(source_path)

    def _source_parts_for(section, exclude_keyword=None):
        names = {c.part_name for c in cls
                 if c.section == section and not c.is_hidden}
        parts = [p for p in result.score.parts if (p.partName or "") in names]
        if exclude_keyword:
            parts = [p for p in parts
                     if exclude_keyword not in (p.partName or "").lower()]
        return parts

    def _output_parts_matching(keyword):
        return [p for p in condensed_score.parts
                if keyword in (p.partName or "").lower()]

    bounds = _measure_bounds(result.score)
    report = ValidationReport(source_path=str(source_path),
                              condensed_path=str(condensed_path))

    # Reeds
    src = _source_parts_for(SECTION_REEDS)
    out = _output_parts_matching("reeds")
    if src and out:
        tol = DEFAULT_TOLERANCES.get("Reeds", tolerance_per_bar)
        report.sections.append(
            _fidelity_pitched("Reeds", src, out, bounds, tol, True)
        )

    # Brass
    src = _source_parts_for(SECTION_BRASS)
    out = _output_parts_matching("brass")
    if src and out:
        tol = DEFAULT_TOLERANCES.get("Brass", tolerance_per_bar)
        report.sections.append(
            _fidelity_pitched("Brass", src, out, bounds, tol, True)
        )

    # Rhythm: compare Guitar + Acoustic Bass only (Piano hidden by design).
    # Measures flagged as slash regions in the source are excluded from the
    # fidelity gate: by Opzione D they are intentionally replaced with slash
    # notation + big-band hit pattern, so note-by-note comparison would
    # produce false FAILs.
    src = [p for p in _source_parts_for(SECTION_RHYTHM)
           if "piano" not in (p.partName or "").lower()]
    # D-041: output part names are 'Guitar'/'Bass'/'Piano' (not 'Rhythm ...')
    out = [p for p in condensed_score.parts
           if (p.partName or "").lower() in {"guitar", "bass", "piano"}]
    if src and out:
        from bigband_condenser.rhythm_staff_style import extract_slash_measures
        import xml.etree.ElementTree as ET
        # music21 part.id is the partName (or 'Pxx-StaffN' for multi-staff
        # parts). extract_slash_measures needs the MusicXML score-part id
        # ('P14', 'P15', ...). Build the mapping from the raw XML.
        name_to_id = {}
        try:
            root = ET.parse(str(source_path)).getroot()
            for sp in root.iter("score-part"):
                pn_el = sp.find("part-name")
                if pn_el is not None and pn_el.text:
                    name_to_id[pn_el.text.strip()] = sp.get("id")
        except Exception:
            pass
        excl = set()
        for part in src:
            name = (part.partName or "").strip()
            xml_id = name_to_id.get(name)
            if not xml_id:
                continue
            try:
                per_staff = extract_slash_measures(source_path, xml_id)
                for staff_set in per_staff.values():
                    excl |= staff_set
            except Exception:
                pass
        tol = DEFAULT_TOLERANCES.get("Rhythm", tolerance_per_bar)
        report.sections.append(
            _fidelity_pitched("Rhythm", src, out, bounds, tol,
                              to_concert=False, exclude_measures=excl)
        )

    # Drums: unpitched comparison
    src = _source_parts_for(SECTION_DRUMS)
    out = _output_parts_matching("drums")
    if src and out:
        report.sections.append(
            _fidelity_unpitched("Drums", src, out, tolerance_per_bar)
        )

    return report


def format_report(report, detailed=True):
    lines = []
    lines.append("=" * 70)
    lines.append("BIG BAND CONDENSER - VALIDATION REPORT")
    lines.append("=" * 70)
    lines.append(f"Source:    {report.source_path}")
    lines.append(f"Condensed: {report.condensed_path}")
    lines.append("")
    lines.append(f"{'Section':<10} {'Src':>6} {'Out':>6} {'Missing':>10} "
                 f"{'Extra':>10} {'Bars bad':>10} {'Verdict':>8}")
    lines.append("-" * 70)
    for s in report.sections:
        if s.name == "Drums":
            miss_str = f"{int(s.missing_quarters)} ev"
            extra_str = f"{int(s.extra_quarters)} ev"
        else:
            miss_str = f"{s.missing_quarters:5.1f} ({s.missing_pct:3.1f}%)"
            extra_str = f"{s.extra_quarters:5.1f} ({s.extra_pct:3.1f}%)"
        if s.strict_passed:
            verdict = "PASS"
        elif s.passed:
            verdict = "PASS*"
        else:
            verdict = "FAIL"
        lines.append(f"{s.name:<10} {s.source_note_count:>6} "
                     f"{s.output_note_count:>6} {miss_str:>10} {extra_str:>10} "
                     f"{s.bars_out_of_tolerance:>5}/{s.bars_checked:<4} "
                     f"{verdict:>8}")
    lines.append("-" * 70)
    verdict = "PASS" if report.passed else "FAIL"
    lines.append(f"OVERALL: {verdict}  "
                 f"(total {report.total_source_notes} src -> "
                 f"{report.total_output_notes} out notes)")
    if detailed:
        for s in report.sections:
            if s.details:
                lines.append("")
                lines.append(f"[{s.name}] out-of-tolerance details "
                             f"(first {len(s.details)}):")
                for d in s.details:
                    lines.append(f"  {d}")
    lines.append("=" * 70)
    return "\n".join(lines)
