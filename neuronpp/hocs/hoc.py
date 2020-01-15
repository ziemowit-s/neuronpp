from neuronpp.cells.core.cell import Cell


class Hoc:
    def __init__(self, hoc_obj, parent, name):
        self.hoc = hoc_obj
        if isinstance(parent, Cell):
            parent = str(parent)
        self.parent = parent
        self.name = name

    def __repr__(self):
        return "{}_{}_{}".format(self.parent, self.__class__.__name__, self.name)

