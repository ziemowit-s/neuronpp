from collections import defaultdict

from neuronpp.core.cells.netstim_cell import NetStimCell

from neuronpp.core.cells.netconn_cell import NetConnCell
from neuronpp.core.hocwrappers.composed.synapse import Synapse


class SynapticCell(NetConnCell):
    def __init__(self, name=None, compile_paths=None):
        NetConnCell.__init__(self, name, compile_paths=compile_paths)
        self.syns = []
        self._syn_num = defaultdict(int)

    def filter_synapses(self, mod_name: str = None, name=None, source=None, point_process=None, parent=None, tag=None,
                        **kwargs):
        """
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
        return self.filter(self.syns, mod_name=mod_name, name=name, source=source, point_process=point_process,
                           parent=parent,
                           tag=tag, **kwargs)

    def add_sypanse(self, source, mod_name: str, sec=None, weight=1, rand_weight=False,
                    delay=0, threshold=10, tag: str = None, **synaptic_params):
        """

        :param source:
            Can be only: hocwrappers.NetStim, hocwrappers.VecStim, hocwrappers.Sec or None. If it is Sec also loc param need to be defined.
            If None it will create NetConn with no source, which can be use as external event source
        :param weight:
        :param rand_weight:
            if True, will find rand weight [0,1) and multiply this by weight.
        :param tag:
        :param mod_name:
        :param sec:
        :param source_loc:
        :param target_loc:
        :param delay:
        :param threshold:
        :param synaptic_params:
        :return:
        """

        pp = self.add_point_process(mod_name=mod_name, sec=sec, tag=tag, **synaptic_params)
        nn = self.add_netcon(source=source, weight=weight, point_process=pp,
                             rand_weight=rand_weight, delay=delay, threshold=threshold)

        syn_name = str(self._syn_num[mod_name])
        syn = Synapse(source, point_process=pp, netconn=nn, parent_sec=pp.parent, name=syn_name, tag=tag)
        self.syns.append(syn)
        self._syn_num[mod_name] += 1

        return syn
