from sundew.types import Function, FunctionTest


class Graph:
    def __init__(self) -> None:
        self.functions: dict[str, Function] = {}

    def extend(self, other_graph: object) -> None:
        if isinstance(other_graph, Graph):
            self.functions.update(other_graph.functions)

    def add_test(self, test: FunctionTest) -> None:
        if test.name.simple not in self.functions:
            self.functions[test.name.simple] = Function(declaration=test.function)
        self.functions[test.name.simple].tests.add(test)

    def add_connection(self, node1: Function, node2: Function) -> None:
        # Assume connection is directional from A -> B
        # Add connection between node1 and node2
        if node1.name.simple not in self.functions:
            self.functions[node1.name.simple] = node1
        self.functions[node1.name.simple].deps.add(node2.name.simple)

        # Add connection between node2 and node1
        if node2.name.simple not in self.functions:
            self.functions[node2.name.simple] = node2
        self.functions[node2.name.simple].usage.add(node1.name.simple)

    def all_functions(self) -> set[str]:
        all_deps = set()
        for function_under_test in self.functions.values():
            all_deps.add(function_under_test.name.simple)
            all_deps.update(function_under_test.deps)

        return all_deps
