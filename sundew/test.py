import ast
import asyncio
import importlib
import inspect
import os
import sys
from contextlib import AbstractContextManager, ExitStack
from functools import wraps
from typing import Any, Callable, Coroutine, Generator
from unittest.mock import patch

from pydantic import BaseConfig, BaseModel, create_model
from rich import print
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeElapsedColumn,
)

from sundew.config import config
from sundew.side_effects import ConvertSideEffect, get_source
from sundew.types import FunctionName, FunctionTest


def update_test_graph(fn: Callable) -> None:
    func_name = fn.__name__
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
                    function = getattr(imported_module, sub_func_name)
                    parent_module = getattr(
                        function,
                        "__module__",
                        None,
                    )
                    # Only connect functions within the module
                    if parent_module in config.modules and inspect.isfunction(function):
                        config.test_graph.add_connection(
                            FunctionName(
                                simple=func_name,
                                qualified=".".join([module_name, func_name]),
                            ),
                            FunctionName(
                                simple=sub_func_name,
                                qualified=".".join([module_name, sub_func_name]),
                            ),
                        )
        else:
            print("Not sure how we get here yet")


def get_test_function(fn: Callable) -> Callable | Coroutine:
    @wraps(fn)
    def sundew_test_wrapper(
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> Callable:
        return fn(*args, **kwargs)

    @wraps(fn)
    async def async_sundew_test_wrapper(
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> Coroutine:
        return await fn(*args, **kwargs)

    if inspect.iscoroutinefunction(fn):
        return async_sundew_test_wrapper
    return sundew_test_wrapper


def test(fn: Callable) -> Callable:
    def add_test(
        setup: set[Generator[Any, None, None]] | None = None,
        kwargs: dict | None = None,
        returns: Any | None = None,
        patches: dict | None = None,
        side_effects: list[Callable] | None = None,
    ) -> Callable:
        update_test_graph(fn)

        config.test_graph.add_test(
            FunctionTest(
                function=get_test_function(fn),
                kwargs=kwargs or {},
                location=f"{os.path.relpath(inspect.stack()[1][1])}:{inspect.stack()[1][2]}",
                patches=patches or {},
                returns=returns,
                setup=setup or set(),
                side_effects=side_effects or [],
            )
        )

        return add_test

    return add_test


def apply_patches(test: FunctionTest, stack: ExitStack) -> None:
    if test.patches:
        for target, new in test.patches.items():
            stack.enter_context(patch(target, new))


def apply_fixtures(test: FunctionTest, stack: ExitStack) -> dict[str, Any]:
    fixture_yields = {}
    if test.setup:
        for fixture in test.setup:
            fixture_yield = stack.enter_context(fixture())
            fixture_yields[fixture.__name__] = fixture_yield

    return fixture_yields


def copy_function_inputs(test: FunctionTest) -> dict[str, Any]:
    isolated_inputs: dict[str, Any] = {}
    signature = inspect.signature(test.function)
    isolated_inputs = {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }

    for arg_name, input_value in test.kwargs.items():
        if callable(input_value):
            if isinstance(input_value(), AbstractContextManager):
                with input_value() as input_val:
                    result = input_val
            else:
                result = input_value()
        else:
            result = input_value
        isolated_inputs[arg_name] = result
    return isolated_inputs


def run_function(test: FunctionTest, isolated_input: dict[str, Any]) -> dict[str, Any]:
    if inspect.iscoroutinefunction(test.function):
        return asyncio.run(test.function(**isolated_input))
    return test.function(**isolated_input)


def check_test_exception(test: FunctionTest, e: Exception) -> None:
    # If we get an exception, check to see if it was expected
    if test.returns:
        assert isinstance(e, test.returns)
    else:
        raise e


def check_test_output(test: FunctionTest, actual_return: Any) -> None:  # noqa: ANN401
    if isinstance(actual_return, ast.Module) and isinstance(test.returns, ast.Module):
        assert (
            ast.unparse(actual_return).strip() == ast.unparse(test.returns).strip()
        ), (
            f"Input {test.kwargs} returned AST for "
            + f"{ast.unparse(actual_return).strip()} "
            + "which does not match the expected AST for "
            + f"{ast.unparse(test.returns).strip()}"
        )
    else:
        assert actual_return == test.returns, (
            f"Input {test.kwargs} returned {actual_return} "
            + "which does not match the expected return of "
            + f"{test.returns}"
        )


def build_side_effect_vars(test_function: Callable) -> type[BaseModel]:
    # Parse function signature annotations
    funtion_arguments: dict[str, tuple[Any, Any]] = {}
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

    return create_model(
        "SideEffectVars",
        **funtion_arguments,
        patches=(dict[str, Any], {}),
        __config__=Config,
    )  # type: ignore[call-overload]


def check_test_side_effects(test: FunctionTest, isolated_input: dict[str, Any]) -> None:
    if test.side_effects:
        side_effect_sources = get_source(test.side_effects)
        for side_effect_source in side_effect_sources:
            side_effect_ast = ConvertSideEffect().visit(ast.parse(side_effect_source))
            side_effect_code = ast.unparse(side_effect_ast)

            side_effect_arg_model = build_side_effect_vars(test.function)
            _ = side_effect_arg_model.construct(patches=test.patches, **isolated_input)
            exec(side_effect_code)  # noqa: S102


def run_test(
    test: FunctionTest,
    stack: ExitStack,
    tests_ran: TaskID,
    progress: Progress,
) -> None:
    try:
        # programmatically apply any patches defined
        apply_patches(test, stack)
        # programmatically apply any fixtures setup
        apply_fixtures(test, stack)
        try:
            # Isolate input arguments
            isolated_input = copy_function_inputs(test)
            # Run the test function once for evaluation
            actual_return = run_function(test, isolated_input)
        except Exception as e:  # noqa: BLE001
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
    except Exception as e:  # noqa: BLE001
        # Stop the progress bar
        progress.stop()
        # Log details of the error
        progress.console.print_exception(show_locals=True)
        print(f"\n[bold orange1]ERROR[/] {test.location} - {str(e)}")
        sys.exit(1)
    else:
        progress.advance(tests_ran)


def select_functions_to_test(function_name: str) -> list[str]:
    # Select function tests if provided
    if function_name:
        selected_functions = [function_name]
    else:  # Else get all tests
        selected_functions = [
            key
            for key in config.test_graph.functions
            if len(config.test_graph.functions[key].tests) > 0
        ]

    return selected_functions


def sort_tests(selected_functions: list[str]) -> list[FunctionTest]:
    # Kahn's algo to topologically sort test_graph
    all_nodes_added = False
    num_visited_nodes = 0
    sorted_tests: list[FunctionTest] = []
    functions_sorted = []

    while not all_nodes_added:
        for func_name in selected_functions:
            func = config.test_graph.functions[func_name]
            if len(func.deps) - num_visited_nodes == 0:
                sorted_tests.extend(func.tests)
                functions_sorted.append(func_name)
        if len(functions_sorted) == len(selected_functions):
            all_nodes_added = True
        else:
            num_visited_nodes += 1

    return sorted_tests


def detect_missing_tests(selected_functions: list[str]) -> list[str]:
    missing_tests: list[str] = []
    for function in config.test_graph.all_functions():
        if function not in selected_functions:
            function_name = config.test_graph.functions[function].name
            missing_tests.append(function_name.qualified or function_name.simple)

    return missing_tests


def run(function_name: str) -> None:
    with Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
    ) as progress:

        total_num_tests = sum(
            len(func.tests) for func in config.test_graph.functions.values()
        )

        selected_functions = select_functions_to_test(function_name)
        sorted_tests = sort_tests(selected_functions)
        missing_tests = detect_missing_tests(selected_functions)

        if missing_tests:
            progress.console.print(
                f"WARNING: Missing tests detected for {missing_tests}",
            )

        progress.console.print(
            f"Selected {len(sorted_tests)}/{total_num_tests} tests",
        )

        tests_ran = progress.add_task("Running tests...", total=len(sorted_tests))

        # Run all selecte tests
        for test in sorted_tests:
            with ExitStack() as stack:
                run_test(test, stack, tests_ran, progress)
