from examples.strings.strings import concatenate, reverse
from sundew.test import test

test(reverse)(
    kwargs={"a": "456123"},
    returns="321654",
)
test(concatenate)(
    kwargs={"a": "456", "b": "123"},
    returns="456123",
)
