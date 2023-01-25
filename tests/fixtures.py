from contextlib import contextmanager
from typing import Any, Generator

from pydantic import BaseModel

from sundew.graph import Graph
from sundew.types import FunctionName, FunctionTest


@contextmanager
def setup_empty_graph() -> Generator[Graph, None, None]:
    try:
        new_graph = Graph()
        new_graph.add_connection(FunctionName("A"), FunctionName("B"))
        yield new_graph
    finally:
        # cleanup
        ...


def setup_simple_graph_2() -> Graph:
    new_graph = Graph()
    new_graph.add_connection(FunctionName("A"), FunctionName("B"))
    return new_graph


def example_fn_1(a: int, b: str) -> str:
    return b + str(a)


def example_fn_2(a: int, b: str = "hello") -> str:
    return b + str(a)


def example_fn_3(graph: Graph) -> None:
    graph.add_connection(FunctionName("C"), FunctionName("D"))


passing_function_test = FunctionTest(
    location="tests/fixtures.py:1000",
    function=example_fn_1,
    kwargs={"a": 1, "b": "2"},
    returns="21",
)

passing_function_test_with_defaults = FunctionTest(
    location="tests/fixtures.py:1000",
    function=example_fn_2,
    kwargs={"a": 1},
    returns="hello1",
)


def setup_simple_test_graph() -> Graph:
    new_graph = Graph()
    new_graph.add_connection(
        FunctionName("passing_function_test"),
        FunctionName("passing_function_test_with_defaults"),
    )
    new_graph.add_test(passing_function_test)
    new_graph.add_test(passing_function_test_with_defaults)
    return new_graph


passing_function_test_with_fixtures = FunctionTest(
    location="tests/fixtures.py:1000",
    fixtures={setup_empty_graph},
    function=example_fn_3,
    kwargs={"a": 1},
    returns="hello1",
)


class SideEffectVars(BaseModel):
    patched: dict[str, Any] = {}


class ExampleSideEffectVars(SideEffectVars):
    a: int
    b: str


def dependent_func() -> str:
    return "hello"


def callee_func() -> str:
    first_word = dependent_func()
    second_word = "world"
    return ", ".join([first_word, second_word])


dependent_func_function_test = FunctionTest(
    location="tests/fixtures.py:1000",
    function=dependent_func,
    returns="hello",
)

callee_func_function_test = FunctionTest(
    location="tests/fixtures.py:1000",
    function=callee_func,
    returns="hello, world",
)


def setup_test_graph_with_dependency() -> Graph:
    new_graph = Graph()
    new_graph.add_connection(
        FunctionName("callee_func"),
        FunctionName("dependent_func"),
    )
    new_graph.add_test(dependent_func_function_test)
    new_graph.add_test(callee_func_function_test)
    return new_graph
