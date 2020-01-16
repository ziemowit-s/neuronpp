from neuronpp.core.cells.netconn_cell import NetConnCell
from neuronpp.core.wrappers.composite.synapse import Synapse


class SynapticCell(NetConnCell):
    def __init__(self, name):
        NetConnCell.__init__(self, name)
        self.syns = []

    def make_sypanse(self, source, weight, mod_name: str = None, sec_name: str = None, loc=0.0, delay=0):
        pps = self.make_point_processes(mod_name=mod_name, sec=sec_name, loc=loc)
        nns = self.make_netcons(source=source, weight=weight, mod_name=mod_name, point_process=pps, delay=delay)

        for i, (p, n) in enumerate(zip(pps, nns)):
            syn = Synapse(source, point_process=p, netconn=n, parent_cell=self, name=str(i))
            self.syns.append(syn)
