from neuron.rxd import rxd

from neuronpp.core.cells.rxd_tools import RxDTool
from neuronpp.core.cells.section_cell import SectionCell
from neuronpp.core.hocwrappers.rxd import RxD


class RxDCell(SectionCell):
    def __init__(self, name=None, compile_paths=None):
        """
        :param name:
            Name of the cell
        """
        SectionCell.__init__(self, name, compile_paths=compile_paths)
        self.rxds = []

    def make_rxd(self, rxd_obj: RxDTool, sec=None, is_3d=False, threads=1, dx_3d_size=None):
        """
        :param rxd_obj:
            RxD Object from RxDTools. It defines RxD structure.
            Each RxD need to implement first RxDTool object and then be passed to this function to implement.
        :param sec:
            start with 'regex:any pattern' to use regular expression. If without 'regex:' - will look which Hoc objects contain the str
        :param is_3d:
        :param threads:
        :param dx_3d_size:
        """
        r = RxD(rxd_obj, parent=self, name=rxd_obj.__class__.__name__)
        self.rxds.append(r)

        if isinstance(sec, str) or sec is None:
            sec = self.filter_secs(name=sec)

        if is_3d:
            rxd.set_solve_type(sec, dimension=3)
        rxd.nthread(threads)

        rxd_obj.load(sec, dx_3d_size=dx_3d_size, rxds=self.rxds)

    def __del__(self):
        SectionCell.__del__(self)
        for r in self.rxds:
            # recommended way to delete section in Python wrapper
            r.hoc = None
            del r
