from neuron import h

from neuronpp.core.hocwrappers.netcon import NetCon
from neuronpp.core.hocwrappers.point_process import PointProcess
from neuronpp.core.hocwrappers.seg import Seg
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
           cell.filter_secs(obj_filter=lambda o: 'apic' in o.name or h.distance(soma.hoc(0.5), o.hoc(0.5)) > 1000)
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

    def add_netcon(self, source, point_process, netcon_weight=1, delay=0, threshold=10):
        """
        :param source:
            NetStim, VecStim, Seg or None.
            If remain None it will create NetConn with no source, which can be use as external event source
        :param netcon_weight:
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
        if source is not None and not isinstance(source, (NetStim, VecStim, Seg)):
            raise TypeError("Param 'source' can be NetStim, VecStim, Seg or None, "
                            "but provided %s" % source.__class__)

        conn, name = self._make_netcon(source=source, point_process=point_process, netcon_weight=netcon_weight, delay=delay, threshold=threshold)
        self.ncs.append(conn)
        self._nc_num[name] += 1
        return conn

    def _make_netcon(self, source, point_process, ref_variable: str = 'v',
                     delay=1.0, netcon_weight=1.0, threshold=10):
        """
        :param source:
            NetStim, VecStim, HOC's Section or None. If None it will create a NetConn without the source.
        :param point_process:
            PointProcess object. If None - will create NetConn without target, it is used as a spike detector.
        :param ref_variable:
            Name of the variable which is reference to pass to the NetConn. In most cases it is voltage 'v'.
            If the source is NetStim or VecStim is the ref_variable is not used.
        :param delay:
        :param netcon_weight:
        :param threshold:
        :return:
        """
        hoc_pp = None
        if point_process is not None:
            if not isinstance(point_process, PointProcess):
                raise TypeError("target can be only None or type of PointProcess, but provided: %s"
                                % point_process.__class__.__name__)
            hoc_pp = point_process.hoc

        if source is None:
            con = h.NetCon(None, hoc_pp)
        else:
            if isinstance(source, (NetStim, VecStim)):
                con = h.NetCon(source.hoc, hoc_pp)

            elif isinstance(source, Seg):
                source_ref = getattr(source.hoc, "_ref_%s" % ref_variable)
                con = h.NetCon(source_ref, hoc_pp, sec=source.hoc.sec)
            else:
                raise TypeError("Source can only be NetStim, VecStim or Seg, but provided type of: %s" % source.__class__)

        if delay:
            con.delay = delay
        if netcon_weight:
            con.weight[0] = netcon_weight
        if threshold:
            con.threshold = threshold

        name = "%s->%s" % (source, point_process)
        con = NetCon(con, source=source, target=point_process, parent=self, name=name)
        return con, name

    def make_spike_detector(self, segment):
        """
        :param segment:
        """
        if not isinstance(segment, Seg):
            raise TypeError("Param 'segment' can be only a Seg object.")
        if self._spike_detector is not None:
            raise RuntimeError("Spike detector has been created already for the cell %s, "
                               "you can't create another one." % self.name)

        nc_detector = self.add_netcon(source=segment, point_process=None)
        nc_detector.name = "SpikeDetector[%s]" % self.name

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