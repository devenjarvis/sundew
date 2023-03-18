import ast
import inspect
from collections.abc import Callable
from typing import Any


def generate_inverse_operation_str(  # noqa: C901, PLR0911
    operation: ast.cmpop,
) -> str:
    if isinstance(operation, ast.Eq):
        return "!="
    if isinstance(operation, ast.NotEq):
        return "=="

    if isinstance(operation, ast.Lt):
        return ">="
    if isinstance(operation, ast.GtE):
        return "<"

    if isinstance(operation, ast.LtE):
        return ">"
    if isinstance(operation, ast.Gt):
        return "<="

    if isinstance(operation, ast.Is):
        return "is not"
    if isinstance(operation, ast.IsNot):
        return "is"

    if isinstance(operation, ast.In):
        return "is not in"
    if isinstance(operation, ast.NotIn):
        return "is in"
    return "unknown operator"


# Generate assert statement from a Compare node
def generate_compare_assert(node: ast.Compare) -> ast.Assert:
    return ast.Assert(
        test=node,
        msg=ast.JoinedStr(
            values=[
                ast.Constant(
                    value=f"Side-effect '{ast.unparse(node)}' failed because: "
                ),
                ast.Constant(value=f"{ast.unparse(node.left)} == "),
                ast.FormattedValue(value=node.left, conversion=-1),
                ast.Constant(value=", and "),
                ast.FormattedValue(value=node.left, conversion=-1),
                ast.Constant(value=f" {generate_inverse_operation_str(node.ops[0])} "),
                ast.FormattedValue(value=node.comparators[0], conversion=-1),
            ]
        ),
    )


# Generate a general assert statement, for expressions we don't explicit handle yet
def generate_general_assert(node: ast.expr) -> ast.Assert:
    return ast.Assert(
        test=node,
        msg=ast.JoinedStr(
            values=[
                ast.Constant(value=ast.unparse(node)),
                ast.Constant(value=" is False."),
            ],
        ),
    )


class ConvertSideEffect(ast.NodeTransformer):
    def visit_Lambda(self, node: ast.Lambda) -> ast.Assert:  # noqa: N802
        if isinstance(node.body, ast.Compare):
            return generate_compare_assert(node.body)
        return generate_general_assert(node.body)


class SideEffectGetter(ast.NodeTransformer):
    def __init__(self) -> None:
        super().__init__()
        self.lambda_sources: set[str] = set()

    def visit_Lambda(self, node: ast.Lambda) -> None:  # noqa: N802
        self.lambda_sources.add(ast.unparse(node).strip())

    def get(self, code_string: str) -> set[str]:
        tree = ast.parse(code_string)
        self.visit(tree)
        return self.lambda_sources


def get_source(funcs: list[Callable[[Any], bool]]) -> set[str]:
    side_effects = SideEffectGetter()
    for func in funcs:
        code_string = inspect.getsource(func).strip()
        side_effects.get(code_string)

    return side_effects.lambda_sources
