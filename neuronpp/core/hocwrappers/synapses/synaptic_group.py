from neuronpp.core.hocwrappers.wrapper import Wrapper
from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper
from neuronpp.core.hocwrappers.synapses.synapse import Synapse
from neuronpp.core.hocwrappers.synapses.single_synapse import SingleSynapse


class SynapticGroup(Wrapper, Synapse, dict):
    def __init__(self, synapses, name, tag=None):
        self.tag = tag
        self.mod_name = '_'.join([s.mod_name for s in synapses])
        name = "%s[%s]" % (self.mod_name, name)

        parent = None
        for s in synapses:
            if not isinstance(s, SingleSynapse):
                raise TypeError("All synapses must be of type SingleSynapse, "
                                "but one of provided object was of type '%s'" % type(s))
            if parent is None:
                parent = s.parent
            else:
                if s.parent.name != parent.name:
                    raise TypeError(
                        "All synapses must have same parent element inside a single "
                        "ComplexSynapse, but the parent of the first element was '%s' "
                        "and of the second '%s'" % (parent, s.parent))
            self[s.mod_name] = s

        Wrapper.__init__(self, parent=parent, name=name)

    def make_event(self, time, use_global_sim_time=True):
        """
        :param time:
            time in ms of next synaptic event
        :param use_global_sim_time:
            If true it will use global time of hoc simulation (don't need to add h.t or sim.time
            the the event time)
        """
        for syn in self.values():
            syn.make_event(time, use_global_sim_time)

    def add_netcon(self, source: HocWrapper, weight: float = 1.0, delay: float = 1.0,
                   threshold: float = 10):
        """
        This is use on all synapses in this object. If you want to set source only for particular
        subset of synapses,
        get them by complex_synapse['synaptic_mod_name'], where complex_synapse is your object and
        synaptic_mod_name is
        a POINT_PROCESS name of the synapse you want to get. Then perform set_source() function on
        received synapse.

        :param source:
            NetStim, VecStim, HOC's Section or None. If it is Sec also loc param need to be defined.
            If remain None it will create NetConn with no source, which can be use as external
            event source
        :param weight:
        :param delay:
            in ms
        :param threshold:
            threshold for NetConn, default=10
        """
        for s in self.values():
            s.add_netcon(source, weight, delay, threshold)

    def __repr__(self):
        synapses_in = '+'.join(self.keys())
        return "{}[{}][{}]".format(self.parent, self.__class__.__name__, synapses_in)
