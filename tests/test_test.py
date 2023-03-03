from sundew import test as sundew_test
from sundew.test import test
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
    },
    returns="21",
)


test(sundew_test.select_functions_to_test)(
    kwargs={"function_name": ""},
    patches={
        "sundew.config.config.test_graph": fixtures.setup_simple_test_graph(),
    },
    returns=["example_fn_1", "example_fn_2"],
)(
    kwargs={"function_name": "example_fn_1"},
    patches={
        "sundew.config.config.test_graph": fixtures.setup_simple_test_graph(),
    },
    returns=["example_fn_1"],
)

test(sundew_test.sort_tests)(
    kwargs={"selected_functions": ["dependent_func", "callee_func"]},
    patches={
        "sundew.config.config.test_graph": fixtures.setup_test_graph_with_dependency(),
    },
    returns=[
        fixtures.dependent_func_function_test,
        fixtures.callee_func_function_test,
    ],
)(
    # Should get same output, regardless of input order
    kwargs={"selected_functions": ["callee_func", "dependent_func"]},
    patches={
        "sundew.config.config.test_graph": fixtures.setup_test_graph_with_dependency(),
    },
    returns=[
        fixtures.dependent_func_function_test,
        fixtures.callee_func_function_test,
    ],
)(
    # Make sure sorting works with only 1 element
    kwargs={"selected_functions": ["dependent_func"]},
    patches={
        "sundew.config.config.test_graph": fixtures.setup_test_graph_with_dependency(),
    },
    returns=[fixtures.dependent_func_function_test],
)(
    # Make sure sorting works with zero elements
    kwargs={"selected_functions": []},
    patches={
        "sundew.config.config.test_graph": fixtures.setup_test_graph_with_dependency(),
    },
    returns=[],
)

test(sundew_test.detect_missing_tests)(
    # Make sure sorting works with only 1 element
    kwargs={"selected_functions": ["callee_func"]},
    patches={
        "sundew.config.config.test_graph": fixtures.setup_test_graph_with_dependency(),
    },
    returns=["tests.fixtures.dependent_func"],
)

# can't test sundew.test.run due to the fact that we are using it.
# Not sure if this is surmountable, or if I just need to break it up for better coverage
