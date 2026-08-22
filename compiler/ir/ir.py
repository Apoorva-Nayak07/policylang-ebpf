"""
PolicyLang Intermediate Representation (IR).

The IR is the normalized representation between
semantic analysis and backend code generation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class IRComparison:
    """A normalized comparison operation."""

    field: str
    operator: str
    value: Union[str, int]


@dataclass(frozen=True)
class IRLogical:
    """A logical combination of two IR conditions."""

    operator: str
    left: "IRCondition"
    right: "IRCondition"


IRCondition = Union[IRComparison, IRLogical]


@dataclass(frozen=True)
class IRPolicy:
    """Normalized representation of a complete policy."""

    action: str
    direction: str
    condition: IRCondition