"""Contains base class for graph and other operators and operands."""

import cookie

class Node(object):
    """Base class for nodes in graphs. Needs graph object in order to add itself
    to. Designed to be inherited for various operations.
    
    Args:
        graph: A cookie.engine.graphs.Graph instance.
        name: Optional name for node.
    """
    default_name_ctr = 0

    def __init__(self, graph: cookie.engine.graphs.Graph, name: str = ""):
        if "/" in name:
            raise ValueError("`/` is not allowed for use in context name.")

        if name == "":
            self.name = "Node:" + "Node_" + str(Graph.default_name_ctr)
            Graph.default_name_ctr += 1
        
        self.inputs, self.output_dtype = self.get_node_properties()

    def op_func(self):
        raise NotImplementedError
    
    def get_node_properties(self):
        raise NotImplementedError
        


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
            raise ValueError("`/` is not allowed for use in context name.")
        
        if name == "":
            self.name = "Graph:" + "Graph_" + str(Graph.default_name_ctr)
            Graph.default_name_ctr += 1
        else:
            self.name = "Graph:" + name
        self.variables = dict()



    def _check_acyclic(self):
        
