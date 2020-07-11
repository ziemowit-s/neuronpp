from neuronpp.core.hocwrappers.sec import Sec
from neuronpp.core.cells.section_cell import SectionCell
from neuronpp.core.hocwrappers.wrapper import Wrapper


class Spine(Wrapper):
    def __init__(self, head: Sec, neck: Sec, cell: SectionCell, name):
        """
        Wrapper for the spine which contains head and neck sections.

        It not derives from the HocWrapper because HocWrapper is a wrapper for a single HOC object

        :param head:
            section of the head
        :param neck:
            section of the neck
        :param cell:
            cell where those sections exists
        :param name:
            name of the spine
        """
        Wrapper.__init__(self, parent=None, name=name)
        self.cell = cell
        cell.connect_secs(source=head, target=neck)
        self.hoc_objs = [neck.hoc, head.hoc]
        self.head = head
        self.neck = neck

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
