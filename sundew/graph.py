from sundew.types import Function, FunctionName, FunctionTest


class Graph:
    def __init__(self) -> None:
        self.functions: dict[str, Function] = {}

    def add_test(self, test: FunctionTest) -> None:
        function_name = test.function.__name__

        if function_name not in self.functions:
            self.functions[function_name] = Function(
                name=FunctionName(
                    simple=function_name,
                    qualified=test.function.__qualname__,
                )
            )
        self.functions[function_name].tests.append(test)

    def add_connection(self, node1: FunctionName, node2: FunctionName) -> None:
        # Assume connection is directional from A -> B
        # Add connection between node1 and node2
        if node1.simple not in self.functions:
            self.functions[node1.simple] = Function(name=node1)
        self.functions[node1.simple].deps.add(node2.simple)

        # Add connection between node2 and node1
        if node2.simple not in self.functions:
            self.functions[node2.simple] = Function(name=node2)
        self.functions[node2.simple].usage.add(node1.simple)

    def dependencies(self, node: str) -> set[str]:
        if node not in self.functions:
            self.functions[node] = Function(name=FunctionName(node))
        return self.functions[node].deps

    def all_functions(self) -> set[str]:
        all_deps = set()
        for function_under_test in self.functions.values():
            all_deps.add(function_under_test.name.simple)
            all_deps.update(function_under_test.deps)

        return all_deps

    def usage(self, node: str) -> set[str]:
        if node not in self.functions:
            self.functions[node] = Function(name=FunctionName(node))
        return self.functions[node].usage
