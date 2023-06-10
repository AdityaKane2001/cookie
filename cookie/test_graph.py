from cookie.graph import Graph
from cookie.tensor import Constant, Variable
from cookie.operators import add, mul, topological_sort

with Graph() as g:
    x = Variable(g, 5.)
    y = Variable(g, 6.)
    c = Constant(g, 3.)
    z = x*y + c
    print(z)
    print(g.variables)
    print(g.constants)