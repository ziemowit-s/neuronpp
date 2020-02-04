from neuron import h
from neuronpp.core.hocwrappers.vecstim import VecStim
import matplotlib.pyplot as plt
from collections import defaultdict

from neuronpp.core.hocwrappers.sec import Sec
from neuronpp.core.cells.utils import make_netconn
from neuronpp.core.hocwrappers.netstim import NetStim
from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper
from neuronpp.core.cells.point_process_cell import PointProcessCell


class NetConnCell(PointProcessCell):
    def __init__(self, name=None, compile_paths=None):
        PointProcessCell.__init__(self, name, compile_paths=compile_paths)
        self.ncs = []
        self._spike_detector = None
        self._nc_num = defaultdict(int)

    def filter_netcons(self, mod_name: str, name: str, **kwargs):
        """
        :param mod_name:
            single string defining name of target point process type name, eg. concere synaptic mechanisms like Syn4PAChDa
        :param name:
            start with 'regex:any pattern' to use regular expression. If without 'regex:' - will look which Hoc objects contain the str
        :return:
        """
        return self.filter(searchable=self.ncs, mod_name=mod_name, name=name, **kwargs)

    def make_netcons(self, source: HocWrapper, weight, rand_weight=False, source_loc=None, point_process=None,
                     mod_name: str = None, delay=0, threshold=10):
        """
        :param source:
            Can be only: hocwrappers.NetStim, hocwrappers.VecStim, hocwrappers.Sec or None. If it is Sec also loc param need to be defined.
            If remain None it will create NetConn with no source, which can be use as external event source
        :param weight:
        :param rand_weight:
            if True, will find rand weight [0,1) and multiply this by weight.
        :param source_loc:
            if source is type of hocwrapper.Sec - source_loc need to be between 0-1, otherwise must remain None.
        :param mod_name:
            single string defining name of point process type name, eg. concrete synaptic mechanisms like Syn4PAChDa
            If None - it assumes that point_process has list of point processes objects
        :param point_process:
            start with 'regex:any pattern' to use regular expression. If without 'regex:' - will look which Hoc objects contain the str
        :param delay:
            in ms
        :param threshold:
            threshold for NetConn, default=10
        return:
            A list of added NetConns.
        """
        if source is not None:
            err = False
            if isinstance(source, Sec):
                if source_loc is None or not isinstance(source_loc, (float, int)):
                    err = True
            elif not isinstance(source, (NetStim, VecStim)):
                err = True
            if err:
                raise TypeError("Param 'source' can be only hocwrappers.NetStim, hocwrappers.VecStim, hocwrappers.Sec or None. "
                                "If it is 'Sec', 'source_loc' need to be also provided.\n"
                                "Instead 'source' was of type: '%s' and 'source_loc' has a value of '%s' instead."
                                % (type(source), source_loc))

        if point_process is None and mod_name is None:
            raise LookupError("If point_process is None you need to provide mod_name string param.")

        if isinstance(point_process, str) or point_process is None:
            if mod_name is None:
                raise LookupError("If point_process is str you need to provide mod_name string param.")
            point_process = self.filter_point_processes(mod_name=mod_name, name=point_process)

        results = []

        for pp in point_process:
            conn, name = make_netconn(parent=self, source=source, source_loc=source_loc, target=pp,
                                      weight=weight, rand_weight=rand_weight, delay=delay, threshold=threshold)
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

        nc_detector, name = make_netconn(parent=self, source=sec, source_loc=loc, target=None)
        nc_detector.name = self.name

        result_vector = h.Vector()
        nc_detector.hoc.record(result_vector)
        self._spike_detector = (nc_detector, result_vector)

    def get_spikes(self):
        """
        :return:
            numpy array of time of spikes in ms
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