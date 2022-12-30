from pydantic import BaseModel
from typing import Any, Callable


class FunctionTest(BaseModel):
    function: Callable
    input: dict[str, Any] = dict()
    output: Any | None = None
    patched: dict[str, Any] = dict()
    side_effects: list[Callable] = []
