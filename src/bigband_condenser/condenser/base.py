"""Abstract base class for section condensers."""
from __future__ import annotations

from abc import ABC, abstractmethod


class SectionCondenser(ABC):
    """One condenser per Charter section.

    Each section condenser takes the N parts belonging to that section
    (after preprocess) and returns a tuple (upper_part, lower_part) of
    music21 Part objects representing the two staves of the grand staff.

    For sections rendered on a single staff (e.g. Drums in v1), lower_part
    may be None.
    """
    section_name: str = ""

    @abstractmethod
    def condense(self, parts: list):
        """Condense a list of music21.Part objects into (upper, lower).

        Args:
            parts: music21 Part objects (already in concert pitch via preprocess).

        Returns:
            Tuple (upper_part, lower_part). lower_part can be None for
            single-staff sections.
        """
        ...
