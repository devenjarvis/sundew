from examples.strings import strings
import io
from shore.test import test

test(strings.concatenate)(
    input={"a": "123", "b": "456"},
    output="123456",
)
test(strings.reverse)(
    input={"a": "123"},
    output="321",
)
test(strings.make_silly)(
    input={"a": "123", "b": "456"},
    output="321654",
)
test(strings.print_string)(
    input={"a": "123"},
    patched={"sys.stdout": io.StringIO()},
    side_effects=[
        lambda patched, **_: patched["sys.stdout"].getvalue(),
        lambda a, **_: a == "123",
    ],
)
test(strings.print_string)(
    input={"a": "456"},
    patched={"sys.stdout": io.StringIO()},
    side_effects=[
        lambda patched, **_: patched["sys.stdout"].getvalue() == "456\n",
        lambda a, **_: a == "456",
    ],
)
