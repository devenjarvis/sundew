from sundew.graph import Graph
from sundew.test import test
from tests import fixtures

test(Graph.add_connections)(
    kwargs={"self": Graph(), "connections": [("A", "B")]},
    side_effects=[
        lambda _: _.self.dep_graph["A"] == {"B"},
    ],
)

test(Graph.add)(
    kwargs={"self": Graph(), "node1": "A", "node2": "B"},
    side_effects=[
        lambda _: _.self.dep_graph["A"] == {"B"},
    ],
)

test(Graph.dependencies)(
    kwargs={"self": Graph(), "node": "A"},
    returns={},
)

test(Graph.usage)(
    setup={fixtures.setup_empty_graph},
    kwargs={"self": Graph(), "node": "B"},
    returns={},
)

# Note: chained tests break failure links (always link to top most test)
test(Graph.usage)(
    kwargs={"self": fixtures.setup_empty_graph, "node": "B"},
    returns={"A"},
)
