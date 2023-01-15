from sundew import test as sundew_test
from sundew.test import test

import tests.fixtures as fixtures

# test(sundew_test.update_function_graph)(
#     inputs={"fn": fixtures.example_fn},
#     side_effects=[
#         lambda: config.function_graph # Not isolated, stopping here...
#     ]
# )

# test(sundew_test.get_test_function)(
#     inputs={"fn": fixtures.example_fn},
#     returns= # Haven't solved function equivalence, stopping here...
# )

# test(sundew_test.test)(
#     # Not sure I can test this within sundew, stopping here...
# )

# test(sundew_test.apply_patches)(
#     # Not sure how to test a context manager, stopping here...
# )

test(sundew_test.copy_function_inputs)(
    input={"test": fixtures.passing_function_test},
    returns={"a": 1, "b": "2"},
)(
    input={"test": fixtures.passing_function_test_with_defaults},
    returns={"a": 1, "b": "hello"},
)

test(sundew_test.run_function)(
    input={
        "test": fixtures.passing_function_test,
        "isolated_input": {"a": 1, "b": "2"},
    },
    returns="21",
)

# can't test sundew.test.run due to the fact that we are using it.
# Not sure if this is surmountable, or if I just need to break it up for better coverage
