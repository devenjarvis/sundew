from sundew.graph import Graph
from pydantic import BaseModel
from typing import Any


def setup_simple_graph():
    new_graph = Graph()
    new_graph.add("A", "B")
    return new_graph


def example_fn(a: int, b: str) -> str:
    return b + str(a)


# def example_function():
#     def my_func(a: int, b: str) -> str:
#         pass

#     return my_func


class SideEffectVars(BaseModel):
    patched: dict[str, Any] = dict()


class ExampleSideEffectVars(SideEffectVars):
    a: int
    b: str
