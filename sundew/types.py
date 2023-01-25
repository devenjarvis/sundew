from dataclasses import dataclass, field
from typing import Any, Callable

from pydantic import BaseModel


class FunctionTest(BaseModel):
    function: Callable
    kwargs: dict[str, Any] = {}
    location: str
    patches: dict[str, Any] = {}
    returns: Any | None = None
    setup: set[Callable] = set()
    side_effects: list[Callable[[Any], bool]] = []


@dataclass(slots=True)
class FunctionName:
    simple: str
    qualified: str | None = None

    def __post_init__(self) -> None:
        if self.qualified is None:
            self.qualified = self.simple


@dataclass(slots=True)
class Function:
    name: FunctionName
    tests: list[FunctionTest] = field(default_factory=list)
    usage: set[str] = field(default_factory=set)
    deps: set[str] = field(default_factory=set)
