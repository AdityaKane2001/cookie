from graphviz import Digraph
from cookie.tensor import Placeholder
from cookie.operators import Operator


def make_graph(topo_sorted_order):
    f = Digraph(format="png")
    f.attr(rankdir="LR", size="10, 8")
    f.attr("node", shape="circle")
    for node in topo_sorted_order:
        shape = "box" if isinstance(node, Placeholder) else "circle"
        f.node(node.name, label=node.name, shape=shape)
    for node in topo_sorted_order:
        if isinstance(node, Operator):
            for e in node.inputs:
                f.edge(e.name, node.name, label=node.name)
    return f
