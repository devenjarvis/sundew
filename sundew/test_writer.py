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


def generate_function_dependency_test_file(
    fn: Callable, mocks: dict[str, DependentFunctionSpy]
) -> None:
    generated_test_file = ""
    generated_test_file_imports = set()
    for mock_name, mock_fn in mocks.items():
        function_under_test = config.test_graph.functions[
            mock_name
        ].name.qualified.split(".")
        generated_test_file_imports.add(
            (
                ".".join(function_under_test[:-1]),
                function_under_test[-1],
            )
        )
        test_strings: set[str] = {test.__str__() for test in mock_fn.calls}
        for test in test_strings:
            generated_test_file += test
            generated_test_file += "\n\n"

    generated_test_file_import_string = "from sundew.test import test\n"
    for generated_from, generated_import in generated_test_file_imports:
        generated_test_file_import_string += (
            f"from {generated_from} import {generated_import}\n"
        )
    generated_test_file_import_string += "\n\n\n"

    file_path: str = inspect.getmodule(fn).__file__ or ""  # type: ignore[union-attr]

    if generated_test_file:
        with (Path(file_path).resolve().parent / f"auto_test_{fn.__name__}.py").open(
            "w"
        ) as test_file:
            test_file.write(generated_test_file_import_string + generated_test_file)
