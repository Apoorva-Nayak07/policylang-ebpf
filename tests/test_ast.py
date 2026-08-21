from compiler.ast.nodes import Comparison, LogicalExpression, Policy


def test_comparison_node():
    node = Comparison(
        field="source.ip",
        operator="==",
        value="10.0.0.5",
    )

    assert node.field == "source.ip"
    assert node.operator == "=="
    assert node.value == "10.0.0.5"


def test_logical_expression_node():
    left = Comparison(
        field="source.ip",
        operator="==",
        value="10.0.0.5",
    )

    right = Comparison(
        field="destination.port",
        operator="==",
        value=443,
    )

    node = LogicalExpression(
        operator="AND",
        left=left,
        right=right,
    )

    assert node.operator == "AND"
    assert node.left == left
    assert node.right == right


def test_policy_node():
    condition = Comparison(
        field="source.ip",
        operator="==",
        value="10.0.0.5",
    )

    policy = Policy(
        action="ALLOW",
        direction="INGRESS",
        condition=condition,
    )

    assert policy.action == "ALLOW"
    assert policy.direction == "INGRESS"
    assert policy.condition == condition
