class Node():
    def __init__(self):
        pass
    
class Variable(Node):
    count = 0
    def __init__(self, graph, data=None, name=None):
        super().__init__()
        graph.variables.add(self)
        self.graph = graph
        self.data = data
        self.grad = None
        self.name = f"Variable/{Variable.count}" if name is None else name
        Variable.count += 1
        
    def __repr__(self):
        if self.grad is None:
            return f"variable {self.name}: data={self.data}"
        else:
            return f"variable {self.name}: data={self.data}, grad={self.grad}"
    

class Placeholder(Node):
    count = 0
    
    def __init__(self, graph, name=None):
        super().__init__()
        graph.placeholders.add(self)
        self.graph = graph
        self.data = None
        self.grad = None
        self.name = f"Placeholder/{Placeholder.count}" if name is None else name
        Placeholder.count += 1
        
    def __repr__(self):
        if self.grad is None:
            return f"Placeholder {self.name}: data={self.data}"
        else:
            return f"Placeholder {self.name}: data={self.data}, grad={self.grad}"
    
class Constant(Node):
    count = 0
    def __init__(self, graph, data, name=None):
        super().__init__()
        graph.constants.add(self)
        self.graph = graph
        self._data = data
        self.grad = None
        self.name = f"Const/{Constant.count}" if name is None else name
        Constant.count += 1
        
    def __repr__(self):
        if self.grad is None:
            return f"Constant {self.name}: data={self.data}"
        else:
            return f"Constant {self.name}: data={self.data}, grad={self.grad}"
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self):
        raise ValueError("Cannot reassign constant")