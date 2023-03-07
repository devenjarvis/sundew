import inspect
from collections.abc import Callable
from contextlib import _GeneratorContextManager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True, eq=True)
class FunctionName:
    simple: str
    qualified: str


@dataclass(slots=True, eq=True)
class FunctionTest:
    function: Callable
    location: str = ""
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

    def formatted_kwargs(self) -> Any | None:
        formatted_kwargs = []
        for kwarg, kwval in self.kwargs.items():
            if inspect.isfunction(kwval):
                formatted_kwargs.append(f"{repr(kwarg)}: {kwval.__name__}")
            else:
                formatted_kwargs.append(f"{repr(kwarg)}: {repr(kwval)}")
        return f"{{{', '.join(formatted_kwargs)}}}"

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
            test_string += f"\tkwargs={self.formatted_kwargs()},\n"
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
            self.kwargs,
        ) + "patches={}, returns={}, setup={}, side_effects={})".format(
            self.patches,
            repr(self.returns),
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
