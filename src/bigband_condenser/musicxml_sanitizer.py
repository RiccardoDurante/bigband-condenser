"""MusicXML output sanitizer.

Addresses an issue observed with music21 v.10.5.0 MusicXML writer where
Rest objects inserted directly into Measure (not into a Voice) get
serialized with print-object="no" even when nothing in the music21 object
graph sets hideObjectOnPrint. In Dorico this renders as a visually-short
measure: the XML total duration matches the TimeSignature, but visible
elements cover only a fraction of the bar.

The sanitizer strips print-object="no" from any <note> element that
contains a <rest> child, restoring full visibility.
"""
from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET


def unhide_rests(xml_path: Path) -> int:
    """Remove print-object='no' from any <note> containing a <rest>.

    Returns the number of elements fixed.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    fixed = 0
    for note in root.iter("note"):
        if note.find("rest") is None:
            continue
        if note.get("print-object") == "no":
            del note.attrib["print-object"]
            if "print-spacing" in note.attrib:
                del note.attrib["print-spacing"]
            fixed += 1
    if fixed:
        tree.write(xml_path, encoding="utf-8", xml_declaration=True)
    return fixed
