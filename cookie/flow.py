from cookie.tensor import Placeholder
from cookie.operators import Operator


def forward(topo_sorted_order, feed_dict=dict()):
    for node in topo_sorted_order:
        if isinstance(node, Placeholder):
            node.data = feed_dict[node.name]

        elif isinstance(node, Operator):
            node.data = node.forward(*[node_input.data for node_input in node.inputs])

    return topo_sorted_order[-1].data


def backward(topo_sorted_order):
    visited = set()
    topo_sorted_order[-1].grad = 1
    for node in reversed(topo_sorted_order):
        if isinstance(node, Operator):
            inputs = node.inputs
            grads = node.backward(
                *[incoming_node.data for incoming_node in node.inputs],
                dout=node.grad
            )

            for inp, grad in zip(inputs, grads):
                if inp not in visited:
                    inp.grad = grad
                else:
                    inp.grad += grad
                visited.add(inp)
    return [node.grad for node in topo_sorted_order]