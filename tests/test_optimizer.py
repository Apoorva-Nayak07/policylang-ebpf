from compiler.ir.ir import IRComparison, IRLogical, IRPolicy
from compiler.optimizer.optimizer import optimize_policy


def test_duplicate_and_condition_is_removed():
    condition = IRLogical(
        operator="AND",
        left=IRComparison(
            field="SRC_IP",
            operator="EQ",
            value="10.0.0.5",
        ),
        right=IRComparison(
            field="SRC_IP",
            operator="EQ",
            value="10.0.0.5",
        ),
    )

    policy = IRPolicy(
        action="ALLOW",
        direction="INGRESS",
        condition=condition,
    )

    optimized = optimize_policy(policy)

    assert optimized.condition == IRComparison(
        field="SRC_IP",
        operator="EQ",
        value="10.0.0.5",
    )


def test_non_duplicate_conditions_are_preserved():
    condition = IRLogical(
        operator="AND",
        left=IRComparison(
            field="SRC_IP",
            operator="EQ",
            value="10.0.0.5",
        ),
        right=IRComparison(
            field="DST_PORT",
            operator="EQ",
            value=443,
        ),
    )

    policy = IRPolicy(
        action="ALLOW",
        direction="INGRESS",
        condition=condition,
    )

    optimized = optimize_policy(policy)

    assert optimized.condition == condition


def test_or_conditions_are_preserved():
    condition = IRLogical(
        operator="OR",
        left=IRComparison(
            field="SRC_IP",
            operator="EQ",
            value="10.0.0.5",
        ),
        right=IRComparison(
            field="SRC_IP",
            operator="EQ",
            value="10.0.0.6",
        ),
    )

    policy = IRPolicy(
        action="DENY",
        direction="INGRESS",
        condition=condition,
    )

    optimized = optimize_policy(policy)

    assert optimized.condition == condition