from neuronpp.core.cells.cell import Cell


class Hoc:
    def __init__(self, hoc_obj, parent: Cell, name):
        self.hoc = hoc_obj
        self.parent = str(parent)
        self.name = name

    def __repr__(self):
        return "{}_{}_{}".format(self.parent, self.__class__.__name__, self.name)

