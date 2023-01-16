import ast
import inspect
from typing import Any, Callable


# Generate assert statement from a Compare node
def generate_compare_assert(node: ast.Compare):
    return ast.Assert(
        test=node,
        msg=ast.JoinedStr(
            values=[
                ast.Constant(value="left="),
                ast.FormattedValue(value=node.left, conversion=-1),
                ast.Constant(value=" right="),
                ast.FormattedValue(value=node.comparators[0], conversion=-1),
            ]
        ),
    )


# Generate a general assert statement, for expressions we don't explicit handle yet
def generate_general_assert(node: ast.expr):
    return ast.Assert(
        test=node,
        msg=ast.JoinedStr(
            values=[
                ast.Constant(value=ast.unparse(node)),
                ast.Constant(value=" is False."),
            ]
        ),
    )


class ConvertSideEffect(ast.NodeTransformer):
    def visit_Lambda(self, node):
        if isinstance(node.body, ast.Compare):
            return generate_compare_assert(node.body)
        else:
            return generate_general_assert(node.body)


class SideEffectGetter(ast.NodeTransformer):
    def __init__(self) -> None:
        super().__init__()
        self.lambda_sources: set[str] = set()

    def visit_Lambda(self, node: ast.Lambda) -> None:
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
