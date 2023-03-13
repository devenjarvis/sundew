import inspect
from collections.abc import Callable
from contextlib import _GeneratorContextManager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


def format_kwargs(kwargs: dict[str, Any]) -> str:
    formatted_kwargs = []
    for kwarg, kwval in kwargs.items():
        if isinstance(kwval, set):
            formatted_kwargs.append(f"{repr(kwarg)}: {kwval}")
        elif inspect.isfunction(kwval):
            formatted_kwargs.append(f"{repr(kwarg)}: {kwval.__name__}")
        else:
            formatted_kwargs.append(f"{repr(kwarg)}: {repr(kwval)}")
    return f"{{{', '.join(formatted_kwargs)}}}"


@dataclass(slots=True, eq=True)
class FunctionName:
    simple: str
    qualified: str


@dataclass(slots=True, eq=True)
class FunctionTest:
    function: Callable
    location: str = ""
    cache: bool = False
    kwargs: dict[str, Any] = field(default_factory=dict)
    patches: dict[str, Any] = field(default_factory=dict)
    returns: Any | None = None
    setup: set[Callable[[], _GeneratorContextManager[Any]]] = field(default_factory=set)
    side_effects: list[Callable[[Any], bool]] = field(default_factory=list)

    @property
    def name(self) -> FunctionName:
        simple_name = self.function.__name__
        qualified_name = self.function.__qualname__
        if simple_name == qualified_name:
            module = inspect.getmodule(self.function)
            qualified_name_array = [module.__name__] if module else []
            qualified_name_array.append(simple_name)
            qualified_name = ".".join(qualified_name_array)

        return FunctionName(simple=simple_name, qualified=qualified_name)

    def formatted_returns(self) -> Any | None:
        if isinstance(self.returns, str):
            return repr(self.returns).replace('"', r"\"")
        if isinstance(self.returns, Path):
            return repr(self.returns)
        return self.returns

    def __str__(self) -> str:
        test_string = ""
        test_string += f"test({self.name.simple})(\n"
        if self.patches:
            test_string += f"\tpatches={self.patches},\n"
        if self.setup:
            test_string += f"\tsetup={self.setup},\n"
        if self.kwargs:
            test_string += f"\tkwargs={format_kwargs(self.kwargs)},\n"
        if self.setup:
            test_string += f"\tside_effects={self.side_effects},\n"
        if self.returns:
            test_string += f"\treturns={self.formatted_returns()},\n"
        test_string += ")"

        # Python formatters prefer double quotes, let's try to adhere
        return test_string.replace("'", '"')

    def __repr__(self) -> str:
        return "FunctionTest(function={}, kwargs={}, ".format(
            self.function.__name__,
            format_kwargs(self.kwargs),
        ) + "patches={}, returns={}, setup={}, side_effects={})".format(
            self.patches,
            self.formatted_returns(),
            self.setup,
            self.side_effects,
        )

    def __hash__(self) -> int:
        return hash(repr(self))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FunctionTest):
            return NotImplemented
        return repr(self) == repr(other)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, FunctionTest):
            return NotImplemented
        return self.function.__name__ < other.function.__name__


@dataclass(slots=True)
class Function:
    declaration: Callable
    tests: set[FunctionTest] = field(default_factory=set)
    usage: set[str] = field(default_factory=set)
    deps: set[str] = field(default_factory=set)

    @property
    def name(self) -> FunctionName:
        simple_name = self.declaration.__name__
        qualified_name = self.declaration.__qualname__
        if simple_name == qualified_name:
            module = inspect.getmodule(self.declaration)
            qualified_name_array = [module.__name__] if module else []
            qualified_name_array.append(simple_name)
            qualified_name = ".".join(qualified_name_array)

        return FunctionName(simple=simple_name, qualified=qualified_name)


@dataclass()
class Cache:
    cache: dict[str, dict[str, Any]] = field(default_factory=dict)

    def contains(self, function: Callable, kwargs: dict[str, Any]) -> bool:
        function_name = function.__name__
        try:
            self.cache[function_name][format_kwargs(kwargs)]
        except KeyError:
            return False
        else:
            return True

    def get_cached_value(
        self, function: Callable, kwargs: dict[str, Any]
    ) -> Any:  # noqa: ANN401
        function_name = function.__name__
        return self.cache[function_name][format_kwargs(kwargs)]

    def update(
        self, function: Callable, kwargs: dict[str, Any], returns: Any  # noqa: ANN401
    ) -> None:
        function_name = function.__name__
        if function_name not in self.cache:
            self.cache[function_name] = {}
        self.cache[function_name][format_kwargs(kwargs)] = returns
