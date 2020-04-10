import nrn

from neuronpp.core.hocwrappers.sec import Sec
from neuronpp.core.cells.section_cell import SectionCell
from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper


class Spine:
    def __init__(self, head: Sec, neck: Sec, cell: SectionCell, name):
        self.cell = cell
        cell.connect_secs(source=head, target=neck)
        self.hoc_objs = [neck.hoc, head.hoc]
        self.head = head
        self.neck = neck
        self.name = name

    @property
    def parent(self):
        parent_seg = self.neck.hoc.parentseg()
        if parent_seg:
            hoc_sec = parent_seg.sec
            return Sec(hoc_sec, cell=self.cell, name=hoc_sec.name())
        else:
            return None

    @property
    def sections(self):
        return (self.head, self.neck)
