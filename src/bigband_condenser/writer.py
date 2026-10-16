"""MusicXML writer wrapper for Big Band Condenser v1.

Thin wrapper around music21.write() that:
- Logs the write operation and output size
- Provides specific error diagnostics for R27 (sub-semicroma durations) that
  suggest running preprocess() first
- Optionally re-parses the output as a smoke-test verification

Rationale (Spike M2):
- Preprocessor (R27+R28+R30 mitigations) must run BEFORE this writer.
- Without preprocess, music21.write() raises MusicXMLExportException on
  Finale drum sub-32th durations. This writer catches that and emits a
  diagnostic pointing at preprocess().
- With preprocess run, music21.write() succeeds and output is valid.
"""
from __future__ import annotations

import logging
import warnings
from pathlib import Path

logger = logging.getLogger(__name__)


class CondenserWriteError(Exception):
    """Raised when music21.write() fails for a Big Band Condenser-specific reason."""


def write_musicxml(
    score,
    output_path: Path | str,
    *,
    title: str | None = None,
    verify: bool = True,
) -> Path:
    """Write a Score to MusicXML, with diagnostics and optional verify.

    Args:
        score: A music21 Score (preferably one that has passed through preprocess()).
        output_path: Where to write the .musicxml file.
        title: Optional title to set on the score metadata before writing.
        verify: If True, re-parse the output file and raise if parse fails.

    Returns:
        The Path of the written file.

    Raises:
        CondenserWriteError: If music21.write() fails. Includes a hint about
            running preprocess() first if the error signature matches R27.
    """
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    if title is not None:
        from music21 import metadata
        if score.metadata is None:
            score.metadata = metadata.Metadata()
        score.metadata.title = title

    logger.info("Writing MusicXML to %s", out)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            score.write("musicxml", fp=str(out))
    except Exception as e:
        msg = str(e)
        if "2048th" in msg or "duration" in msg.lower() and "too short" in msg.lower():
            raise CondenserWriteError(
                f"music21.write() failed on sub-32th duration (R27). "
                f"Did you forget to call preprocess() first? Original error: {e}"
            ) from e
        raise CondenserWriteError(f"music21.write() failed: {e}") from e

    size = out.stat().st_size
    logger.info("Wrote %d bytes", size)

    if verify:
        _verify_output_parses(out)

    return out


def _verify_output_parses(path: Path) -> None:
    """Smoke-test: re-parse the output file and confirm it loads without errors."""
    from music21 import converter
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            _ = converter.parse(str(path))
    except Exception as e:
        raise CondenserWriteError(
            f"Output file {path.name} failed to re-parse (invalid MusicXML?): {e}"
        ) from e
    logger.info("Verification: output file re-parses OK")
