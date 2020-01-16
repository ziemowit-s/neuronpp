from neuronpp.core.cells.netconn_cell import NetConnCell
from neuronpp.core.hocwrappers.composed.synapse import Synapse


class SynapticCell(NetConnCell):
    def __init__(self, name):
        NetConnCell.__init__(self, name)
        self.syns = []

    def make_sypanse(self, source, weight, tag: str = None, mod_name: str = None, sec=None, loc=0.0, delay=0):
        """

        :param source:
        :param weight:
        :param tag:
            custom name
        :param mod_name:
        :param sec:
        :param loc:
        :param delay:
        :return:
        """
        pps = self.make_point_processes(tag=tag, mod_name=mod_name, sec=sec, loc=loc)
        nns = self.make_netcons(source=source, weight=weight, mod_name=mod_name, point_process=pps, delay=delay)

        result = []
        for i, (p, n) in enumerate(zip(pps, nns)):
            syn = Synapse(source, point_process=p, netconn=n, parent_cell=self, name=str(i))
            self.syns.append(syn)
            result.append(syn)

        return result
