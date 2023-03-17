import ast
import asyncio
import importlib
import inspect
import os
import sys
from collections.abc import Callable, Coroutine
from contextlib import ExitStack, _GeneratorContextManager
from functools import wraps
from typing import Any, Optional, Union
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
from sundew.test_writer import (
    generate_function_dependency_test_file,
    mock_function_dependencies,
)
from sundew.types import Function, FunctionTest


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
                    sub_function = getattr(imported_module, sub_func_name)
                    parent_module = getattr(
                        sub_function,
                        "__module__",
                        None,
                    )
                    # Only connect functions within the module
                    if parent_module in config.modules and inspect.isfunction(
                        sub_function
                    ):
                        config.test_graph.add_connection(
                            Function(declaration=fn),
                            Function(declaration=sub_function),
                        )
        else:
            print("Not sure how we get here yet.")


def get_test_function(fn: Callable) -> Callable:
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
        async_sundew_test_wrapper.__signature__ = inspect.signature(  # type: ignore[attr-defined]
            fn
        )
        return async_sundew_test_wrapper
    sundew_test_wrapper.__signature__ = inspect.signature(fn)  # type: ignore[attr-defined]
    return sundew_test_wrapper


def test(fn: Callable) -> Callable:
    def add_test(
        cache: bool = False,  # noqa: FBT
        setup: Optional[set[Callable[[], _GeneratorContextManager[Any]]]] = None,
        kwargs: Optional[dict[str, Any]] = None,
        returns: Union[Any, Exception, None] = None,
        patches: Optional[dict[str, Any]] = None,
        side_effects: Optional[list[Callable]] = None,
    ) -> Callable:
        update_test_graph(fn)

        config.test_graph.add_test(
            FunctionTest(
                function=get_test_function(fn),
                kwargs=kwargs or {},
                cache=cache,
                location=f"{os.path.relpath(inspect.stack()[1][1])}:{inspect.stack()[1][2]}",
                patches=patches or {},
                returns=returns,
                setup=setup or set(),
                side_effects=side_effects or [],
            ),
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
            fixture_yield: Any = stack.enter_context(fixture())
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
            if inspect.isgeneratorfunction(input_value):  # type: ignore[arg-type]
                with input_value() as input_val:
                    result = input_val
            else:
                result = input_value
        else:
            result = input_value
        isolated_inputs[arg_name] = result
    return isolated_inputs


def run_function(
    test: FunctionTest, isolated_input: dict[str, Any]
) -> Any:  # noqa: ANN401
    if test.cache and config.cache.contains(test.function, test.kwargs):
        return config.cache.get_cached_value(test.function, test.kwargs)

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
    #     assert actual_return.__code__.co_code == test.returns.__code__.co_code, (
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


def check_test_side_effects(
    test: FunctionTest,
    actual_return: Any,  # noqa: ANN401
    isolated_input: dict[str, Any],
) -> None:
    if test.side_effects:
        side_effect_sources = get_source(test.side_effects)
        for side_effect_source in side_effect_sources:
            side_effect_ast = ConvertSideEffect().visit(ast.parse(side_effect_source))
            side_effect_code = ast.unparse(side_effect_ast)

            side_effect_arg_model = build_side_effect_vars(test.function)
            _ = side_effect_arg_model.construct(
                patches=test.patches, returns=actual_return, **isolated_input
            )
            exec(side_effect_code)  # noqa: S102


def run_test(
    test: FunctionTest,
    stack: ExitStack,
    tests_ran: TaskID,
    progress: Progress,
    enable_auto_test_writer: bool,  # noqa: FBT001
) -> None:
    try:
        # programmatically apply any patches defined
        apply_patches(test, stack)
        # programmatically apply any fixtures setup
        apply_fixtures(test, stack)
        try:
            # Isolate input arguments
            isolated_input = copy_function_inputs(test)

            # Mock dependent functions to be able to write regression tests
            mocks = mock_function_dependencies(test.function, stack)

            # Run the test function once for evaluation
            actual_return = run_function(test, isolated_input)

            if enable_auto_test_writer:
                # Write tests with mock data
                generate_function_dependency_test_file(test.function, mocks)

        except Exception as e:  # noqa: BLE001
            # If we get an exception, check if it's expected
            check_test_exception(test, e)
        else:
            # If we didn't get an exception then check the output normally
            if test.returns:
                check_test_output(test, actual_return)
        finally:
            # Check if we have defined side effects
            check_test_side_effects(test, actual_return, isolated_input)

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
        if test.cache:
            config.cache.update(test.function, test.kwargs, actual_return)

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


def run(function_name: str, enable_auto_test_writer: bool) -> None:  # noqa: FBT001
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

        # Run all selected tests
        for test in sorted_tests:
            with ExitStack() as stack:
                run_test(test, stack, tests_ran, progress, enable_auto_test_writer)
