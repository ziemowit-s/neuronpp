from neuronpp.core.cells.core_cell import CoreCell
from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper


class VecStim(HocWrapper):
    def __init__(self, hoc_obj, parent: CoreCell, name):
        HocWrapper.__init__(self, hoc_obj=hoc_obj, parent=parent, name=name)
