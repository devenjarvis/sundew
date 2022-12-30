from pydantic import BaseModel
from typing import Any, Callable


class FunctionTest(BaseModel):
    function: Callable
    input: dict[str, Any] = dict()
    returns: Any | None = None
    patches: dict[str, Any] = dict()
    side_effects: list[Callable] = []
