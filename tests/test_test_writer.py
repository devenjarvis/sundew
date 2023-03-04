from contextlib import ExitStack

from sundew import test_writer
from sundew.test import test
from tests import fixtures

test(test_writer.mock_function_dependencies)(
    setup={fixtures.extend_config_with_dependent_functions},
    kwargs={"fn": fixtures.callee_func, "stack": ExitStack()},
    returns={
        "dependent_func": test_writer.DependentFunctionSpy(fixtures.dependent_func)
    },
)

test(test_writer.generate_naive_function_import)(
    kwargs={"mock_name": "mock_function_dependencies"},
    returns=("sundew.test_writer", "mock_function_dependencies"),
)

test(test_writer.generate_function_dependency_test_file)(
    # setup={fixtures.extend_config_with_dependent_functions},
    kwargs={
        "fn": test_writer.generate_function_dependency_test_file,
        "mocks": {
            "generate_naive_function_import": test_writer.DependentFunctionSpy(
                test_writer.generate_naive_function_import
            ),
            "build_test_strings": test_writer.DependentFunctionSpy(
                test_writer.build_test_strings
            ),
            "build_import_string": test_writer.DependentFunctionSpy(
                test_writer.build_import_string
            ),
            "write_tests_to_file": test_writer.DependentFunctionSpy(
                test_writer.write_tests_to_file
            ),
        },
    },
    returns=None,
)
