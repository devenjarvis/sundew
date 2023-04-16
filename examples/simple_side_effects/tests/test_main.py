import io

import main

from sundew import test

test(main.concatenate)(
    kwargs={"a": "123", "b": "456"},
    returns="123456",
)
test(main.reverse)(
    kwargs={"a": "123"},
    returns="321",
)
test(main.make_silly)(
    kwargs={"a": "123", "b": "456"},
    returns="321654",
)
test(main.print_string)(
    kwargs={"a": "123"},
    patches={"sys.stdout": io.StringIO()},
    side_effects=[
        lambda _: _.patches["sys.stdout"].getvalue() == "123\n",
        lambda _: _.a == "123",
    ],
)(
    kwargs={"a": "456"},
    patches={"sys.stdout": io.StringIO()},
    side_effects=[
        lambda _: _.patches["sys.stdout"].getvalue() == "456\n",
        lambda _: _.a == "456",
    ],
)

test(main.print_hello)(
    kwargs={"name": "Dave"},
    patches={"sys.stdout": io.StringIO()},
    side_effects=[
        lambda _: _.patches["sys.stdout"].getvalue() == "Hello, Dave\n",
    ],
)
