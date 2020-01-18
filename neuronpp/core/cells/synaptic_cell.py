from neuronpp.core.cells.netconn_cell import NetConnCell
from neuronpp.core.hocwrappers.composed.synapse import Synapse


class SynapticCell(NetConnCell):
    def __init__(self, name=None):
        NetConnCell.__init__(self, name)
        self.syns = []

    def filter_synapse(self, mod_name: str, name, source=None, point_process=None):
        """
        All name must contains index of the point process of the specific type.
        eg. head[0][0] where head[0] is name and [0] is index of the point process of the specific type.

        :param mod_name:
            single string defining name of point process type name, eg. concere synaptic mechanisms like Syn4PAChDa
        :param name:
            start with 'regex:any pattern' to use regular expression. If without 'regex:' - will look which Hoc objects contain the str
        :param source:
            string of source compound name (if source is provided)
        :param point_process:
            string of point process compound name
        :return:
        """
        return self.filter(self.syns, mod_name=mod_name, name=name, source=source, point_process=point_process)

    def make_sypanses(self, source, weight, tag: str = None, mod_name: str = None, sec=None, loc=0.0, delay=0, **synaptic_params):

        pps = self.make_point_processes(tag=tag, mod_name=mod_name, sec=sec, loc=loc, **synaptic_params)
        nns = self.make_netcons(source=source, weight=weight, mod_name=mod_name, point_process=pps, delay=delay)

        result = []
        for i, (p, n) in enumerate(zip(pps, nns)):
            syn = Synapse(source, point_process=p, netconn=n, parent_cell=self, name=str(i))
            self.syns.append(syn)
            result.append(syn)

        return result
