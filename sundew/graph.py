from typing import Tuple
from collections import defaultdict


class Graph:
    def __init__(self, connections: list[Tuple[str, str]] | None = None):
        self.dep_graph: dict[str, set[str]] = defaultdict(set)
        self.usage_graph: dict[str, set[str]] = defaultdict(set)
        if connections:
            self.add_connections(connections)

    def add_connections(self, connections: list[Tuple[str, str]]):
        # Add connections (list of tuple pairs) to graph
        # Assume each pair is directional from A -> B
        for node1, node2 in connections:
            self.add(node1, node2)

    def add(self, node1: str, node2: str):
        # Add connection between node1 and node2
        self.dep_graph[node1].add(node2)
        # Add connection between node2 and node1
        self.usage_graph[node2].add(node1)

    def dependencies(self, node: str) -> set[str]:
        return self.dep_graph[node]

    def usage(self, node: str) -> set[str]:
        return self.usage_graph[node]
