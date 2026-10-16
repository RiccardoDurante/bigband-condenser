"""Shared Pydantic data models for Big Band Condenser v1.

Based on bigband-ai/backend/shared/models.py (generic classes only, extracted
2026-10-16 for Big Band Condenser M3 production code). WriteRequest from the
donor project was NOT copied: it is specific to the generative pipeline.

Design pattern (preserved from donor):
- Pitch + duration + offset for individual notes (NoteData)
- Melodic sequences with source metadata (MelodyData)

These models are used across modules for cross-boundary communication.
"""
from pydantic import BaseModel, Field


class NoteData(BaseModel):
    """A single note in concert pitch."""

    pitch: str = Field(description="Concert pitch name, e.g. 'C4', 'Bb3', 'F#5'")
    duration: float = Field(
        description="Duration in quarter-note units (1.0 = quarter, 0.5 = eighth)"
    )
    offset: float = Field(
        description="Position from start of melody in quarter-note units"
    )


class MelodyData(BaseModel):
    """A sequence of notes extracted from the score or generated.

    The source_* metadata fields are the key value-add from the donor project:
    they track where each melody fragment came from in the original score,
    enabling traceability through the condensation pipeline.
    """

    notes: list[NoteData] = Field(default_factory=list)
    key: str | None = Field(default=None, description="Key signature, e.g. 'Bb major'")
    time_signature: str | None = Field(default=None, description="e.g. '4/4', '3/4'")
    tempo: float | None = Field(default=None, description="BPM")
    source_instrument: str | None = Field(default=None)
    source_bar_start: int | None = Field(default=None)
    source_bar_end: int | None = Field(default=None)
