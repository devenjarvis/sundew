import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import MagicMock

from sundew import test, test_writer, utils
from tests import fixtures

test(test_writer.mock_function_dependencies)(
    setup=[fixtures.extend_config_with_dependent_functions],
    kwargs={"fn": fixtures.callee_func, "stack": ExitStack()},
    returns={"dependent_func": utils.FunctionSpy(fixtures.dependent_func)},
)

test(test_writer.generate_naive_function_import)(
    kwargs={
        "mock_name": "mock_function_dependencies",
        "mock_test_functions": {fixtures.dependent_func_function_test},
    },
    returns=[("sundew.test_writer", "mock_function_dependencies")],
)

test(test_writer.generate_function_dependency_test_file)(
    kwargs={
        "fn": test_writer.generate_function_dependency_test_file,
        "mocks": {
            "generate_naive_function_import": utils.FunctionSpy(
                test_writer.generate_naive_function_import
            ),
            "build_test_strings": utils.FunctionSpy(test_writer.build_test_strings),
            "build_import_string": utils.FunctionSpy(test_writer.build_import_string),
            "write_tests_to_file": utils.FunctionSpy(test_writer.write_tests_to_file),
        },
    },
    returns=None,
)

# TODO: Fix multilin lambda side_effects
test(test_writer.write_tests_to_file)(
    kwargs={
        "file_path": Path("/example.py"),
        "generated_test_file_import_string": "from sundew import test\n",
        "generated_test_file": "test(example)()",
    },
    patches={
        "sundew.test_writer.Path.open": unittest.mock.mock_open(),
        "black.format_file_in_place": MagicMock(),
    },
    side_effects=[
        lambda _: _.patches["sundew.test_writer.Path.open"].mock_calls[0].args
        == ("w",),
        lambda _: _.patches["sundew.test_writer.Path.open"].mock_calls[2].args
        == ("from sundew import test\ntest(example)()"),
    ],
)

test(test_writer.check_returns_for_imports)(
    kwargs={"test_fn": fixtures.function_test_with_path_returns},
    returns=[["pathlib", "PosixPath"]],
)

test(test_writer.check_kwargs_for_imports)(
    kwargs={"test_fn": fixtures.function_test_with_function_kwargs},
    returns=[["tests.fixtures", "example_fn_2"]],
)
