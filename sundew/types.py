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
