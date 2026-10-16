"""Section condensers for Big Band Condenser v1.

One condenser per Charter section (Reeds, Brass, Rhythm, Drums). Each
produces a tuple (upper_part, lower_part) representing the two staves
of the grand staff for that section (Drums: lower_part is None).
"""
from bigband_condenser.condenser.base import SectionCondenser
from bigband_condenser.condenser.reeds import ReedsCondenser

__all__ = ["SectionCondenser", "ReedsCondenser"]
