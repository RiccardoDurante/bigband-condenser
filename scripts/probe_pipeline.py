"""Reproduce the condense pipeline without makeBeams, to isolate the source of hidden rests."""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from music21 import converter, metadata, stream, note  # noqa: E402
import bigband_condenser.condenser.reeds as reeds_mod  # noqa: E402
from bigband_condenser.classifier import classify_score, SECTION_REEDS  # noqa: E402
from bigband_condenser.condenser import ReedsCondenser  # noqa: E402
from bigband_condenser.preprocessor import preprocess  # noqa: E402

# Monkey-patch makeBeams to be a no-op, so we can see if it's the culprit
_original_makeBeams = stream.Part.makeBeams
def _no_op_makeBeams(self, *args, **kwargs):
    return self
stream.Part.makeBeams = _no_op_makeBeams

EXTRACT = REPO_ROOT / "samples" / "kronos_kai_kairos_extract.musicxml"
OUT = REPO_ROOT / "samples" / "preview_reeds_probe_nobeams.musicxml"

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    score = converter.parse(str(EXTRACT))
result = preprocess(score, EXTRACT)
classifications = classify_score(EXTRACT)
reed_names = {c.part_name for c in classifications if c.section == SECTION_REEDS and not c.is_hidden}
reed_parts = [p for p in result.score.parts if (p.partName or "") in reed_names]

upper, lower = ReedsCondenser().condense(reed_parts, source_score=result.score)

# Count hidden rests in upper and lower BEFORE writing
def count_hidden(part):
    n_total = 0
    n_hidden = 0
    for r in part.recurse().getElementsByClass(note.Rest):
        n_total += 1
        style = getattr(r, "style", None)
        if style is not None and getattr(style, "hideObjectOnPrint", False):
            n_hidden += 1
    return n_total, n_hidden

u_total, u_hidden = count_hidden(upper)
l_total, l_hidden = count_hidden(lower)
print(f"In-memory counts (before XML write):")
print(f"  upper: {u_total} rests, {u_hidden} hidden")
print(f"  lower: {l_total} rests, {l_hidden} hidden")

out = stream.Score()
out.insert(0, upper)
out.insert(0, lower)
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    out.write("musicxml", fp=str(OUT))

print()
print(f"Written: {OUT.name}")
