import abc
from typing import Optional, Union, List, Dict

from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper
from neuronpp.core.hocwrappers.netcon import NetCon


class Synapse:

    @abc.abstractmethod
    def make_event(self, time, use_global_sim_time=True):
        """
        Currently it makes events to all NetConns connected to the synapse.

        :param time:
            time in ms of the simulational event
        :param use_global_sim_time:
            If true it will use global time of hoc simulation
            (don't need to add h.t or sim.time the the event time)
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def add_netcon(self, source: Optional[HocWrapper], weight: float = 1.0, delay: float = 1.0,
                   threshold: float = 10) -> Union[NetCon, Dict[str, List[NetCon]]]:
        """
        Currently it allows to add single new source
        :param source:
            Can be only: hocwrappers.NetStim, hocwrappers.VecStim, hocwrappers.Sec or None.
            If it is Sec also loc param need to be defined.
            If remain None it will create NetConn with no source, which can be use as external
            event source
        :param weight:
        :param delay:
            in ms
        :param threshold:
            threshold for NetConn, default=10
        :return
            Created NetCon or list of NetCons
        """
        raise NotImplementedError()
