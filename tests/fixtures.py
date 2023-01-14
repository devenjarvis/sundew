from sundew.graph import Graph
from sundew.types import FunctionTest
from pydantic import BaseModel
from typing import Any


def setup_simple_graph():
    new_graph = Graph()
    new_graph.add("A", "B")
    return new_graph


def example_fn_1(a: int, b: str) -> str:
    return b + str(a)


def example_fn_2(a: int, b: str = "hello") -> str:
    return b + str(a)


passing_function_test = FunctionTest(
    location="tests/fixtures.py:1000",
    function=example_fn_1,
    input={"a": 1, "b": "2"},
    returns="21",
)

passing_function_test_with_defaults = FunctionTest(
    location="tests/fixtures.py:1000",
    function=example_fn_2,
    input={"a": 1},
    returns="hello1",
)


class SideEffectVars(BaseModel):
    patched: dict[str, Any] = dict()


class ExampleSideEffectVars(SideEffectVars):
    a: int
    b: str
