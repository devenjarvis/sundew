import inspect
from collections.abc import Callable
from contextlib import ExitStack
from pathlib import Path
from typing import Any
from unittest.mock import patch

import black

from sundew.config import config
from sundew.types import FunctionTest


class DependentFunctionSpy:
    def __init__(self, func: Callable) -> None:
        self.func = func
        self.calls: set[FunctionTest] = set()
        self.__name__ = func.__name__
        self.__qualname__ = func.__qualname__

    def __call__(
        self, *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> Any:  # noqa: ANN401
        answer = self.func(*args, **kwargs)
        function_test = FunctionTest(
            function=self.func,
            kwargs=inspect.getcallargs(self.func, *args, **kwargs),
            returns=answer,
        )
        self.calls.add(function_test)
        return answer

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DependentFunctionSpy):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return (
            self.func.__code__.co_code == other.func.__code__.co_code
            and self.calls == other.calls
        )


def mock_function_dependencies(
    fn: Callable, stack: ExitStack
) -> dict[str, DependentFunctionSpy]:
    mocks: dict[str, DependentFunctionSpy] = {}
    for dep_func_simple_name in config.test_graph.functions[fn.__name__].deps:
        dep_func = config.test_graph.functions[dep_func_simple_name]
        # Recursively mock sub-dependent functions
        if (
            config.test_graph.functions[dep_func_simple_name].deps
            and dep_func_simple_name != "mock_function_dependencies"
        ):
            mocks.update(mock_function_dependencies(dep_func.declaration, stack))
        # Spy on all dependent functions
        mocks[dep_func_simple_name] = stack.enter_context(
            patch(
                dep_func.name.qualified,
                DependentFunctionSpy(dep_func.declaration),
            )
        )
    return mocks


def check_kwargs_for_imports(test_fn: FunctionTest) -> list[list[str]]:
    imports = []
    for kwval in test_fn.kwargs.values():
        if inspect.isfunction(kwval) or inspect.isclass(kwval):
            module = inspect.getmodule(kwval)
            qualified_name_array = [module.__name__] if module else []
            qualified_name_array.append(kwval.__name__)
            imports.append(qualified_name_array)
        elif isinstance(kwval, (list, tuple, set)):
            for el in kwval:
                if inspect.isfunction(el):
                    module = inspect.getmodule(el)
                    qualified_name_array = [module.__name__] if module else []
                    qualified_name_array.append(el.__name__)
                    imports.append(qualified_name_array)
                elif hasattr(el, "__slots__"):
                    module = inspect.getmodule(type(el))
                    qualified_name_array = [module.__name__] if module else []
                    qualified_name_array.append(type(el).__name__)
                    imports.append(qualified_name_array)
    return imports


def check_returns_for_imports(test_fn: FunctionTest) -> list[list[str]]:
    imports = []
    if inspect.isfunction(test_fn.returns):
        module = inspect.getmodule(test_fn.returns)
        qualified_name_array = [module.__name__] if module else []
        qualified_name_array.append(test_fn.returns.__name__)
        imports.append(qualified_name_array)
    elif isinstance(test_fn.returns, Path):
        imports.append(["pathlib", "PosixPath"])

    return imports


def generate_naive_function_import(
    mock_name: str, mock_test_functions: set[FunctionTest]
) -> list[tuple[str, str]]:
    imports = []
    # Get main function import
    imports.append(config.test_graph.functions[mock_name].name.qualified.split("."))
    # Check for any additional functions in kwargs
    for test_fn in mock_test_functions:
        imports.extend(check_kwargs_for_imports(test_fn))
        imports.extend(check_returns_for_imports(test_fn))

    return [
        (
            ".".join(function_under_test[:-1]),
            function_under_test[-1],
        )
        for function_under_test in imports
    ]


def build_test_strings(fn_tests: set[FunctionTest]) -> str:
    all_function_tests = ""
    # Sort tests alphabeticaly by function name
    for test in sorted(fn_tests):
        all_function_tests += test.__str__() + "\n"

    return all_function_tests


def build_import_string(generated_test_file_imports: set[tuple[str, str]]) -> str:
    generated_test_file_import_string = ""
    import_paren_limit = 2

    # Group naive test imports
    grouped_generated_test_file_imports: dict[str, list[str]] = {
        "sundew.test": ["test"]
    }
    for generated_from, generated_import in generated_test_file_imports:
        grouped_generated_test_file_imports.setdefault(generated_from, []).append(
            generated_import
        )

    # Build import string from groups
    for grouped_from, grouped_import in sorted(
        grouped_generated_test_file_imports.items()
    ):
        generated_test_file_import_string += "from {} import {}{}{}\n".format(
            grouped_from,
            "(\n\t" if len(grouped_import) > import_paren_limit else "",
            ",\n\t".join(sorted(grouped_import))
            if len(grouped_import) > import_paren_limit
            else ", ".join(sorted(grouped_import)),
            ",\n)" if len(grouped_import) > import_paren_limit else "",
        )
    generated_test_file_import_string += "\n"
    return generated_test_file_import_string


def write_tests_to_file(
    file_path: Path,
    generated_test_file_import_string: str,
    generated_test_file: str,
) -> None:
    with (file_path).open("w") as test_file:
        test_file.write(
            generated_test_file_import_string.expandtabs(4)
            + generated_test_file.expandtabs(4)
        )
    # Auto format file
    black.format_file_in_place(
        file_path,
        fast=True,
        mode=black.FileMode(),
        write_back=black.WriteBack.YES,
    )


def build_file_path(fn: Callable) -> Path:
    if module_path := inspect.getmodule(fn).__file__:  # type: ignore[union-attr]
        file_path = Path(module_path).resolve()
    else:
        file_path = Path(".").resolve()

    for _ in config.test_graph.functions[fn.__name__].name.qualified.split(".")[:-1]:
        file_path = file_path.parent
    file_path = file_path / "tests"
    for directory in config.test_graph.functions[fn.__name__].name.qualified.split(".")[
        1:-1
    ]:
        # Create directory
        file_path /= directory

    file_path /= f"auto_test_{fn.__name__}.py"

    return file_path


def generate_function_dependency_test_file(
    fn: Callable, mocks: dict[str, DependentFunctionSpy]
) -> None:
    generated_test_file_imports = set()
    mock_calls: set[FunctionTest] = set()
    # Build imports
    for mock_name, mock_fn in mocks.items():
        # Only add imports if we generated tests for the mocked function
        if mock_fn.calls:
            for generated_import in generate_naive_function_import(
                mock_name, mock_fn.calls
            ):
                generated_test_file_imports.add(generated_import)
            # Only add tests we don't have written already
            mock_calls.update(
                mock_fn.calls - config.test_graph.functions[mock_name].tests
            )

    generated_test_file_import_string = build_import_string(generated_test_file_imports)

    # Build file path
    file_path = build_file_path(fn)

    # Build test file all at once
    generated_test_file = build_test_strings(mock_calls)

    if generated_test_file:
        file_path.parents[0].mkdir(parents=True, exist_ok=True)
        # Add __init__.py if it doesn't exist
        (file_path.parents[0] / "__init__.py").touch()
        write_tests_to_file(
            file_path, generated_test_file_import_string, generated_test_file
        )
