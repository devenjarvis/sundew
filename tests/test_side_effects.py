from sundew.test import test
from sundew import side_effects
import ast

test(side_effects.ConvertSideEffect().visit)(
    input={"node": ast.parse("lambda a: a.b == a.c")},
    returns=ast.parse("assert a.b == a.c, f'left={a.b} right={a.c}'"),
)
