from neuron import h
from neuron.units import ms

from neuronpp.core.cells.core_cell import CoreCell
from neuronpp.core.decorators import non_removable_fields
from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper
from neuronpp.core.hocwrappers.point_process import PointProcess


@non_removable_fields("sources", "target")
class NetCon(HocWrapper):
    def __init__(self, hoc_obj, name, source: HocWrapper, target: PointProcess, parent: CoreCell):
        HocWrapper.__init__(self, hoc_obj=hoc_obj, parent=parent, name=name)
        self.source = source
        self.target = target

    def make_event(self, time, use_global_sim_time=True, use_delay=True):
        """
        Make stimulation of NetCon.

        :param time:
            time in ms of the simulational event
        :param use_global_sim_time:
            If true it will use global time of hoc simulation
            (don't need to add h.t or sim.time the the event time)
        :param use_delay:
            If true use delay (ms) defined for the NetCon while creation
        """
        if h.t == 0:
            raise ConnectionRefusedError("NetConn cannot make event before running the simulation. "
                                         "Run SimRun at least for 1 ms and then make event or"
                                         "warmup_on_create=True on construct of Simulation object.")
        sim_time = time * ms
        if use_delay:
            sim_time += self.hoc.delay
        if use_global_sim_time:
            sim_time = h.t + sim_time
        self.hoc.event(sim_time)

    def get_weight(self):
        return self.hoc.weight[0]

    def set_weight(self, weight):
        self.hoc.weight[0] = weight
