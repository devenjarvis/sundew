import ast
import copy
from functools import wraps
import sys
from typing import Any, Callable
import inspect
import importlib
from sundew.config import config
from sundew.types import FunctionTest
from sundew.side_effects import ConvertSideEffect
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


arg: dict[str, Any] = dict()
patched: dict[str, Any] = dict()


def test(fn):
    @wraps(fn)
    def decorator(
        input: dict = dict(),
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
                            getattr(imported_module, sub_func_name), "__module__", None
                        )
                        # Only connect functions within the module
                        if parent_module in config.modules:
                            config.function_graph.add_connections(
                                [(func_name, sub_func_name)]
                            )
            else:
                ...

        @wraps(fn)
        def sundew_test_wrapper(*args, **kwargs):
            # global_shadow = {
            #     k: v for k, v in globals().items() if not k.startswith("__")
            # }
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


def build_side_effects(funcs: list[Callable]) -> set[str]:
    class LambdaGetter(ast.NodeTransformer):
        def __init__(self):
            super().__init__()
            self.lambda_sources: set[str] = set()

        def visit_Lambda(self, node):
            self.lambda_sources.add(ast.unparse(node).strip())

        def get(self, code_string):
            tree = ast.parse(code_string)
            self.visit(tree)
            return self.lambda_sources

    side_effects = LambdaGetter()
    for func in funcs:
        code_string = inspect.getsource(func).strip()
        side_effects.get(code_string)

    return side_effects.lambda_sources


def run():
    with Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
    ) as progress:
        tests_ran = progress.add_task("Running tests...", total=len(config.tests))
        for test in config.tests:
            with ExitStack() as stack:
                try:
                    # programmatically apply any patches defined
                    if test.patches:
                        for target, new in test.patches.items():
                            stack.enter_context(patch(target, new))
                    # Run the test function once for evaluation
                    try:
                        isolated_input = copy.deepcopy(test.input)
                        actual_return = test.function(**isolated_input)
                    except Exception as e:
                        # If we get an exception, check to see if it was expected
                        if test.returns:
                            assert isinstance(e, test.returns)
                        else:
                            raise e
                    else:
                        # If we didn't get an exception then check the output normally
                        if test.returns:
                            if isinstance(actual_return, ast.Module):
                                assert (
                                    ast.unparse(actual_return).strip()
                                    == ast.unparse(test.returns).strip()
                                ), (
                                    f"Input {test.input} returned AST for "
                                    + f"{ast.unparse(actual_return).strip()} "
                                    + "which does not match the expected AST for "
                                    + f"{ast.unparse(test.returns).strip()}"
                                )
                            else:
                                assert actual_return == test.returns, (
                                    f"Input {test.input} returned {actual_return} "
                                    + "which does not match the expected return of "
                                    + f"{test.returns}"
                                )
                    finally:
                        # Regardless of if we got a planned exception or not,
                        # check if we have defined side effects
                        if test.side_effects:
                            side_effect_sources = build_side_effects(test.side_effects)
                            for side_effect_source in side_effect_sources:
                                side_effect_ast = ConvertSideEffect().visit(
                                    ast.parse(side_effect_source)
                                )
                                side_effect_code = ast.unparse(side_effect_ast)
                                # Replace variables used by side_effects
                                arg = isolated_input  # noqa: F841
                                patched = test.patches  # noqa: F841
                                exec(side_effect_code)
                except AssertionError as e:
                    # Stop the progress bar
                    progress.stop()
                    # Log details of the failure
                    print(f"\n[bold red1]FAILURE[/] {test.location} - {str(e)}")
                    sys.exit(1)
                except Exception as e:
                    # Stop the progress bar
                    progress.stop()
                    # Log details of the error
                    progress.console.print_exception(show_locals=True)
                    print(f"\n[bold orange1]ERROR[/] {test.location} - {str(e)}")
                    sys.exit(1)
                else:
                    progress.advance(tests_ran)
