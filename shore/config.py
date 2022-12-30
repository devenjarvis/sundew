from pydantic import BaseSettings
from shore.graph import Graph
from shore.types import FunctionTest


class Configuration(BaseSettings):
    modules: set[str] = set()
    function_graph: Graph = Graph()
    tests: list[FunctionTest] = []


config = Configuration()
