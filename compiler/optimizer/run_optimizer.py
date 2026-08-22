from compiler.ast.nodes import Comparison, LogicalExpression, Policy
from compiler.ir.lower import lower_policy
from compiler.optimizer.optimizer import optimize_policy


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
            field="source.ip",
            operator="==",
            value="10.0.0.5",
        ),
    ),
)


ir = lower_policy(policy)
optimized = optimize_policy(ir)

print("Original IR")
print("-----------")
print(ir)

print("\nOptimized IR")
print("------------")
print(optimized)