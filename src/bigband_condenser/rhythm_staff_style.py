"""M6.1: parse <measure-style><slash/></measure-style> as a measure-flag state.

Finale exports <slash type="start"/> at the first measure of a style region
and <slash type="stop"/> when the style changes or ends. It may emit
redundant 'stop' events when the style attributes change (e.g. from
use-stems="no" to use-stems="yes"), so FIFO pairing of start/stop is
unreliable. Instead we walk measures in document order, maintain a
per-staff active flag, and record the per-measure state.

For single-staff parts the staff key is None.
For multi-staff parts (Piano = 2) the keys are "1" and "2".
"""
from __future__ import annotations

import xml.etree.ElementTree as ET


def extract_slash_measures(xml_path, part_id):
    """Return dict {staff_num_or_None: set_of_measure_numbers_where_slash_active}."""
    tree = ET.parse(str(xml_path))
    root = tree.getroot()
    part = next((p for p in root.iter("part") if p.get("id") == part_id), None)
    if part is None:
        return {}

    active = {}  # staff -> bool
    slash_by_staff: dict = {}

    for m in part.iter("measure"):
        try:
            mnum = int(m.get("number"))
        except Exception:
            continue
        # Apply any measure-style events at the top of this measure FIRST
        for attr in m.iter("attributes"):
            for ms in attr.iter("measure-style"):
                staff = ms.get("number")
                for slash in ms.iter("slash"):
                    typ = slash.get("type")
                    if typ == "start":
                        active[staff] = True
                    elif typ == "stop":
                        active[staff] = False
        # Record active state AFTER processing this measure's events
        for staff, is_active in active.items():
            if is_active:
                slash_by_staff.setdefault(staff, set()).add(mnum)

    return slash_by_staff


def coalesce_to_ranges(measure_set):
    """Convert a set of measure numbers to a list of (start, stop) contiguous ranges."""
    if not measure_set:
        return []
    sorted_m = sorted(measure_set)
    ranges = []
    start = sorted_m[0]
    prev = start
    for m in sorted_m[1:]:
        if m == prev + 1:
            prev = m
        else:
            ranges.append((start, prev))
            start = m
            prev = m
    ranges.append((start, prev))
    return ranges
