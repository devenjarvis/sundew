import inspect
from collections.abc import Callable
from contextlib import ExitStack
from pathlib import Path
from typing import Any
from unittest.mock import patch

from sundew.config import config
from sundew.types import FunctionTest


class DependentFunctionSpy:
    def __init__(self, func: Callable) -> None:
        self.func = func
        self.calls: list[FunctionTest] = []
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
        self.calls.append(function_test)
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
        # Spy on all dependent functions
        mocks[dep_func_simple_name] = stack.enter_context(
            patch(
                dep_func.name.qualified,
                DependentFunctionSpy(dep_func.declaration),
            )
        )
    return mocks


def generate_naive_function_import(mock_name: str) -> tuple[str, str]:
    function_under_test = config.test_graph.functions[mock_name].name.qualified.split(
        "."
    )
    return (
        ".".join(function_under_test[:-1]),
        function_under_test[-1],
    )


def build_test_strings(fn_tests: list[FunctionTest]) -> str:
    all_function_tests = ""
    test_strings: set[str] = {test.__str__() for test in fn_tests}
    for test in test_strings:
        all_function_tests += test + "\n"

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
    fn: Callable,
    file_path: str,
    generated_test_file_import_string: str,
    generated_test_file: str,
) -> str:
    with (Path(file_path).resolve().parent / f"auto_test_{fn.__name__}.py").open(
        "w"
    ) as test_file:
        test_file.write(
            generated_test_file_import_string.expandtabs(4)
            + generated_test_file.expandtabs(4)
        )


def generate_function_dependency_test_file(
    fn: Callable, mocks: dict[str, DependentFunctionSpy]
) -> None:
    generated_test_file = ""
    generated_test_file_imports = set()
    for mock_name, mock_fn in mocks.items():
        generated_test_file_imports.add(generate_naive_function_import(mock_name))
        generated_test_file += build_test_strings(mock_fn.calls)

    generated_test_file_import_string = build_import_string(generated_test_file_imports)

    file_path: str = inspect.getmodule(fn).__file__ or ""  # type: ignore[union-attr]

    if generated_test_file:
        write_tests_to_file(
            fn, file_path, generated_test_file_import_string, generated_test_file
        )
