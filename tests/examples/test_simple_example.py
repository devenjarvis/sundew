from examples.examples import simple_example
from sundew.test import test

test(simple_example.quadratic)(
    kwargs={"a": 1, "b": -8, "c": 5},
    returns=(7.3166247903554, 0.6833752096446002),
)