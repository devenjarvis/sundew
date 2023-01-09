from sundew.test import test
from sundew.side_effects import ConvertSideEffect
import ast

test(ConvertSideEffect().visit)(
    input={"node": ast.parse("lambda a: a.b == a.c")},
    returns=ast.parse("assert a.b == a.c, f'left={a.b} right={a.c}'"),
)
