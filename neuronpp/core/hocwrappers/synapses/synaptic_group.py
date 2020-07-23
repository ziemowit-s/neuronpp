from typing import List, Optional, Dict

from neuronpp.core.hocwrappers.netcon import NetCon
from neuronpp.core.decorators import non_removable_fields
from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper
from neuronpp.core.hocwrappers.synapses.synapse import Synapse
from neuronpp.core.hocwrappers.group_hoc_wrapper import GroupHocWrapper
from neuronpp.core.hocwrappers.synapses.single_synapse import SingleSynapse


@non_removable_fields("target")
class SynapticGroup(GroupHocWrapper, Synapse):
    def __init__(self, synapses: List[SingleSynapse], name: str, tag: Optional[str] = None):
        """
        It is a dictionary containing Single Synapses where key is point_process name of the 
        synapse of the same type, eg. self["ExpSyn"] = list(syn1, syn2, syn3)

        All synapses in the group need to have a single target

        It not derives from the HocWrapper because HocWrapper is a wrapper for a single HOC object

        :param synapses:
            list of Single Synapses.
            All synapses need to have the same parent object.
        :param name:
            string name for the group
        :param tag:
            string tag which will be attached to the synaptic group as tag.
            you can filter by this tag
        """
        self.tag = tag
        self.mod_name = '_'.join([s.point_process_name for s in synapses])
        name = "%s[%s]" % (self.mod_name, name)

        GroupHocWrapper.__init__(self, objs=synapses, name=name,
                                 key_func=lambda s: s.point_process_name)

        parent = None
        for o in synapses:
            if not isinstance(o, HocWrapper):
                raise TypeError("All objects must derived from HocWrapper")
            if parent is None:
                parent = o.parent
            else:
                if o.parent.name != parent.name:
                    raise TypeError("All objects must have the same parent.")

        self.parent = parent
        self.target = self.parent

    @property
    def sources(self) -> Dict[str, List[SingleSynapse]]:
        """
        Returns dictionary where key is point_process name and value is list of SingleSynapse
        """
        return dict([(pp_name, syn.sources) for pp_name, syn_list in self.items()
                     for syn in syn_list])

    @property
    def netcons(self) -> Dict[str, List[SingleSynapse]]:
        """
        Returns dictionary where key is point_process name and value is list of NetCon
        """
        return dict([(pp_name, syn.netcons) for pp_name, syn_list in self.items()
                     for syn in syn_list])

    def make_event(self, time, use_global_sim_time=True):
        """
        Make stimulation of all NetCons in all synapses.

        :param time:
            time in ms of the simulational event
        :param use_global_sim_time:
            If true it will use global time of hoc simulation (don't need to add h.t or sim.time
            the the event time)
        """
        for syn_list in self.values():
            for syn in syn_list:
                syn.make_event(time, use_global_sim_time)

    def add_netcon(self, source: Optional[HocWrapper], weight: float = 1.0, delay: float = 1.0,
                   threshold: float = 10) -> Dict[str, List[NetCon]]:
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
        :return
            dictionary of all created NetCons for all synapses, where key is the key of each Synapse
        """
        result = {}
        for key, syn_list in self.items():
            result[key] = []
            for syn in syn_list:
                nc = syn.add_netcon(source, weight, delay, threshold)
                result[key].append(nc)
        return result

    def __repr__(self):
        synapses_in = '+'.join(self.keys())
        return "{}[{}][{}]".format(self.parent, self.__class__.__name__, synapses_in)
