from examples.mathematics import mathematics
from sundew.test import test


test(mathematics.product)(
    input={"a": 2, "b": 3},
    returns=6,
)
test(mathematics.product)(
    input={"a": 5, "b": 5},
    returns=25,
)

# Failing test
# test(mathematics.product)(
#     input={"a": 2, "b": 3},
#     returns=8,
# )

# Test error
test(mathematics.error)(input={"a": 2})

test(mathematics.divide)(input={"a": 10.0, "b": 2.0}, returns=5.0)

test(mathematics.divide)(input={"a": 10.0, "b": 0.0}, returns=ZeroDivisionError)


test(mathematics.negative)(
    input={"a": 2},
    returns=-2,
)
test(mathematics.negative)(
    input={"a": -5},
    returns=5,
)

test(mathematics.square)(
    input={"a": 5},
    returns=25,
)

test(mathematics.square_root)(
    input={"a": 25},
    returns=5,
)

test(mathematics.quadratic)(
    input={"a": 1, "b": -8, "c": 5},
    returns=(7.3166247903554, 0.6833752096446002),
)
