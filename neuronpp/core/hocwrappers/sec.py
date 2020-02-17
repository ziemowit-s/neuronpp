from neuronpp.core.hocwrappers.seg import Seg
from neuronpp.core.cells.core_cell import CoreCell
from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper


class Sec(HocWrapper):
    def __init__(self, obj, parent: CoreCell, name):
        HocWrapper.__init__(self, hoc_obj=obj, parent=parent, name=name)

    def __call__(self, loc):
        hoc_seg = self.hoc(loc)
        return Seg(obj=hoc_seg, parent=self, name="%s(%s)" % (self.name, loc))
