from neuronpp.core.cells.core_cell import CoreCell
from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper


class Sec(HocWrapper):
    def __init__(self, obj, parent: CoreCell, name):
        HocWrapper.__init__(self, hoc_obj=obj, parent=parent, name=name)

    def __call__(self, loc):
        return self.hoc(loc)
