from cookie.tensor import Node, Variable, Constant, Placeholder


class Graph:
    def __init__(self):
        self.variables = set()
        self.constants = set()
        self.placeholders = set()
        self.operators = set()

    def reset_counts(self, root):
        if hasattr(root, "count"):
            root.count = 0
        else:
            for child in root.__subclasses__():
                self.reset_counts(child)

    def delete_session(self):
        for var in self.variables:
            del var

        for const in self.constants:
            del const

        for placeholder in self.placeholders:
            del placeholder

        for op in self.operators:
            del op

        self.reset_counts(Node)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.delete_session()


if __name__ == "__main__":
    with Graph() as g:
        print(g.constants)
