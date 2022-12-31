from examples.strings import strings
import io
from sundew.test import test

test(strings.concatenate)(
    input={"a": "123", "b": "456"},
    returns="123456",
)
test(strings.reverse)(
    input={"a": "123"},
    returns="321",
)
test(strings.make_silly)(
    input={"a": "123", "b": "456"},
    returns="321654",
)
test(strings.print_string)(
    input={"a": "123"},
    patches={"sys.stdout": io.StringIO()},
    side_effects=[
        lambda patches, **_: patches["sys.stdout"].getvalue(),
        lambda a, **_: a == "123",
    ],
)
test(strings.print_string)(
    input={"a": "456"},
    patches={"sys.stdout": io.StringIO()},
    side_effects=[
        lambda patches, **_: patches["sys.stdout"].getvalue() == "456\n",
        lambda a, **_: a == "456",
    ],
)
