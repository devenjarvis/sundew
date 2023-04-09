import main

from sundew import test

test(main.say_after)(
    kwargs={"delay": 0.1, "what": "hello"},
    returns="hello",
)
