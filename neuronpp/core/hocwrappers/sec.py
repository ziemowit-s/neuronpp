from neuronpp.core.cells.cell import Cell
from neuronpp.core.hocwrappers.hoc import Hoc


class Sec(Hoc):
    def __init__(self, obj, parent: Cell, name):
        Hoc.__init__(self, hoc_obj=obj, parent=parent, name=name)
