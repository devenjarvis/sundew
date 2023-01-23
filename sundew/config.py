from pydantic import BaseSettings

from sundew.graph import Graph


class Configuration(BaseSettings):
    modules: set[str] = set()
    test_graph: Graph = Graph()


config = Configuration()
