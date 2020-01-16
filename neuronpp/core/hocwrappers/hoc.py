from neuronpp.core.cells.core_cell import CoreCell


class Hoc:
    def __init__(self, hoc_obj, parent: CoreCell, name):
        self.hoc = hoc_obj
        self.parent = str(parent)
        self.name = name

    def __repr__(self):
        return "{}+{}+{}".format(self.parent, self.__class__.__name__, self.name)

