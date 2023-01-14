from examples.async_example import async_example
from sundew.test import test

test(async_example.say_after)(
    input={"delay": 0.1, "what": "hello"},
    returns="hello",
)
