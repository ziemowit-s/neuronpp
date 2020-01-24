import random

from neuron import h
from neuron.units import ms
from neuronpp.core.cells.utils import make_netconn

from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper
from neuronpp.core.hocwrappers.sec import Sec

from neuronpp.core.hocwrappers.composed.composed_hoc_wrapper import ComposedHocWrapper
from neuronpp.core.hocwrappers.netconn import NetConn
from neuronpp.core.hocwrappers.point_process import PointProcess


class Synapse(ComposedHocWrapper):
    def __init__(self, source, point_process: PointProcess, netconn: NetConn, parent_sec: Sec, name, tag=None):
        ComposedHocWrapper.__init__(self, parent=parent_sec, name=name)

        self.hoc = point_process.hoc
        self.tag = tag
        self.source = source
        self.netconn = netconn
        self.point_process = point_process
        self.mod_name = point_process.mod_name

    def make_event(self, time, use_global_sim_time=True):
        """
        :param time:
            time in ms of next synaptic event
        :param use_global_sim_time:
            If true it will use global time of hoc simulation (don't need to add h.t or sim.time the the event time)
        """
        sim_time = time * ms
        if use_global_sim_time:
            sim_time = h.t + sim_time
        self.netconn.hoc.event(sim_time)

    def set_source(self, source: HocWrapper, source_loc=None, weight=1.0, rand_weight=False, delay=1.0, threshold=10):
        """
        :param source:
            Can be only: hocwrappers.NetStim, hocwrappers.VecStim, hocwrappers.Sec or None. If it is Sec also loc param need to be defined.
            If remain None it will create NetConn with no source, which can be use as external event source
        :param source_loc:
            if source is type of hocwrapper.Sec - source_loc need to be between 0-1, otherwise must remain None.
        :param weight:
        :param rand_weight:
            if True, will find rand weight [0,1) and multiply this by weight.
        :param delay:
            in ms
        :param threshold:
            threshold for NetConn, default=10
        """
        self.source = source
        self.netconn = make_netconn(parent=self.parent, source=source, target=self.point_process, ref_variable='v',
                                    source_loc=source_loc, delay=delay, weight=weight, rand_weight=rand_weight,
                                    threshold=threshold)

    def __repr__(self):
        return "{}[{}]{}+{}".format(self.parent, self.__class__.__name__, self.netconn, self.name)
