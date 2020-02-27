from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper

from neuronpp.core.hocwrappers.composed.composed_hoc_wrapper import ComposedHocWrapper
from neuronpp.core.hocwrappers.netcon import NetCon
from neuronpp.core.hocwrappers.point_process import PointProcess


class Synapse(ComposedHocWrapper):
    def __init__(self, source, point_process: PointProcess, netcon: NetCon, name, tag=None):
        self.mod_name = point_process.mod_name
        name = "%s[%s]" % (self.mod_name, name)
        ComposedHocWrapper.__init__(self, parent=point_process.parent, name=name)

        self.hoc = point_process.hoc
        self.tag = tag

        self.sources = []
        if source is not None:
            self.sources.append(source)

        self.netcons = []
        if netcon is not None:
            self.netcons.append(netcon)

        self.point_process = point_process
        self.mod_name = point_process.mod_name

    def make_event(self, time, use_global_sim_time=True):
        """
        Currently it makes events to all NetConns connected to the synapse.
        :param time:
            time in ms of next synaptic event
        :param use_global_sim_time:
            If true it will use global time of hoc simulation (don't need to add h.t or sim.time the the event time)
        """
        for nc in self.netcons:
            nc.make_event(time, use_global_sim_time)

    def add_source(self, source: HocWrapper, weight=1.0, delay=1.0, threshold=10):
        """
        Currently it allows to add single new source
        :param source:
            Can be only: hocwrappers.NetStim, hocwrappers.VecStim, hocwrappers.Sec or None. If it is Sec also loc param need to be defined.
            If remain None it will create NetConn with no source, which can be use as external event source
        :param source_loc:
            if source is type of hocwrapper.Sec - source_loc need to be between 0-1, otherwise must remain None.
        :param weight:
        :param delay:
            in ms
        :param threshold:
            threshold for NetConn, default=10
        """
        conn = self.point_process.cell.add_netcon(source=source, point_process=self.point_process, netcon_weight=weight,
                                                  delay=delay, threshold=threshold)
        self.netcons.append(conn)
        if source is not None:
            self.sources.append(source)

    def __repr__(self):
        ncs = '+'.join([str(nc) for nc in self.netcons])
        return "{}[{}]{}+{}".format(self.parent, self.__class__.__name__, ncs, self.name)
