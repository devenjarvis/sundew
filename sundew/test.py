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
from pydantic import BaseModel, create_model


def build_side_effect_vars(test_function: Callable) -> BaseModel:
    # Parse function signature annotations
    funtion_arguments: dict[str, Any] = dict()
    for name, parameter in inspect.signature(test_function).parameters.items():
        funtion_arguments[name] = (
            parameter.annotation
            if parameter.annotation is not inspect.Signature.empty
            else Any,
            ...,
        )

    return create_model(
        "SideEffectVars",
        patched=(dict[str, Any], dict()),
        **funtion_arguments,
    )


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
    for func in funcs:
        code_string = inspect.getsource(func).strip()

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

    return LambdaGetter().get(code_string)


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
                                    f"Input {test.input} returned AST for {ast.unparse(actual_return).strip()} "
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
                                SideEffectVars = build_side_effect_vars(test.function)
                                side_effect_ast = ConvertSideEffect().visit(
                                    ast.parse(side_effect_source)
                                )
                                side_effect_code = ast.unparse(side_effect_ast)
                                l = SideEffectVars(
                                    patched=test.patches, **isolated_input
                                )
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
