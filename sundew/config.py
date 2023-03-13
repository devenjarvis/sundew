from pydantic import BaseSettings

from sundew.graph import Graph
from sundew.types import Cache


class Configuration(BaseSettings):
    modules: set[str] = set()
    test_graph: Graph = Graph()
    cache: Cache = Cache()


config = Configuration()
