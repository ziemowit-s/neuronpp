from neuron import h
from neuron.units import ms

from neuronpp.core.cells.cell import Cell
from neuronpp.core.hocwrappers.netconn import NetConn
from neuronpp.core.hocwrappers.point_process import PointProcess


class Synapse:
    def __init__(self, source, point_process: PointProcess, netconn: NetConn, parent_cell: Cell, name):
        self.parent = str(parent_cell)
        self.name = name

        self.source = source
        self.point_process = point_process
        self.netconn = netconn

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
        return "{}[{}]{}_{}".format(self.parent, self.__class__.__name__, self.netconn, self.name)
