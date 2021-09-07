"""Contains base class for graph and other operators and operands."""

import cookie
import numpy as np

class Node(object):
    """Base class for nodes in graphs. Needs graph object in order to add itself
    to. Designed to be inherited for various operations.
    
    Args:
        graph: A cookie.engine.graphs.Graph instance.
        name: Optional name for node.
    """
    default_name_ctr = 0
    def __init__(self, graph: cookie.engine.graphs.Graph, name: str = ""):

        self.inputs = None
        self.outputs = None

    def op_func(self):
        raise NotImplementedError
    
    def __add__(self, obj):
        return self.value + obj.value

    def __sub__(self, obj):
        return self.value - obj.value

    def __mul__(self, obj):
        return self.value * obj.value

    def __div__(self, obj):
        return self.value / obj.value

    def __matmul__(self, obj):
        return self.value @ obj.value


class Graph(object):
    """Base class for graphs in cookie. Needs Context object to keep variables  
    and graphs in check.
    
    Args:
        ctx: A cookie.engine.context.Context instance.
        name: Optional name for graph.
    """
    default_name_ctr = 0
    def __init__(self, ctx:cookie.engine.context.Context, name:str = ""):
        if "/" in name:
            raise ValueError("`/` is not allowed for use in graph name.")
        if name == "":
            self.name = "Graph:" + "Graph_" + str(Graph.default_name_ctr)
            Graph.default_name_ctr += 1
        else:
            self.name = "Graph:" + name
        
        self.structure = []
        if not ctx.register_graph(self):
            raise ValueError("Graph with the same name exists.")

    def add_op_node(self, op_node):
        op_inputs_names = [i.name for i in op_node.inputs]
        op_outputs_names = [i.name for i in op_node.outputs]
        for in_edge in op_inputs_names:
            self.structure.append((in_edge, op_node.name))
        
        for out_edge in op_outputs_names:
            self.structure.append((op_node.name, out_edge))


    def build(self):
        pass

    def call(self, inputs):
        pass

    def _check_acyclic(self):
        pass

class Variable(object):
    default_name_ctr = 0
    def __init__(self, value, ctx, op, name=""):
        if "/" in name:
            raise ValueError("`/` is not allowed for use in variable name.")

        if name == "":
            self.name = "Variable:" + "Variable" + str(Variable.default_name_ctr)
            Variable.default_name_ctr += 1
        else:
            self.name = "Variable:" + name
        
        self.value = np.array(value)
        self.gradient = None
        self.dtype = value.dtype

        ctx.add_variable(self)


class Placeholder(object):
    default_name_ctr = 0

    def __init__(self, value, ctx, name=""):
        if "/" in name:
            raise ValueError("`/` is not allowed for use in placeholder name.")

        if name == "":
            self.name = "Placeholder:" + "Placeholder" + \
                str(Placeholder.default_name_ctr)
            Placeholder.default_name_ctr += 1
        else:
            self.name = "Placeholder:" + name

        self.value = np.array(value)
        self.gradient = None
        self.dtype = value.dtype

        ctx.add_placeholder(self)


class Constant(object):
    default_name_ctr = 0

    def __init__(self, value, ctx, name=""):
        if "/" in name:
            raise ValueError("`/` is not allowed for use in constant name.")

        if name == "":
            self.name = "Constant:" + "Constant" + \
                str(Constant.default_name_ctr)
            Constant.default_name_ctr += 1
        else:
            self.name = "Constant:" + name

        self._value = np.array(value)
        self.gradient = None
        self.dtype = value.dtype

        ctx.add_constant(self)
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self):
        raise ValueError("Cannot reassign constant")



class AddOp(Node):
    default_name_ctr = 0
    def __init__(self, graph):
        super(Node, self).__init__(graph)

        self.name = "AddOp" + str(AddOp.default_name_ctr)
        self.graph = graph
        AddOp.default_name_ctr += 1

    def op_func(self, inputs):
        sum = 0
        for i in inputs:
            sum += i.value
        output = Variable(sum)

        self.graph.add_op_node(self)
        return output

    def __call__(self, inputs):
        return self.op_func(inputs) 