from neuron import h
from neuron.units import ms

from neuronpp.core.cells.core_cell import CoreCell
from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper


class NetCon(HocWrapper):
    def __init__(self, hoc_obj, name, source: HocWrapper, parent: CoreCell):
        HocWrapper.__init__(self, hoc_obj=hoc_obj, parent=parent, name=name)
        self.source = source

    def make_event(self, time, use_global_sim_time=True):
        """
        Currently it makes events to all NetConns connected to the synapse.
        :param time:
            time in ms of next synaptic event
        :param use_global_sim_time:
            If true it will use global time of hoc simulation (don't need to add h.t or sim.time the the event time)
        """
        if h.t == 0:
            raise ConnectionRefusedError("NetConn cannot make event before running the simulation. "
                                         "Run SimRun at least for 1 ms and then make event.")
        sim_time = time * ms
        if use_global_sim_time:
            sim_time = h.t + sim_time
            self.hoc.event(sim_time)