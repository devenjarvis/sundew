import io

from examples.examples import simple_example
from sundew.test import test

test(simple_example.quadratic)(
    kwargs={"a": 1, "b": -8, "c": 5},
    returns=(7.3166247903554, 0.6833752096446002),
)

test(simple_example.wait_2_sec)(
    patches={"sys.stdout": io.StringIO()},
    returns=4,
)
test(simple_example.wait_2_sec)(returns=4)

test(simple_example.wait_2_sec)(returns=4)

test(simple_example.wait_2_sec)(returns=4)

test(simple_example.wait_2_sec)(returns=4)

test(simple_example.simple_sleep)(
    cache=True,
    kwargs={"secs": 2},
    returns=None,
)
