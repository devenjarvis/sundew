from functools import wraps
from typing import Any, Callable
import inspect
import importlib
from shore.config import config
from shore.types import FunctionTest
from contextlib import ExitStack
from unittest.mock import patch


class TestError(Exception):
    def __init__(self, message):
        self.message = message


def test(fn):
    def decorator(
        input: dict | None,
        output: Any | None = None,
        patched: dict = dict(),
        side_effects: list[Callable] = [],
    ):
        func_name = fn.__code__.co_name
        # Don't check this wrapper function
        if func_name != "shore_test_wrapper":
            # Get package_name, module_name, and module
            module_name = inspect.getmodule(fn).__name__
            module = importlib.import_module(module_name)
            config.modules.add(module.__name__)

            # Loop through sub functions called
            for sub_func_name in fn.__code__.co_names:
                # We only care about functions in the modules we are testing
                if hasattr(module, sub_func_name):
                    # Verify that the funcion is native to the modules we are testing
                    parent_module = getattr(module, sub_func_name).__module__
                    # Only connect functions within the module
                    if parent_module in config.modules:
                        config.function_graph.add_connections(
                            [(func_name, sub_func_name)]
                        )

        @wraps(fn)
        def shore_test_wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        config.tests.append(
            FunctionTest(
                function=shore_test_wrapper,
                input=input,
                output=output,
                patched=patched,
                side_effects=side_effects,
            )
        )
        return shore_test_wrapper

    return decorator


def run():
    for test in config.tests:
        with ExitStack() as stack:
            # programmatically apply any patches defined
            if test.patched:
                for target, new in test.patched.items():
                    stack.enter_context(patch(target, new))
            # Run the test function once for evaluation
            actual_output = test.function(**test.input)

        # If we have defined side effects
        if test.side_effects:
            for side_effect in test.side_effects:
                if test.patched:
                    assert side_effect(patched=test.patched, **test.input)
                else:
                    assert side_effect(**test.input)
        # If we have defined output
        if test.output:
            assert actual_output == test.output
        print(". PASS")
