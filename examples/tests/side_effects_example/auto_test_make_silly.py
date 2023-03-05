from examples.side_effects_example import concatenate, reverse
from sundew.test import test

test(concatenate)(
    kwargs={"a": "456", "b": "123"},
    returns="456123",
)
test(reverse)(
    kwargs={"a": "456123"},
    returns="321654",
)
