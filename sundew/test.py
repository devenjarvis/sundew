from functools import wraps
import sys
from typing import Any, Callable
import inspect
import importlib
from sundew.config import config
from sundew.types import FunctionTest
from contextlib import ExitStack
from unittest.mock import patch
from rich import print
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    MofNCompleteColumn,
    TimeElapsedColumn,
)
import os
from time import sleep


class TestError(Exception):
    def __init__(self, message):
        self.message = message


def test(fn):
    def decorator(
        input: dict | None,
        returns: Any | None = None,
        patches: dict = dict(),
        side_effects: list[Callable] = [],
    ):
        func_name = fn.__code__.co_name
        # Don't check this wrapper function
        if func_name != "sundew_test_wrapper":
            # Get package_name, module_name, and module
            if module := inspect.getmodule(fn):
                module_name = module.__name__
                imported_module = importlib.import_module(module_name)
                config.modules.add(imported_module.__name__)

                # Loop through sub functions called
                for sub_func_name in fn.__code__.co_names:
                    # We only care about functions in the modules being tested
                    if hasattr(imported_module, sub_func_name):
                        # Verify that the funcion is native to the modules being tested
                        parent_module = getattr(
                            imported_module, sub_func_name
                        ).__module__
                        # Only connect functions within the module
                        if parent_module in config.modules:
                            config.function_graph.add_connections(
                                [(func_name, sub_func_name)]
                            )
            else:
                ...

        @wraps(fn)
        def sundew_test_wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        config.tests.append(
            FunctionTest(
                location=f"{os.path.relpath(inspect.stack()[1][1])}:{inspect.stack()[1][2]}",
                function=sundew_test_wrapper,
                input=input,
                returns=returns,
                patches=patches,
                side_effects=side_effects,
            )
        )
        return sundew_test_wrapper

    return decorator


def lambda_internals(func):
    return inspect.getsource(func).split(":")[1].strip()[:-1]


def run():
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
    ) as progress:
        for test in progress.track(config.tests, description="Running tests..."):
            with ExitStack() as stack:
                try:
                    # programmatically apply any patches defined
                    if test.patches:
                        for target, new in test.patches.items():
                            stack.enter_context(patch(target, new))
                    # Run the test function once for evaluation
                    try:
                        actual_return = test.function(**test.input)
                    except Exception as e:
                        # If we get an exception, check to see if it was expected
                        if test.returns:
                            assert isinstance(e, test.returns)
                        else:
                            raise e
                    else:
                        # If we didn't get an exception then check the output normally
                        if test.returns:
                            assert actual_return == test.returns, (
                                f"Input {test.input} returned {actual_return} "
                                + "which does not match the expected return of "
                                + f"{test.returns}"
                            )
                    finally:
                        # Regardless of if we got a planned exception or not,
                        # check if we have defined side effects
                        if test.side_effects:
                            for side_effect in test.side_effects:
                                if test.patches:
                                    assert side_effect(
                                        patches=test.patches, **test.input
                                    ), f"({lambda_internals}) is not true."
                                else:
                                    assert side_effect(**test.input)
                except AssertionError as e:
                    # Give progress bar enough time to update
                    sleep(0.15)
                    # Stop the progress bar
                    progress.stop()
                    # Log details of the failure
                    print(f"\n[bold red1]FAILURE[/] {test.location} - {str(e)}")
                    sys.exit(1)
                except Exception as e:
                    # Give progress bar enough time to update
                    sleep(0.15)
                    # Stop the progress bar
                    progress.stop()
                    # Log details of the error
                    print(f"\n[bold orange1]ERROR[/] {test.location} - {str(e)}")
                    sys.exit(1)
