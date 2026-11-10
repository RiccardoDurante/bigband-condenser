"""Inject MusicXML <defaults> block for A4 landscape layout.

A4 landscape in standard MusicXML tenths (scaling: 7.0556 mm = 40 tenths):
  page-width  = 1684 tenths (297 mm)
  page-height = 1190 tenths (210 mm)

Also sets consistent staff-distance and system-distance so the 4 sections
(Reeds, Brass, Rhythm, Drums) sit on evenly spaced systems. Target density
approx 6-8 bars/page, 4 systems/page.
"""
from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path


# Jazz-standard compact labels for condensed score parts.
# Full name used at the first system, abbreviation on subsequent systems.
_DEFAULT_LABEL_MAP = {
    "Reeds (upper)":   ("Reeds 1", "R1"),
    "Reeds (lower)":   ("Reeds 2", "R2"),
    "Brass (upper)":   ("Brass 1", "B1"),
    "Brass (lower)":   ("Brass 2", "B2"),
    "Rhythm (treble)": ("Guitar",  "Gtr"),
    "Rhythm (bass)":   ("Bass",    "Bs"),
    "Rhythm (chords)": ("Piano",   "Pno"),
    "Drums":           ("Drums",   "Dr"),
}


def shrink_part_labels(root, label_map=None, font_full=9, font_abbr=8):
    """Shrink part-name/part-abbreviation fonts and apply clean jazz labels.

    Dorico uses <part-name> on the first system and <part-abbreviation> on
    subsequent ones. The defaults inherited from the source are verbose and
    push the staves apart, so we:
      - replace the name/abbrev with compact labels from label_map
      - set a smaller font-size so staves do not have to spread to make room
      - remove any <part-name-display> / <part-abbreviation-display> blocks
        that would override our text
    """
    if label_map is None:
        label_map = _DEFAULT_LABEL_MAP
    for sp in root.iter("score-part"):
        pn = sp.find("part-name")
        if pn is None:
            continue
        key = (pn.text or "").strip()
        full, abbr = label_map.get(key, (key, (key[:3] if key else "")))
        pn.text = full
        pn.set("font-size", str(font_full))
        # Insert or replace <part-abbreviation> right after <part-name>
        pa = sp.find("part-abbreviation")
        if pa is None:
            pa = ET.Element("part-abbreviation")
            idx = list(sp).index(pn)
            sp.insert(idx + 1, pa)
        pa.text = abbr
        pa.set("font-size", str(font_abbr))
        # Strip display variants so our text wins
        for tag in ("part-name-display", "part-abbreviation-display"):
            for sub in list(sp.findall(tag)):
                sp.remove(sub)


_DEFAULTS_XML = """
  <defaults>
    <scaling>
      <millimeters>7.0556</millimeters>
      <tenths>40</tenths>
    </scaling>
    <page-layout>
      <page-height>1190</page-height>
      <page-width>1684</page-width>
      <page-margins type="both">
        <left-margin>70</left-margin>
        <right-margin>70</right-margin>
        <top-margin>70</top-margin>
        <bottom-margin>70</bottom-margin>
      </page-margins>
    </page-layout>
    <system-layout>
      <system-margins>
        <left-margin>0</left-margin>
        <right-margin>0</right-margin>
      </system-margins>
      <system-distance>90</system-distance>
      <top-system-distance>110</top-system-distance>
    </system-layout>
    <staff-layout>
      <staff-distance>75</staff-distance>
    </staff-layout>
  </defaults>
"""


def inject_landscape_layout(xml_path):
    """Add or replace the <defaults> block in-place so the file is A4 landscape.

    Works on both score-partwise and score-timewise. Preserves the rest of
    the file (including comments and processing instructions).
    """
    path = Path(xml_path)
    content = path.read_text(encoding="utf-8")

    tree = ET.ElementTree(ET.fromstring(content))
    root = tree.getroot()

    # Remove existing <defaults> (if any)
    existing = root.find("defaults")
    if existing is not None:
        root.remove(existing)

    # Build new element from the literal XML, then insert after <work>,
    # <movement-number>, <movement-title>, <identification> if present
    new_defaults = ET.fromstring(_DEFAULTS_XML.strip())

    # Insertion point: after any of these children, before <part-list>
    insert_after = {"work", "movement-number", "movement-title", "identification"}
    insert_idx = 0
    for i, child in enumerate(list(root)):
        if child.tag in insert_after:
            insert_idx = i + 1
        elif child.tag == "part-list":
            break
    root.insert(insert_idx, new_defaults)

    # Preserve the XML declaration + DOCTYPE if present
    head_end = content.find("?>")
    header = content[: head_end + 2] + "\n" if head_end != -1 else ""
    # Preserve DOCTYPE
    doctype_start = content.find("<!DOCTYPE")
    if doctype_start != -1:
        doctype_end = content.find(">", doctype_start) + 1
        header += content[doctype_start:doctype_end] + "\n"

    # Remove any <page-layout>, <system-layout>, <staff-layout> inside
    # <print> elements so the global <defaults> rules unchallenged.
    for print_el in root.iter("print"):
        for local_tag in ("page-layout", "system-layout", "staff-layout"):
            for sub in list(print_el.findall(local_tag)):
                print_el.remove(sub)

    # Shrink and normalize part labels so staves do not need to spread
    # horizontally to make room for long inherited names.
    shrink_part_labels(root)

    body = ET.tostring(root, encoding="unicode")
    path.write_text(header + body, encoding="utf-8")
