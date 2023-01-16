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
        lambda _: _.patches["sys.stdout"].getvalue() == "123\n",
        lambda _: _.a == "123",
    ],
)(
    input={"a": "456"},
    patches={"sys.stdout": io.StringIO()},
    side_effects=[
        lambda _: _.patches["sys.stdout"].getvalue() == "456\n",
        lambda _: _.a == "456",
    ],
)

# Failing side-effect test
# test(strings.print_string)(
#     input={"a": "789"},
#     patches={"sys.stdout": io.StringIO()},
#     side_effects=[
#         lambda _: _.patched["sys.stdout"].getvalue() == "7ate9\n",
#     ],
# )
