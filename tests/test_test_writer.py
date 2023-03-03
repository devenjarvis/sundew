from contextlib import ExitStack

from sundew import test_writer
from sundew.test import test
from tests import fixtures

test(test_writer.mock_function_dependencies)(
    patches={
        "sundew.config.config.test_graph": fixtures.setup_test_graph_with_dependency(),
    },
    kwargs={"fn": fixtures.callee_func, "stack": ExitStack()},
    returns={
        "dependent_func": test_writer.DependentFunctionSpy(fixtures.dependent_func)
    },
)
