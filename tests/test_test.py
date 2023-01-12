from sundew import test as sundew_test
from sundew.test import test, arg

# from sundew.config import config
# import tests.fixtures as fixtures

# TODO: Figure out how to compare function outputs
# TODO: Figure out how to isolate globals for side_effects
# test(sundew_test.test)(
#     input={"fn": fixtures.example_fn},
#     returns=fixtures.example_fn,
#     side_effects=[
#         lambda l: len(config.tests) == 1,
#     ],
# )

test(sundew_test.build_side_effects)(
    input={"funcs": [lambda: arg["a"] == arg["b"]]},
    returns={"lambda: arg['a'] == arg['b']"},
)

test(sundew_test.build_side_effects)(
    input={
        "funcs": [
            lambda: arg["a"] == arg["b"],
            lambda: (arg["c"] - arg["d"]) != arg["e"],
        ]
    },
    returns={"lambda: arg['a'] == arg['b']", "lambda: arg['c'] - arg['d'] != arg['e']"},
)

test(sundew_test.build_side_effects)(
    input={"funcs": [lambda: arg["a"] == arg["b"], lambda: arg["a"] == arg["b"]]},
    returns={"lambda: arg['a'] == arg['b']"},
)

# can't test sundew.test.run due to the fact that we are using it.
# Not sure if this is surmountable, or if I just need to break it up for better coverage
