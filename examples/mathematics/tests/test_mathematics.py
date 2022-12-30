from examples.mathematics import mathematics
from shore.test import test


test(mathematics.product)(
    input={"a": 2, "b": 3},
    output=6,
)
test(mathematics.product)(
    input={"a": 5, "b": 5},
    output=25,
)

test(mathematics.negative)(
    input={"a": 2},
    output=-2,
)
test(mathematics.negative)(
    input={"a": -5},
    output=5,
)

test(mathematics.square)(
    input={"a": 5},
    output=25,
)

test(mathematics.square_root)(
    input={"a": 25},
    output=5,
)

test(mathematics.quadratic)(
    input={"a": 1, "b": -8, "c": 5},
    output=(7.3166247903554, 0.6833752096446002),
)
