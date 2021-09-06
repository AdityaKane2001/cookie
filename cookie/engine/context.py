"""Contains defiition for base Context class."""

import cookie
from typing import List

class Context(object):
    """
    Base class for specialized contexts (if any). Contains all required 
    information to build and execute graphs. Heirarchy of execution is Context,
    Graph then Nodes. Here execution means forward pass. 

    Args:
        name: An optional name for the context
        graphs: Optional list of graphs in that context. 
    """
    default_name_ctr = 0
    global_contexts = []

    def __init__(self, name:str = "", graphs: List = []):
        if "/" in name:
            raise ValueError("`/` is not allowed for use in context name.")
        if name == "":
            self.name = "Context:" + "Context_" + str(Context.default_name_ctr)
            Context.default_name_ctr += 1
        self.name = "Context:" + name
        self.assets = dict()
        Context.global_contexts.append(self.name)

    def _register_graphs(self, graphs:List[cookie.engine.graphs.Graph]) -> bool:
        for graph in graphs:
            if graph.name in self.assets.keys():
                return True
            self.assets[graph.name] = (graph, [])
            self.assets[graph.name][1] += graph.objects
        
        return True
    
    def _register_graph(self, graph: cookie.engine.graphs.Graph) -> bool:
        if graph.name in self.assets.keys():
            return True
        self.assets[graph.name] = (graph, [])
        self.assets[graph.name][1] += graph.objects

        return True
    
    def __enter__(self) -> cookie.engine.context.Context:
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass
