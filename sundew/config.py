from pydantic import BaseSettings

from sundew.graph import Graph
from sundew.types import FunctionTest


class Configuration(BaseSettings):
    modules: set[str] = set()
    test_graph: Graph = Graph()


config = Configuration()
