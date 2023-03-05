import io

from examples import side_effects_example
from sundew.test import test

test(side_effects_example.concatenate)(
    kwargs={"a": "123", "b": "456"},
    returns="123456",
)
test(side_effects_example.reverse)(
    kwargs={"a": "123"},
    returns="321",
)
test(side_effects_example.make_silly)(
    kwargs={"a": "123", "b": "456"},
    returns="321654",
)
test(side_effects_example.print_string)(
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
