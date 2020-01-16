from neuronpp.core.cells.cell import Cell
from neuronpp.core.hocwrappers.hoc import Hoc


class NetStim(Hoc):
    def __init__(self, hoc_obj, parent: Cell, name):
        Hoc.__init__(self, hoc_obj=hoc_obj, parent=parent, name=name)