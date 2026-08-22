"""
PolicyLang IR Optimizer.

v0.1 optimization:
- Remove duplicate logical conditions.
- Preserve policy action and direction.
"""

from __future__ import annotations

from compiler.ir.ir import IRComparison, IRLogical, IRPolicy, IRCondition


def optimize_condition(condition: IRCondition) -> IRCondition:
    if isinstance(condition, IRComparison):
        return condition

    if isinstance(condition, IRLogical):
        left = optimize_condition(condition.left)
        right = optimize_condition(condition.right)

        # Duplicate condition:
        # A AND A -> A
        if condition.operator == "AND" and left == right:
            return left

        return IRLogical(
            operator=condition.operator,
            left=left,
            right=right,
        )

    return condition


def optimize_policy(policy: IRPolicy) -> IRPolicy:
    return IRPolicy(
        action=policy.action,
        direction=policy.direction,
        condition=optimize_condition(policy.condition),
    )