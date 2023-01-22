from dataclasses import dataclass, field

from sundew.types import FunctionTest


@dataclass(slots=True)
class Function:
    tests: list[FunctionTest] = field(default_factory=list)
    usage: set[str] = field(default_factory=set)
    deps: set[str] = field(default_factory=set)


class Graph:
    def __init__(self) -> None:
        self.functions: dict[str, Function] = {}

    def add_test(self, test: FunctionTest) -> None:
        function_name = test.function.__name__

        if function_name not in self.functions:
            self.functions[function_name] = Function()
        self.functions[function_name].tests.append(test)

    def add_connection(self, node1: str, node2: str) -> None:
        # Assume connection is directional from A -> B
        # Add connection between node1 and node2
        if node1 not in self.functions:
            self.functions[node1] = Function()
        self.functions[node1].deps.add(node2)

        # Add connection between node2 and node1
        if node2 not in self.functions:
            self.functions[node2] = Function()
        self.functions[node2].usage.add(node1)

    def dependencies(self, node: str) -> set[str]:
        if node not in self.functions:
            self.functions[node] = Function()
        return self.functions[node].deps

    def usage(self, node: str) -> set[str]:
        if node not in self.functions:
            self.functions[node] = Function()
        return self.functions[node].usage
