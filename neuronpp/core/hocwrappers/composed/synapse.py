from neuron import h
from neuron.units import ms
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

    def __repr__(self):
        return "{}[{}]{}+{}".format(self.parent, self.__class__.__name__, self.netconn, self.name)
