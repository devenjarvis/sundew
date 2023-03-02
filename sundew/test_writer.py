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
            generated_test_file += "\n"

    generated_test_file_import_string = ""
    grouped_generated_test_file_imports: dict[str, list[str]] = {
        "sundew.test": ["test"]
    }
    for generated_from, generated_import in generated_test_file_imports:
        grouped_generated_test_file_imports.setdefault(generated_from, []).append(
            generated_import
        )
    import_paren_limit = 2
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

    file_path: str = inspect.getmodule(fn).__file__ or ""  # type: ignore[union-attr]

    if generated_test_file:
        with (Path(file_path).resolve().parent / f"auto_test_{fn.__name__}.py").open(
            "w"
        ) as test_file:
            test_file.write(
                generated_test_file_import_string.expandtabs(4)
                + generated_test_file.expandtabs(4)
            )
