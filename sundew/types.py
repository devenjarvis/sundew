from pydantic import BaseModel
from typing import Any, Callable


class FunctionTest(BaseModel):
    location: str
    function: Callable
    input: dict[str, Any] = dict()
    returns: Any | None = None
    patches: dict[str, Any] = dict()
    side_effects: list[Callable[[Any], bool]] = []
