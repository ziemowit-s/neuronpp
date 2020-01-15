from neuron.rxd import rxd

from neuronpp.cells.core.section_cell import SectionCell
from neuronpp.cells.core.rxd_tools import RxDTool
from neuronpp.hocs.rxd import RxD


class RxDCell(SectionCell):
    def __init__(self, name):
        """
        :param name:
            Name of the cell
        """
        SectionCell.__init__(self, name)
        self.rxds = []

    def add_rxd(self, rxd_obj: RxDTool, name_filter, regex=False, is_3d=False, threads=1, dx_3d_size=None):
        """
        :param rxd_obj:
            RxD Object from RxDTools. It defines RxD structure.
            Each RxD need to implement first RxDTool object and then be passed to this function to implement.
        :param name_filter:
            If None - will takes all sections
        :param regex:
            If True: pattern will be treated as regex expression, if False: pattern str must be in field str
        :param is_3d:
        :param threads:
        :param dx_3d_size:
        """
        r = RxD(rxd_obj, parent=self, name=rxd_obj.__class__.__name__)
        self.rxds.append(r)

        secs = self.filter_secs(name_filter=name_filter, regex=regex)

        if is_3d:
            rxd.set_solve_type(secs, dimension=3)
        rxd.nthread(threads)

        rxd_obj.load(secs, dx_3d_size=dx_3d_size, rxds=self.rxds)
