import nrn
from numpy import pi

from neuronpp.core.hocwrappers.seg import Seg
from neuronpp.core.cells.core_cell import CoreCell
from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper


class Sec(HocWrapper):
    def __init__(self, obj: nrn.Section, cell: CoreCell, name: str):
        """
        Create wrapper for the Section object from HOC.

        Parent is not defined since it is provided as a property method which looks for the parent
        on the neuron's tree.
        :param obj:
            HOC's Section object
        :param cell:
            Cell where the section is located
        :param name:
            string name of the section
        """
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
        return Seg(obj=hoc_seg, parent=self)
