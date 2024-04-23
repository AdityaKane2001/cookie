from cookie.graph import Graph
from cookie.tensor import Constant, Variable, Placeholder
from cookie.operators import add, mul, topological_sort
from cookie.flow import forward, backward
from cookie.plot_graph import make_graph


print("hello from test_graph.py!")

with Graph() as g:
    x = Variable(g, 0.9)
    y = Variable(g, 0.4)
    p1 = Placeholder(g, name="p1")
    c = Constant(g, 1.3)
    z1 = (x * y + c) * c + x
    z2 = p1 * z1 + x * y + c * z1

    topo_sorted_order = topological_sort(z2, g)
    # print(topo_sorted_order)

    output = forward(topo_sorted_order, feed_dict={"p1": 2.})
    grads = backward(topo_sorted_order)
    # print(output)
    # print(grads)
    print(len(topo_sorted_order))
        
    graph_fig = make_graph(topo_sorted_order)
    graph_fig.render(filename="assets/example")
