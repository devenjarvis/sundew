from main import concatenate, reverse

from sundew import test

test(concatenate)(
    cache=True,
    kwargs={"a": "456", "b": "123"},
    returns="456123",
)
test(reverse)(
    cache=True,
    kwargs={"a": "456123"},
    returns="321654",
)
