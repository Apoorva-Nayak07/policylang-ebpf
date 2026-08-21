from compiler.ast.nodes import Comparison, LogicalExpression, Policy


def build_test_policy():
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

    condition = LogicalExpression(
        operator="AND",
        left=left,
        right=right,
    )

    return Policy(
        action="ALLOW",
        direction="INGRESS",
        condition=condition,
    )


if __name__ == "__main__":
    policy = build_test_policy()

    print("Policy AST")
    print("----------")
    print(policy)