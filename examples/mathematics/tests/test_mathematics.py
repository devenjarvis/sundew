from examples.mathematics import mathematics
from sundew.test import test

test(mathematics.product)(
    kwargs={"a": 2, "b": 3},
    returns=6,
)
test(mathematics.product)(
    kwargs={"a": 5, "b": 5},
    returns=25,
)


test(mathematics.divide)(kwargs={"a": 10.0, "b": 2.0}, returns=5.0)

test(mathematics.divide)(kwargs={"a": 10.0, "b": 0.0}, returns=ZeroDivisionError)


test(mathematics.negative)(
    kwargs={"a": 2},
    returns=-2,
)
test(mathematics.negative)(
    kwargs={"a": -5},
    returns=5,
)

test(mathematics.square)(
    kwargs={"a": 5},
    returns=25,
)

test(mathematics.square_root)(
    kwargs={"a": 25},
    returns=5,
)

test(mathematics.quadratic)(
    kwargs={"a": 1, "b": -8, "c": 5},
    returns=(7.3166247903554, 0.6833752096446002),
)
