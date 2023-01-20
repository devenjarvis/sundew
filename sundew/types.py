from pydantic import BaseModel
from typing import Any, Callable


class FunctionTest(BaseModel):
    function: Callable
    input: dict[str, Any] = dict()
    location: str
    patches: dict[str, Any] = dict()
    returns: Any | None = None
    setup: set[Callable] = set()
    side_effects: list[Callable[[Any], bool]] = []
