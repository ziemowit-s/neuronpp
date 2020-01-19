from neuronpp.core.cells.core_cell import CoreCell
from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper


class NetConn(HocWrapper):
    def __init__(self, hoc_obj, name, parent: CoreCell):
        HocWrapper.__init__(self, hoc_obj=hoc_obj, parent=parent, name=name)