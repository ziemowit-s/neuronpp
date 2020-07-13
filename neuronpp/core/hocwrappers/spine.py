from neuronpp.core.hocwrappers.sec import Sec
from neuronpp.core.cells.section_cell import SectionCell
from neuronpp.core.hocwrappers.sec_group import SecGroup


class Spine(SecGroup):
    def __init__(self, head: Sec, neck: Sec, cell: SectionCell, name):
        """
        Wrapper for the spine which contains head and neck sections.

        The connection of the head and the neck is done here in the constructor.

        :param head:
            section of the head
        :param neck:
            section of the neck
        :param cell:
            cell where those sections exists
        :param name:
            name of the spine
        """
        cell.connect_secs(source=head, target=neck)
        self.head = head
        self.neck = neck
        SecGroup.__init__(self, secs=[head, neck], name=name)

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
        return self.head, self.neck
