import io

from examples.strings import strings
from sundew.test import test

test(strings.concatenate)(
    kwargs={"a": "123", "b": "456"},
    returns="123456",
)
test(strings.reverse)(
    kwargs={"a": "123"},
    returns="321",
)
test(strings.make_silly)(
    kwargs={"a": "123", "b": "456"},
    returns="321654",
)
test(strings.print_string)(
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
