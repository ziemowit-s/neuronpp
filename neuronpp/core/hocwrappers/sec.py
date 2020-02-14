from neuronpp.core.cells.core_cell import CoreCell
from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper
from neuronpp.core.hocwrappers.seg import Seg


class Sec(HocWrapper):
    def __init__(self, obj, parent: CoreCell, name):
        HocWrapper.__init__(self, hoc_obj=obj, parent=parent, name=name)

    def __call__(self, loc):
        seg = Seg(obj=self.hoc(loc), parent=self, name="%s(%s)" % (self.name, loc))
        return seg
