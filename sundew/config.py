from pydantic import BaseSettings

from sundew.graph import Graph
from sundew.types import FunctionTest


class Configuration(BaseSettings):
    modules: set[str] = set()
    function_graph: Graph = Graph()
    tests: list[FunctionTest] = []


config = Configuration()
