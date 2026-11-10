"""M10: generate a landscape PDF from a condensed MusicXML via LilyPond.

Uses musicxml2ly (LilyPond's official converter) when available for better
fidelity with the source MusicXML. Falls back to music21 if musicxml2ly
is not reachable.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import warnings
from pathlib import Path


_WINGET_BASE = (
    r"C:\Users\ricca\AppData\Local\Microsoft\WinGet\Packages"
    r"\LilyPond.LilyPond_Microsoft.Winget.Source_8wekyb3d8bbwe\lilypond-2.24.4"
)
_LILY_EXE = _WINGET_BASE + r"\bin\lilypond.exe"
_MUSICXML2LY = _WINGET_BASE + r"\bin\musicxml2ly.py"
_LILY_PYLIB = _WINGET_BASE + r"\share\lilypond\2.24.4\python"


def _find_lilypond():
    exe = shutil.which("lilypond")
    if exe:
        return exe
    if Path(_LILY_EXE).exists():
        return _LILY_EXE
    raise RuntimeError("lilypond.exe not found.")


_TOPLEVEL = r"""
#(set-default-paper-size "a4" 'landscape)
"""

_PAPER_BLOCK = r"""
\paper {
  top-margin = 15\mm
  bottom-margin = 15\mm
  left-margin = 15\mm
  right-margin = 15\mm
  ragged-last-bottom = ##f
  ragged-bottom = ##f
  max-systems-per-page = #4
  min-systems-per-page = #3
  indent = 25\mm
  short-indent = 15\mm
  system-system-spacing.basic-distance = #22
  system-system-spacing.minimum-distance = #18
  system-system-spacing.padding = #4
  system-system-spacing.stretchability = #30
  staff-staff-spacing.basic-distance = #11
  staff-staff-spacing.minimum-distance = #9
  staff-staff-spacing.padding = #1
  print-page-number = ##t
}

\layout {
  \context {
    \Score
    % Uniform horizontal spacing: all bars get similar width regardless of
    % how many notes they contain. This is the main lever against the
    % "some bars tiny, some huge" effect.
    \override SpacingSpanner.uniform-stretching = ##t
    \override SpacingSpanner.strict-note-spacing = ##f
    \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/8)
  }
}
"""


def _convert_via_musicxml2ly(xml_path, ly_path):
    if not Path(_MUSICXML2LY).exists():
        raise FileNotFoundError(_MUSICXML2LY)
    env = os.environ.copy()
    env["PYTHONPATH"] = _LILY_PYLIB + os.pathsep + env.get("PYTHONPATH", "")
    cmd = [sys.executable, _MUSICXML2LY, "-o", str(ly_path), str(xml_path)]
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        raise RuntimeError(
            f"musicxml2ly exit {result.returncode}: {result.stderr[:400]}"
        )
    return ly_path


def _convert_via_music21(xml_path, ly_path):
    warnings.simplefilter("ignore")
    from music21 import converter
    score = converter.parse(str(xml_path))
    score.write("lily", fp=str(ly_path))
    return ly_path


def convert_musicxml_to_ly(xml_path, ly_path):
    try:
        print("  trying musicxml2ly (LilyPond native) ...")
        _convert_via_musicxml2ly(xml_path, ly_path)
        print("  musicxml2ly OK")
        return ly_path
    except Exception as e:
        print(f"  musicxml2ly failed: {str(e)[:200]}")
        print("  falling back to music21 ...")
        return _convert_via_music21(xml_path, ly_path)


def _strip_existing_paper(content):
    content = re.sub(r"#\(set-(default-)?paper-size[^)]*\)", "", content)
    out = []
    i = 0
    while i < len(content):
        if content.startswith(r"\paper", i):
            brace_start = content.find("{", i)
            if brace_start == -1:
                out.append(content[i]); i += 1; continue
            depth = 0
            j = brace_start
            while j < len(content):
                if content[j] == "{":
                    depth += 1
                elif content[j] == "}":
                    depth -= 1
                    if depth == 0:
                        j += 1
                        break
                j += 1
            i = j
        else:
            out.append(content[i])
            i += 1
    return "".join(out)


def _inject_breaks(ly_content, bars_per_system=6):
    """Insert \\break after every Nth bar check '|' to force uniform density."""
    # LilyPond uses bar check '|' at measure boundaries. We count them
    # in each Staff block and inject \break every N.
    # Conservative implementation: only when |\n or |} patterns are clean.
    lines = ly_content.splitlines(keepends=True)
    out = []
    bar_count = 0
    in_notes_block = False
    for line in lines:
        out.append(line)
        if re.search(r"\\new\s+Staff", line):
            bar_count = 0
        # Count bar-checks at end of line
        if re.search(r"\|\s*$", line.rstrip()):
            bar_count += 1
            if bar_count % bars_per_system == 0:
                # Insert a line break directive; LilyPond's optimal-breaking
                # will respect it as a suggestion.
                out.append("              \\break\n")
    return "".join(out)


def patch_ly(ly_path, bars_per_system=6):
    content = Path(ly_path).read_text(encoding="utf-8")
    content = _strip_existing_paper(content)
    # Inject paper + toplevel directives after \version
    lines = content.splitlines(keepends=True)
    new_lines = []
    injected = False
    for line in lines:
        new_lines.append(line)
        if (not injected) and line.strip().startswith(r"\version"):
            new_lines.append(_TOPLEVEL)
            new_lines.append(_PAPER_BLOCK)
            injected = True
    if not injected:
        new_lines = [_TOPLEVEL, _PAPER_BLOCK] + new_lines
    content = "".join(new_lines)
    # Note: we skip the \break injection for now because musicxml2ly output
    # structure differs from music21's and detecting bar boundaries safely
    # requires parsing. Left as FR-M10-polish. Uniform-stretching above
    # already provides most of the benefit.
    Path(ly_path).write_text(content, encoding="utf-8")


def compile_pdf(ly_path, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = out_dir / Path(ly_path).stem
    lily = _find_lilypond()
    cmd = [lily, "-o", str(stem), str(ly_path)]
    print(f"  cmd: lilypond -o {stem} {ly_path}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stderr:
        tail = "\n".join(result.stderr.splitlines()[-10:])
        print("  [lilypond tail]")
        print(tail, file=sys.stderr)
    return result.returncode


def main(argv=None):
    parser = argparse.ArgumentParser(prog="build_pdf")
    parser.add_argument("input", type=Path)
    parser.add_argument("-o", "--output-dir", type=Path, default=Path("samples"))
    parser.add_argument("--keep-ly", action="store_true")
    args = parser.parse_args(argv)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    ly_path = args.output_dir / (args.input.stem + ".ly")

    print(f"[1/3] Converting {args.input.name} -> LilyPond ...")
    convert_musicxml_to_ly(args.input, ly_path)
    print(f"      wrote: {ly_path} ({ly_path.stat().st_size // 1024} KB)")

    print(f"[2/3] Patching .ly with landscape + uniform spacing ...")
    patch_ly(ly_path)

    print(f"[3/3] Compiling with LilyPond ...")
    rc = compile_pdf(ly_path, args.output_dir)
    if rc != 0:
        return rc

    pdf_path = args.output_dir / (args.input.stem + ".pdf")
    if pdf_path.exists():
        kb = pdf_path.stat().st_size // 1024
        print(f"DONE: {pdf_path} ({kb} KB)")

    if not args.keep_ly:
        ly_path.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
