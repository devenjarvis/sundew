from examples.mathematics.mathematics import product
from sundew.test import test

test(product)(
    kwargs={"a": -8, "b": -8},
    returns=64,
)
