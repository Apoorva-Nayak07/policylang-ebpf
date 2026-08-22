from compiler.ast.nodes import Comparison, LogicalExpression, Policy
from compiler.ir.ir import IRComparison, IRLogical, IRPolicy
from compiler.ir.lower import lower_policy


def test_lower_basic_policy():
    policy = Policy(
        action="ALLOW",
        direction="INGRESS",
        condition=LogicalExpression(
            operator="AND",
            left=Comparison(
                field="source.ip",
                operator="==",
                value="10.0.0.5",
            ),
            right=Comparison(
                field="destination.port",
                operator="==",
                value=443,
            ),
        ),
    )

    ir = lower_policy(policy)

    assert isinstance(ir, IRPolicy)
    assert ir.action == "ALLOW"
    assert ir.direction == "INGRESS"

    assert isinstance(ir.condition, IRLogical)
    assert ir.condition.operator == "AND"

    assert ir.condition.left == IRComparison(
        field="SRC_IP",
        operator="EQ",
        value="10.0.0.5",
    )

    assert ir.condition.right == IRComparison(
        field="DST_PORT",
        operator="EQ",
        value=443,
    )


def test_lower_not_equal():
    policy = Policy(
        action="DENY",
        direction="INGRESS",
        condition=Comparison(
            field="source.ip",
            operator="!=",
            value="192.168.1.10",
        ),
    )

    ir = lower_policy(policy)

    assert ir.action == "DENY"
    assert ir.direction == "INGRESS"

    assert ir.condition == IRComparison(
        field="SRC_IP",
        operator="NE",
        value="192.168.1.10",
    )


def test_lower_protocol():
    policy = Policy(
        action="ALLOW",
        direction="INGRESS",
        condition=Comparison(
            field="protocol",
            operator="==",
            value="tcp",
        ),
    )

    ir = lower_policy(policy)

    assert ir.condition == IRComparison(
        field="PROTOCOL",
        operator="EQ",
        value="tcp",
    )