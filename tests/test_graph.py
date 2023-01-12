from sundew.graph import Graph
from sundew.test import test, arg
import tests.fixtures as fixtures

test(Graph.add_connections)(
    input={"self": Graph(), "connections": [("A", "B")]},
    side_effects=[
        lambda: arg["self"].dep_graph["A"] == {"B"},
    ],
)

test(Graph.add)(
    input={"self": Graph(), "node1": "A", "node2": "B"},
    side_effects=[
        lambda: arg["self"].dep_graph["A"] == {"B"},
    ],
)

test(Graph.dependencies)(
    input={"self": Graph(), "node": "A"},
    returns={},
)

test(Graph.usage)(
    input={"self": Graph(), "node": "B"},
    returns={},
)
test(Graph.usage)(
    input={"self": fixtures.setup_simple_graph(), "node": "B"},
    returns={"A"},
)
