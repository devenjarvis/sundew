import io

from examples.examples import simple_example
from sundew import test

test(simple_example.quadratic)(
    kwargs={"a": 1, "b": -8, "c": 5},
    returns=(7.3166247903554, 0.6833752096446002),
)

test(simple_example.wait_2_sec)(
    patches={"sys.stdout": io.StringIO()},
    returns=None,
)
test(simple_example.wait_2_sec)()

test(simple_example.simple_sleep)(
    cache=True,
    kwargs={"secs": 2},
    returns=None,
)


test(simple_example.quadratic)(
    kwargs={"a": 1, "b": -8, "c": 5},
    returns=(7.3166247903554, 0.6833752096446002),
    side_effects=[lambda _: _.a < 5],  # noqa: PLR2004
)
