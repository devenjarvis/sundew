import ast
import copy
from functools import wraps
import sys
import asyncio
from typing import Any, Callable, Coroutine, Type
import inspect
import importlib
from sundew.config import config
from sundew.types import FunctionTest
from sundew.side_effects import ConvertSideEffect, get_source
from contextlib import ExitStack
from unittest.mock import patch
from pydantic import BaseConfig, create_model, BaseModel
from rich import print
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    MofNCompleteColumn,
    TimeElapsedColumn,
    TaskID,
)
import os


def update_function_graph(fn: Callable) -> None:
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
            print("Not sure how we get here yet")


def get_test_function(fn: Callable) -> Callable | Coroutine:
    @wraps(fn)
    def sundew_test_wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    @wraps(fn)
    async def async_sundew_test_wrapper(*args, **kwargs):
        return await fn(*args, **kwargs)

    if inspect.iscoroutinefunction(fn):
        return async_sundew_test_wrapper
    else:
        return sundew_test_wrapper


def test(fn) -> Callable:
    def add_test(
        input: dict = dict(),
        returns: Any | None = None,
        patches: dict = dict(),
        side_effects: list[Callable] = [],
    ) -> Callable:
        update_function_graph(fn)

        config.tests.append(
            FunctionTest(
                location=f"{os.path.relpath(inspect.stack()[1][1])}:{inspect.stack()[1][2]}",
                function=get_test_function(fn),
                input=input,
                returns=returns,
                patches=patches,
                side_effects=side_effects,
            )
        )

        return add_test

    return add_test


def apply_patches(test: FunctionTest, stack: ExitStack):
    if test.patches:
        for target, new in test.patches.items():
            stack.enter_context(patch(target, new))


def copy_function_inputs(test: FunctionTest) -> dict[str, Any]:
    signature = inspect.signature(test.function)
    defaults = {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }
    return copy.deepcopy(defaults | test.input)


def run_function(test: FunctionTest, isolated_input: dict[str, Any]) -> dict[str, Any]:
    if inspect.iscoroutinefunction(test.function):
        return asyncio.run(test.function(**isolated_input))
    else:
        return test.function(**isolated_input)


def check_test_exception(test: FunctionTest, e: Exception) -> None:
    # If we get an exception, check to see if it was expected
    if test.returns:
        assert isinstance(e, test.returns)
    else:
        raise e


def check_test_output(test: FunctionTest, actual_return: Any) -> None:
    if test.returns:
        if isinstance(actual_return, ast.Module):
            assert (
                ast.unparse(actual_return).strip() == ast.unparse(test.returns).strip()
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


def build_side_effect_vars(test_function: Callable) -> Type[BaseModel]:
    # Parse function signature annotations
    funtion_arguments: dict[str, tuple[Any, Any]] = dict()
    for name, parameter in inspect.signature(test_function).parameters.items():
        funtion_arguments[name] = (
            # parameter or Any,
            parameter.annotation
            if parameter.annotation is not inspect.Signature.empty
            else Any,
            ...,
        )

    class Config(BaseConfig):
        arbitrary_types_allowed = True

    model = create_model(
        "SideEffectVars",
        **funtion_arguments,
        patches=(dict[str, Any], dict()),
        __config__=Config,
    )  # type: ignore

    return model


def check_test_side_effects(test: FunctionTest, isolated_input: dict[str, Any]) -> None:
    if test.side_effects:
        side_effect_sources = get_source(test.side_effects)
        for side_effect_source in side_effect_sources:
            side_effect_ast = ConvertSideEffect().visit(ast.parse(side_effect_source))
            side_effect_code = ast.unparse(side_effect_ast)

            # Replace variables used by side_effects
            # arg = isolated_input  # noqa: F841
            # patched = test.patches  # noqa: F841
            # _ = create_model('SideEffectVars', foo=(str, ...), bar=123)
            SideEffectVarsModel = build_side_effect_vars(test.function)
            _ = SideEffectVarsModel(patches=test.patches, **isolated_input)
            exec(side_effect_code)


def run_test(
    test: FunctionTest, stack: ExitStack, tests_ran: TaskID, progress: Progress
):
    try:
        # programmatically apply any patches defined
        apply_patches(test, stack)
        try:
            # Isolate input arguments
            isolated_input = copy_function_inputs(test)
            # Run the test function once for evaluation
            actual_return = run_function(test, isolated_input)
        except Exception as e:
            # If we get an exception, check if it's expected
            check_test_exception(test, e)
        else:
            # If we didn't get an exception then check the output normally
            check_test_output(test, actual_return)
        finally:
            # Check if we have defined side effects
            check_test_side_effects(test, isolated_input)

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
                run_test(test, stack, tests_ran, progress)
