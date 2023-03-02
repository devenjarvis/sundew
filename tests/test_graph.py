from sundew.graph import Graph
from sundew.test import test
from sundew.types import Function
from tests.fixtures import callee_func, dependent_func

test(Graph.add_connection)(
    kwargs={
        "self": Graph(),
        "node1": Function(callee_func),
        "node2": Function(dependent_func),
    },
    side_effects=[
        lambda _: _.self.functions["callee_func"].deps == {"dependent_func"},
    ],
)

# TODO: Add remaining Graph tests
