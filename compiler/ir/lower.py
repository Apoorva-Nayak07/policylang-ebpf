"""
PolicyLang AST → IR lowering pass.
"""

from __future__ import annotations

from compiler.ast.nodes import Comparison, LogicalExpression, Policy, Condition
from compiler.ir.ir import IRComparison, IRLogical, IRPolicy, IRCondition


FIELD_MAP = {
    "source.ip": "SRC_IP",
    "destination.ip": "DST_IP",
    "source.port": "SRC_PORT",
    "destination.port": "DST_PORT",
    "protocol": "PROTOCOL",
}

OPERATOR_MAP = {
    "==": "EQ",
    "!=": "NE",
}


class IRLoweringError(Exception):
    """Raised when an AST cannot be lowered into Policy IR."""


def lower_condition(condition: Condition) -> IRCondition:
    if isinstance(condition, Comparison):
        if condition.field not in FIELD_MAP:
            raise IRLoweringError(
                f"Unsupported AST field: {condition.field}"
            )

        if condition.operator not in OPERATOR_MAP:
            raise IRLoweringError(
                f"Unsupported AST operator: {condition.operator}"
            )

        return IRComparison(
            field=FIELD_MAP[condition.field],
            operator=OPERATOR_MAP[condition.operator],
            value=condition.value,
        )

    if isinstance(condition, LogicalExpression):
        if condition.operator not in {"AND", "OR"}:
            raise IRLoweringError(
                f"Unsupported logical operator: {condition.operator}"
            )

        return IRLogical(
            operator=condition.operator,
            left=lower_condition(condition.left),
            right=lower_condition(condition.right),
        )

    raise IRLoweringError(
        f"Unsupported AST node: {type(condition).__name__}"
    )


def lower_policy(policy: Policy) -> IRPolicy:
    return IRPolicy(
        action=policy.action,
        direction=policy.direction,
        condition=lower_condition(policy.condition),
    )