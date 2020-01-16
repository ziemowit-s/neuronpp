from neuronpp.core.cells.cell import Cell
from neuronpp.core.wrappers.hoc import Hoc


class NetConn(Hoc):
    def __init__(self, hoc_obj, name, parent: Cell):
        Hoc.__init__(self, hoc_obj=hoc_obj, parent=parent, name=name)