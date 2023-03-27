import ast

from sundew import side_effects, test

test(side_effects.ConvertSideEffect.visit)(
    kwargs={
        "self": side_effects.ConvertSideEffect(),
        "node": ast.parse("lambda a: a.b == a.c"),
    },
    returns=ast.parse(
        """assert a.b == a.c, f"Side-effect 'a.b == a.c' failed because: a.b == {a.b}, and {a.b} != {a.c}" """  # noqa: E501
    ),
)

test(side_effects.SideEffectGetter.visit_Lambda)(
    kwargs={
        "self": side_effects.SideEffectGetter(),
        "node": ast.parse("lambda _: _.b == _.c").body[0].value,  # type: ignore[attr-defined]
    },
    side_effects=[lambda _: _.self.lambda_sources == {"lambda _: _.b == _.c"}],
)

test(side_effects.SideEffectGetter.get)(
    kwargs={
        "self": side_effects.SideEffectGetter(),
        "code_string": "lambda _: _.b == _.c",
    },
    returns={"lambda _: _.b == _.c"},
)

test(side_effects.get_source)(
    kwargs={"funcs": [lambda _: _.a == _.b]},
    returns={"lambda _: _.a == _.b"},
)(
    kwargs={
        "funcs": [
            lambda _: _.a == _.b,
            lambda _: (_.c - _.d) != _.e,
        ],
    },
    returns={"lambda _: _.a == _.b", "lambda _: _.c - _.d != _.e"},
)(
    kwargs={"funcs": [lambda _: _.a == _.b, lambda _: _.a == _.b]},
    returns={"lambda _: _.a == _.b"},
)
