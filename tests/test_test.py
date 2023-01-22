import io
from sundew import test as sundew_test
from sundew.config import config
from sundew.test import test
from tests import fixtures
from rich.progress import Progress

# test(sundew_test.update_test_graph)(
#   Not isolated, stopping here...

# test(sundew_test.get_test_function)(
#     returns= Haven't solved function equivalence, stopping here...

# test(sundew_test.test)(
#     # Not sure I can test this within sundew, stopping here...

# test(sundew_test.apply_patches)(
#     # Not sure how to test a context manager, stopping here...

test(sundew_test.copy_function_inputs)(
    kwargs={"test": fixtures.passing_function_test},
    returns={"a": 1, "b": "2"},
)(
    kwargs={"test": fixtures.passing_function_test_with_defaults},
    returns={"a": 1, "b": "hello"},
)

test(sundew_test.run_function)(
    kwargs={
        "test": fixtures.passing_function_test,
        "isolated_input": {"a": 1, "b": "2"},
    },
    returns="21",
)

test(sundew_test.select_tests)(
    kwargs={"function_name": "", "progress": Progress()},
    patches={
        "sundew.config.config.test_graph": fixtures.setup_simple_test_graph(),
    },
    returns=["example_fn_1", "example_fn_2"],
)
# (
#     kwargs={"function_name": "example_fn_1", "progress": Progress()},
#     patches={
#         "sundew.config.config.test_graph": fixtures.setup_simple_test_graph(),
#     },
#     returns=["example_fn_1"],
# )

# can't test sundew.test.run due to the fact that we are using it.
# Not sure if this is surmountable, or if I just need to break it up for better coverage
