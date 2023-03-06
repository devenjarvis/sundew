from examples.examples.simple_example import (
    divide,
    negative,
    product,
    square,
    square_root,
)
from sundew.test import test

test(divide)(
    kwargs={"a": 1.3667504192892004, "b": 2},
    returns=0.6833752096446002,
)
test(divide)(
    kwargs={"a": 14.6332495807108, "b": 2},
    returns=7.3166247903554,
)
test(negative)(
    kwargs={"a": -8},
    returns=8,
)
test(product)(
    kwargs={"a": -8, "b": -8},
    returns=64,
)
test(product)(
    kwargs={"a": 2, "b": 1},
    returns=2,
)
test(product)(
    kwargs={"a": 1, "b": 5},
    returns=5,
)
test(product)(
    kwargs={"a": 4, "b": 5},
    returns=20,
)
test(square)(
    kwargs={"a": -8},
    returns=64,
)
test(square_root)(
    kwargs={"a": 44},
    returns=6.6332495807108,
)
