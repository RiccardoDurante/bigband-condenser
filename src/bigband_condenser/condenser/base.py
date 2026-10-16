"""Abstract base class for section condensers."""
from __future__ import annotations

from abc import ABC, abstractmethod


class SectionCondenser(ABC):
    """One condenser per Charter section.

    Each section condenser takes the N parts belonging to that section
    (after preprocess) and returns a tuple (upper_part, lower_part) of
    music21 Part objects representing the two staves of the grand staff.

    Optional keyword arg source_score: pass the parsed music21 Score of
    the source file so the condenser can preserve metadata (key signature,
    time signature, tempo marking) in the output Parts.
    """
    section_name: str = ""

    @abstractmethod
    def condense(self, parts: list, source_score=None):
        """Condense a list of music21.Part objects into (upper, lower).

        Args:
            parts: music21 Part objects (already in concert pitch via preprocess).
            source_score: Optional music21.Score to extract metadata from.
                          If None, the output Parts have no key/time/tempo.

        Returns:
            Tuple (upper_part, lower_part). lower_part can be None for
            single-staff sections (e.g. drums).
        """
        ...
