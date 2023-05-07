from contextlib import AsyncExitStack

from sundew import test
from sundew import test_runner as sundew_test
from tests import fixtures

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
        "stack": AsyncExitStack(),
    },
    returns="21",
)


test(sundew_test.select_functions_to_test)(
    kwargs={"function_name": ""},
    setup=[fixtures.extend_config_with_simple_functions],
    side_effects={
        lambda _: {"tests.fixtures.example_fn_1", "tests.fixtures.example_fn_2"}
        <= set(_.returns)
    },
)(
    kwargs={"function_name": "tests.fixtures.example_fn_1"},
    setup=[fixtures.extend_config_with_simple_functions],
    returns=["tests.fixtures.example_fn_1"],
)

test(sundew_test.sort_tests)(
    setup=[fixtures.extend_config_with_dependent_functions],
    kwargs={
        "selected_functions": [
            "tests.fixtures.dependent_func",
            "tests.fixtures.callee_func",
        ]
    },
    returns=[
        fixtures.dependent_func_function_test,
        fixtures.callee_func_function_test,
    ],
)(
    # Should get same output, regardless of input order
    setup=[fixtures.extend_config_with_dependent_functions],
    kwargs={
        "selected_functions": [
            "tests.fixtures.callee_func",
            "tests.fixtures.dependent_func",
        ]
    },
    returns=[
        fixtures.dependent_func_function_test,
        fixtures.callee_func_function_test,
    ],
)(
    # Make sure sorting works with only 1 element
    setup=[fixtures.extend_config_with_dependent_functions],
    kwargs={"selected_functions": ["tests.fixtures.dependent_func"]},
    returns=[fixtures.dependent_func_function_test],
)(
    # Make sure sorting works with zero elements
    setup=[fixtures.extend_config_with_dependent_functions],
    kwargs={"selected_functions": []},
    returns=[],
)

# test(sundew_test.detect_missing_tests)(

# can't test sundew.test.run due to the fact that we are using it.
# Not sure if this is surmountable, or if I just need to break it up for better coverage
