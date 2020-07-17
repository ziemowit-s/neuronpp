from neuronpp.core.hocwrappers.sec import Sec
from neuronpp.core.cells.section_cell import SectionCell
from neuronpp.core.hocwrappers.sec_group import SecGroup
from neuronpp.core.decorators import non_removable_fields


@non_removable_fields("cell")
class Spine(SecGroup):
    def __init__(self, head: Sec, neck: Sec, cell: SectionCell, name):
        """
        Wrapper for the spine which contains head and neck sections.

        The connection of the head and the neck is done here in the constructor.

        Parent is not defined since it is provided as a property method which looks for the parent
        on the neuron's tree.

        :param head:
            section of the head
        :param neck:
            section of the neck
        :param cell:
            cell where those sections exists
        :param name:
            name of the spine
        """
        cell.connect_secs(child=head, parent=neck, child_loc=0.0, parent_loc=1.0)
        self.head = head
        self.neck = neck
        self.cell = cell
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
