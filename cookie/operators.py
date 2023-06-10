from cookie.graph import Node
from cookie.tensor import Variable, Constant, Placeholder


def node_checker(func, self, other):
    if isinstance(other, Node):
        return func(self, other)
    if isinstance(other, int) or isinstance(other, float):
        return func(self, Constant(other))
    raise TypeError(f"Incompatible types for operator {func}: {type(self)}, {type(other)}")


class Operator(Node):
    def __init__(self, graph):
        graph.operators.add(self)
        self.graph = graph
        self.value = None
        self.inputs = []
        self.gradient = None

    def __repr__(self):
        return f"Operator: name:{self.name}"


class add(Operator):
    count = 0

    def __init__(self, a, b, name="add"):
        assert a.graph == b.graph
        super().__init__(a.graph)
        self.inputs = [a, b]
        self.name = f"{name}_{add.count}" if name is None else name

    def forward(self, a, b):
        return a + b

    def backward(self, a, b, dout):
        return dout, dout


class mul(Operator):
    count = 0

    def __init__(self, a, b, name="mul"):
        assert a.graph == b.graph
        super().__init__(a.graph)
        self.inputs = [a, b]
        self.name = f"{name}_{add.count}" if name is None else name

    def forward(self, a, b):
        return a * b

    def backward(self, a, b, dout):
        return dout * b, dout * a


class matmul(Operator):
    count = 0

    def __init__(self, a, b, name="matmul"):
        assert a.graph == b.graph
        super().__init__(a.graph)
        self.inputs = [a, b]
        self.name = f"{name}_{add.count}" if name is None else name

    def forward(self, a, b):
        return a @ b

    def backward(self, a, b, dout):
        return dout @ b.T, dout @ a.T


def topological_sort(root, graph):
    visited = set()
    order = list()
    
    def _dfs(node):
        if node not in visited:
            visited.add(node)
            if isinstance(node, Operator):
                for ip in node.inputs:
                    _dfs(ip)
            order.append(node)
    
    if root is None:
        for _node in graph.operators:
            _dfs(_node)

    else:
        _dfs(root)
    
    return order


Node.__add__ = lambda self, other: node_checker(add, self, other)
Node.__mul__ = lambda self, other: node_checker(mul, self, other)
Node.__matmul__ = lambda self, other: node_checker(matmul, self, other)
