from sundew import test
from sundew.graph import Graph
from sundew.types import Function
from tests.fixtures import callee_func, dependent_func

test(Graph.add_connection)(
    kwargs={
        "self": Graph(),
        "node1": Function(callee_func),
        "node2": Function(dependent_func),
    },
    side_effects=[
        lambda _: _.self.functions["tests.fixtures.callee_func"].deps
        == {"tests.fixtures.dependent_func"},
    ],
)

# TODO: Add remaining Graph tests
