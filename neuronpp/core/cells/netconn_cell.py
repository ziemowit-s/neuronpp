from neuron import h
from neuron.hoc import HocObject
from nrn import Segment
import matplotlib.pyplot as plt
from collections import defaultdict

from neuronpp.core.hocwrappers.sec import Sec
from neuronpp.core.cells.utils import make_conn
from neuronpp.core.hocwrappers.netconn import NetConn
from neuronpp.core.hocwrappers.netstim import NetStim
from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper
from neuronpp.core.cells.point_process_cell import PointProcessCell


class NetConnCell(PointProcessCell):
    def __init__(self, name=None):
        PointProcessCell.__init__(self, name)
        self.ncs = []
        self._spike_detector = None
        self._nc_num = defaultdict(int)

    def filter_netcons(self, mod_name: str, name: str):
        """
        :param mod_name:
            single string defining name of target point process type name, eg. concere synaptic mechanisms like Syn4PAChDa
        :param name:
            start with 'regex:any pattern' to use regular expression. If without 'regex:' - will look which Hoc objects contain the str
        :return:
        """
        return self.filter(searchable=self.ncs, mod_name=mod_name, name=name)

    def make_netcons(self, source: HocWrapper, weight, point_process=None, mod_name: str = None, delay=0):
        """
        All name must contains index of the point process of the specific type.
        eg. head[0][0] where head[0] is name and [0] is index of the point process of the specific type.

        :param source:
            Can be only hocwrappers.NetStim, h.Segment, or None.
            If None it will create NetConn with no source, which can be use as external event source
        :param weight:
        :param mod_name:
            single string defining name of point process type name, eg. concrete synaptic mechanisms like Syn4PAChDa
            If None - it assumes that point_process has list of point processes objects
        :param point_process:
            start with 'regex:any pattern' to use regular expression. If without 'regex:' - will look which Hoc objects contain the str
        :param delay:
        return:
            A list of added NetConns.
        """
        if source is not None:
            if not isinstance(source, (NetStim, HocObject)) and 'pointer to hoc scalar' not in str(source._ref_v):
                raise TypeError("Param 'source' can be only hocwrappers.NetStim, pointer to variable (eg. source._ref_v) or None. "
                                "But provided type was %s instead." % type(source))

        if point_process is None and mod_name is None:
            raise LookupError("If point_process is None you need to provide mod_name string param.")

        if isinstance(point_process, str) or point_process is None:
            if mod_name is None:
                raise LookupError("If point_process is str you need to provide mod_name string param.")
            point_process = self.filter_point_processes(mod_name=mod_name, name=point_process)

        results = []
        for pp in point_process:
            conn, name = self._make_netconn(source=source, point_process=pp, weight=weight, delay=delay)
            results.append(conn)

            self.ncs.append(conn)
            self._nc_num[name] += 1

        return results

    def make_spike_detector(self, sec="soma", loc=0.5):
        """
        :param sec:
            The name of the section where spike detector will be set. Default is 'soma'.
        :param loc:
            Location on the sec where spike detector will be set. Default is 0.5
        :return:
        """
        if isinstance(sec, str):
            sec = self.filter_secs(sec)
            if len(sec) != 1:
                raise IndexError("If 'sec' is string, filter must return exactly single element, but returned %s for filter: '%s'"
                                 % (len(sec), sec))
            sec = sec[0]

        if not isinstance(sec, Sec):
            raise TypeError("Param 'sec' must be a type of hocwrappers.sec.Sec after string filter find or as explicite param.")

        segment = sec.hoc(loc)
        nc_detector, name = self._make_netconn(source=segment._ref_v, point_process=None)
        nc_detector.name = self.name

        result_vector = h.Vector()
        nc_detector.hoc.record(result_vector)
        self._spike_detector = (nc_detector, result_vector)

    def get_spikes(self):
        """
        :return:
            spikes array of time in ms when spikes occures.
        """
        if self._spike_detector is None:
            raise LookupError("Spike detector have not been setup before run. call cell.make_spike_detector() function before.")
        spikes = self._spike_detector[1].as_numpy()
        return spikes

    def plot_spikes(self):
        spikes = self.get_spikes()
        fig, ax = plt.subplots(1)

        ax.set_title("Spike detector of %s" % self.name)
        ax.vlines(spikes, 0, 1)
        ax.set(xlabel='t (ms)', ylabel="spikes")

    def _make_netconn(self, source, point_process, weight=None, delay=None):
        if isinstance(source, HocWrapper):
            source = source.hoc
        if point_process is not None:
            point_process = point_process.hoc

        conn_hoc = make_conn(source=source, target=point_process, delay=delay, weight=weight)
        name = "%s->%s" % (source, point_process)
        conn = NetConn(conn_hoc, parent=self, name=name)
        return conn, name