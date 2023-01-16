from sundew.test import test
from sundew import side_effects
import ast

test(side_effects.ConvertSideEffect.visit)(
    input={
        "self": side_effects.ConvertSideEffect(),
        "node": ast.parse("lambda a: a.b == a.c"),
    },
    returns=ast.parse("assert a.b == a.c, f'left={a.b} right={a.c}'"),
)

test(side_effects.SideEffectGetter.visit_Lambda)(
    input={
        "self": side_effects.SideEffectGetter(),
        "node": ast.parse("lambda _: _.b == _.c").body[0].value,  # type: ignore
    },
    side_effects=[lambda _: _.self.lambda_sources == {"lambda _: _.b == _.c"}],
)

test(side_effects.SideEffectGetter.get)(
    input={
        "self": side_effects.SideEffectGetter(),
        "code_string": "lambda _: _.b == _.c",
    },
    returns={"lambda _: _.b == _.c"},
)

test(side_effects.get_source)(
    input={"funcs": [lambda _: _.a == _.b]},
    returns={"lambda _: _.a == _.b"},
)(
    input={
        "funcs": [
            lambda _: _.a == _.b,
            lambda _: (_.c - _.d) != _.e,
        ]
    },
    returns={"lambda _: _.a == _.b", "lambda _: _.c - _.d != _.e"},
)(
    input={"funcs": [lambda _: _.a == _.b, lambda _: _.a == _.b]},
    returns={"lambda _: _.a == _.b"},
)
