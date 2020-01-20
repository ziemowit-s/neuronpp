from neuron import h
from neuron.units import ms

from neuronpp.core.hocwrappers.composed.composed_hoc_wrapper import ComposedHocWrapper
from neuronpp.core.hocwrappers.composed.synapse import Synapse


class ComplexSynapse(ComposedHocWrapper, dict):
    def __init__(self, synapses, name, tag=None):
        self.tag = tag
        self.mod_name = '+'.join([s.mod_name for s in synapses])

        parent = None
        for s in synapses:
            if not isinstance(s, Synapse):
                raise TypeError("All synapses must be of type hocwrappers.Synapse, but one of provided object was of type '%s'" % type(s))
            if parent is None:
                parent = s.parent
            else:
                if s.parent != parent:
                    raise TypeError("All synapses must have same parent element inside a single ComplexSynapse, "
                                    "but the parent of the first element was '%s' and of the second '%s'" % (parent, s.parent))
            self[s.mod_name] = s

        ComposedHocWrapper.__init__(self, parent=parent, name=name)

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

        for syn in self.values():
            syn.netconn.hoc.event(sim_time)

    def __repr__(self):
        synapses_in = '+'.join(self.keys())
        return "{}[{}]+{}".format(self.parent, self.__class__.__name__, synapses_in)
