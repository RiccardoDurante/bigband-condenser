"""Check whether the skeleton part is really free of Rest objects after purge."""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from music21 import converter, stream, note, clef  # noqa: E402
from bigband_condenser.condenser.reeds import _build_skeleton_part  # noqa: E402
from bigband_condenser.preprocessor import preprocess  # noqa: E402

EXTRACT = REPO_ROOT / "samples" / "kronos_kai_kairos_extract.musicxml"

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    score = converter.parse(str(EXTRACT))
result = preprocess(score, EXTRACT)
skeleton = _build_skeleton_part(result.score, "Test", clef.TrebleClef())

rests = list(skeleton.recurse().getElementsByClass(note.Rest))
hidden = []
for r in rests:
    style = getattr(r, "style", None)
    is_hidden = style is not None and getattr(style, "hideObjectOnPrint", False)
    hidden.append(is_hidden)

print(f"Rest objects remaining in skeleton: {len(rests)}")
print(f"  of which hidden (print-object=no): {sum(hidden)}")
print(f"  of which visible: {len(rests) - sum(hidden)}")
if rests:
    print()
    print("First 10 Rest objects:")
    for r in rests[:10]:
        site = r.activeSite
        site_type = type(site).__name__ if site else "None"
        meas_num = "?"
        parent = site
        while parent is not None:
            if isinstance(parent, stream.Measure):
                meas_num = parent.number
                break
            parent = getattr(parent, "activeSite", None)
        style = getattr(r, "style", None)
        is_hid = style is not None and getattr(style, "hideObjectOnPrint", False)
        print(f"  M{meas_num} offset={float(r.offset):.3f} ql={float(r.duration.quarterLength):.3f} site={site_type} hidden={is_hid}")
