from examples.examples import async_example
from sundew import test

test(async_example.say_after)(
    kwargs={"delay": 0.1, "what": "hello"},
    returns="hello",
)
