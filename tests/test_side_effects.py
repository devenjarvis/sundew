from sundew.test import test, arg
from sundew import side_effects
import ast

test(side_effects.ConvertSideEffect().visit)(
    input={"node": ast.parse("lambda a: a.b == a.c")},
    returns=ast.parse("assert a.b == a.c, f'left={a.b} right={a.c}'"),
)

test(side_effects.get_source)(
    input={"funcs": [lambda: arg["a"] == arg["b"]]},
    returns={"lambda: arg['a'] == arg['b']"},
)

test(side_effects.get_source)(
    input={
        "funcs": [
            lambda: arg["a"] == arg["b"],
            lambda: (arg["c"] - arg["d"]) != arg["e"],
        ]
    },
    returns={"lambda: arg['a'] == arg['b']", "lambda: arg['c'] - arg['d'] != arg['e']"},
)

test(side_effects.get_source)(
    input={"funcs": [lambda: arg["a"] == arg["b"], lambda: arg["a"] == arg["b"]]},
    returns={"lambda: arg['a'] == arg['b']"},
)
