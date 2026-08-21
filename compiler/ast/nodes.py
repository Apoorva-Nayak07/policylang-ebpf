"""
PolicyLang Abstract Syntax Tree (AST)

The AST represents the structure of a parsed PolicyLang program.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class Comparison:
    """Represents a comparison such as source.ip == 10.0.0.5."""

    field: str
    operator: str
    value: Union[str, int]


@dataclass(frozen=True)
class LogicalExpression:
    """Represents AND/OR between two conditions."""

    operator: str
    left: "Condition"
    right: "Condition"


Condition = Union[Comparison, LogicalExpression]


@dataclass(frozen=True)
class Policy:
    """Root node representing a complete PolicyLang policy."""

    action: str
    direction: str
    condition: Condition