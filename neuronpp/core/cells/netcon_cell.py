import numpy as np
from neuron import h
from nrn import Segment

from neuronpp.core.cells.utils import get_default
from neuronpp.core.hocwrappers.netcon import NetCon
from neuronpp.core.hocwrappers.point_process import PointProcess
from neuronpp.core.hocwrappers.vecstim import VecStim
import matplotlib.pyplot as plt
from collections import defaultdict

from neuronpp.core.hocwrappers.netstim import NetStim
from neuronpp.core.cells.point_process_cell import PointProcessCell


class NetConCell(PointProcessCell):
    def __init__(self, name=None, compile_paths=None):
        PointProcessCell.__init__(self, name, compile_paths=compile_paths)
        self.ncs = []
        self._spike_detector = None
        self._nc_num = defaultdict(int)

    def filter_netcons(self, mod_name: str, name: str, obj_filter=None, **kwargs):
        """
        Currently all filter passed are treated as AND statements.

        * Whole object callable function passed to the obj_filter param.
            eg. (lambda expression) returns sections which name contains 'apic' or their distance > 1000 um from the soma:
          ```
           soma = cell.filter_secs("soma")
           cell.filter_secs(obj_filter=lambda o: 'apic' in o.name or h.distance(soma(0.5), o(0.5)) > 1000)
          ```

        * Single object field filter based on callable function passed to the obj_filter param.
          eg. (lambda expression) returns sections which parent's name contains less than 10 characters
          ```
          cell.filter_secs(parent=lambda o: len(o.parent.name) < 10)
          ```

        :param mod_name:
            single string defining name of target point process type name, eg. concere synaptic mechanisms like Syn4PAChDa
        :param obj_filter:
            Whole object callable functional filter. If you added also any kwargs they will be together with the
            obj_filter treated as AND statement.
        :param name:
            start with 'regex:any pattern' to use regular expression. If without 'regex:' - will look which Hoc objects contain the str
        :return:
        """
        return self.filter(searchable=self.ncs, obj_filter=obj_filter, mod_name=mod_name, name=name, **kwargs)

    def add_netcon(self, source, point_process, weight=1, rand_weight=False, delay=0, threshold=10):
        """
        :param source:
            NetStim, VecStim, HOC's Section or None. If it is Sec also loc param need to be defined.
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
        source = get_default(source)
        if source is not None and not isinstance(source, (NetStim, VecStim, Segment)):
            raise TypeError("Param 'source' can be NetStim, VecStim, Segment, Section (Sec or HOC's Section) or None, "
                            "but provided %s" % source.__class__)

        conn, name = self._make_netcon(source=source, point_process=point_process, weight=weight,
                                       rand_weight=rand_weight, delay=delay, threshold=threshold)
        self.ncs.append(conn)
        self._nc_num[name] += 1
        return conn

    def _make_netcon(self, source, point_process, ref_variable: str = 'v',
                     delay=1.0, weight=1.0, rand_weight=None, threshold=10):
        """
        :param source:
            NetStim, VecStim, HOC's Section or None. If None it will create a NetConn without the source.
        :param point_process:
            PointProcess object. If None - will create NetConn without target, it is used as a spike detector.
        :param ref_variable:
            Name of the variable which is reference to pass to the NetConn. In most cases it is voltage 'v'.
            If the source is NetStim or VecStim is the ref_variable is not used.
        :param delay:
        :param weight:
        :param rand_weight:
            Truncated normal distribution (only positive) with mu=weight, sigma=weight
        :param threshold:
        :return:
        """
        if rand_weight:
            current_weight = np.abs(np.random.normal(weight, weight, 1)[0])
        else:
            current_weight = weight

        if point_process is not None:
            if not isinstance(point_process, PointProcess):
                raise TypeError("target can be only None or type of PointProcess, but provided: %s"
                                % point_process.__class__.__name__)
            point_process = point_process.hoc

        if source is None:
            con = h.NetCon(None, point_process)
        else:
            if isinstance(source, (NetStim, VecStim)):
                con = h.NetCon(source.hoc, point_process)

            else:
                source_ref = getattr(source, "_ref_%s" % ref_variable)
                con = h.NetCon(source_ref, point_process, sec=source.sec)

        if delay:
            con.delay = delay
        if weight:
            con.weight[0] = current_weight
        if threshold:
            con.threshold = threshold

        name = "%s->%s" % (source, point_process)
        con = NetCon(con, source=source, parent=self, name=name)
        return con, name

    def make_spike_detector(self, segment):
        """
        :param segment:
            If Sec or HOC Section, default loc is 0.5
        :return:
        """
        segment = get_default(segment)
        if not isinstance(segment, Segment):
            raise TypeError("Param 'segment' can be only Sec, HOC's: Segment or Section.")

        # source, point_process, weight, rand_weight=False, delay=0, threshold=10
        nc_detector = self.add_netcon(source=segment, point_process=None)
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