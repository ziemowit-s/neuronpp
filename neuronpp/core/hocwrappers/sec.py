from neuronpp.core.cells.core_cell import CoreCell
from neuronpp.core.hocwrappers.hoc import Hoc


class Sec(Hoc):
    def __init__(self, obj, parent: CoreCell, name):
        Hoc.__init__(self, hoc_obj=obj, parent=parent, name=name)
