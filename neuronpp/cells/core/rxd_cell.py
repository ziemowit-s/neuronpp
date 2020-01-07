from neuron.rxd import rxd

from neuronpp.cells.core.basic_cell import BasicCell
from neuronpp.cells.core.rxd_tools import RxDTool


class RxDCell(BasicCell):
    def __init__(self, name):
        """
        :param name:
            Name of the cell
        """
        BasicCell.__init__(self, name)
        self.rxds = {}

    def add_rxd(self, rxd_obj: RxDTool, sec_names, is_3d=False, threads=1, dx_3d_size=None):
        """
        :param rxd_obj:
            RxD Object from RxDTools. It defines RxD structure.
            Each RxD need to implement first RxDTool object and then be passed to this function to implement.
        :param is_3d:
        :param threads:
        :param dx_3d_size:
        :param sec_names:
            list of sections or string defining single section name or sections names separated by space
            If None - will takes all sections
        """
        self.rxds[rxd_obj.__class__.__name__] = rxd_obj

        if sec_names is 'all':
            sec_names = self.secs.values()
        else:
            sec_names = self.filter_secs(sec_names=sec_names).values()

        if is_3d:
            rxd.set_solve_type(sec_names, dimension=3)
        rxd.nthread(threads)

        rxd_obj.load(sec_names, dx_3d_size=dx_3d_size, rxds=self.rxds)
