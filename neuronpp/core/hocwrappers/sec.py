
import nrn
from numpy import pi
from typing import Optional

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
        self.add_non_removable_field("cell")

        self.cell = cell
        HocWrapper.__init__(self, hoc_obj=obj, parent=None, name=name)

    @property
    def parent(self):
        """
        Returns parent Section or None if there is no parent.
        """
        parent_seg = self.hoc.parentseg()
        if parent_seg:
            hoc_sec = parent_seg.sec
            return Sec(hoc_sec, cell=self.cell, name=hoc_sec.name())
        else:
            return None

    @property
    def area(self) -> float:
        """
        Returns total area of the Section
        """
        return pi*self.hoc.L*self.hoc.diam

    @property
    def orientation(self) -> float:
        """
        Return the end (0 or 1) which connects to the parent. This is the value, y, used:
            * In Neuron++ SectionCell: cell.connect_secs(child, parent, x, y)
            * In NEURON child.connect(parent(x), y)
        """
        return self.hoc.orientation()

    @property
    def parent_loc(self) -> Optional[float]:
        """
        Returns location on parent that child is connected to. (0 <= x <= 1).
        This information is also available via: self.hoc.parentseg().x

        If the section has no parent it will return None
        """
        parent = self.hoc.parentseg()
        if parent:
            return parent.x
        else:
            return None

    def __call__(self, loc) -> Seg:
        hoc_seg = self.hoc(loc)
        return Seg(obj=hoc_seg, parent=self)
