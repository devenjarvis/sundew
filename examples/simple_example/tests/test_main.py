import io

import main

from sundew import test

test(main.quadratic)(
    kwargs={"a": 1, "b": -8, "c": 5},
    returns=(7.3166247903554, 0.6833752096446002),
)

test(main.wait_2_sec)(
    patches={"sys.stdout": io.StringIO()},
    returns=None,
)
test(main.wait_2_sec)()

test(main.simple_sleep)(
    cache=True,
    kwargs={"secs": 2},
    returns=None,
)


test(main.quadratic)(
    kwargs={"a": 1, "b": -8, "c": 5},
    returns=(7.3166247903554, 0.6833752096446002),
    side_effects=[lambda _: _.a < 5],  # noqa: PLR2004
)
