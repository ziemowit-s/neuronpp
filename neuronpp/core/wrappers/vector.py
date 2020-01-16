from neuronpp.core.cells.cell import Cell
from neuronpp.core.wrappers.hoc import Hoc


class Vector(Hoc):
    def __init__(self, hoc_obj, parent: Cell, name):
        Hoc.__init__(self, hoc_obj=hoc_obj, parent=parent, name=name)