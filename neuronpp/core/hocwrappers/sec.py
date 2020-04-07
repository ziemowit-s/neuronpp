from numpy import pi
import nrn

from neuronpp.core.hocwrappers.seg import Seg
from neuronpp.core.cells.core_cell import CoreCell
from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper


class Sec(HocWrapper):
    def __init__(self, obj: nrn.Section, cell: CoreCell, name):
        self.cell = cell
        HocWrapper.__init__(self, hoc_obj=obj, parent=None, name=name)

    @property
    def parent(self):
        parent_seg = self.hoc.parentseg()
        if parent_seg:
            hoc_sec = parent_seg.sec
            return Sec(hoc_sec, cell=self.cell, name=hoc_sec.name())
        else:
            return None

    @property
    def area(self):
        return pi*self.hoc.L*self.hoc.diam

    def __call__(self, loc):
        hoc_seg = self.hoc(loc)
        return Seg(obj=hoc_seg, parent=self, name="%s(%s)" % (self.name, loc))
