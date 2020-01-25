import numpy as np
from neuron import h
from neuronpp.core.hocwrappers.netconn import NetConn

from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper
from neuronpp.core.hocwrappers.point_process import PointProcess

from neuronpp.core.hocwrappers.sec import Sec

from neuronpp.core.hocwrappers.vecstim import VecStim

from neuronpp.core.hocwrappers.netstim import NetStim


def get_netstim(start, number, interval, noise):
    stim = h.NetStim()
    stim.start = start
    stim.number = number
    stim.interval = interval
    stim.noise = noise
    return stim


def get_vecstim(ping_array):
    stim = h.VecStim()
    vec = h.Vector(ping_array)
    stim.play(vec)

    return stim, vec


def make_netconn(parent, source: HocWrapper = None, target: PointProcess = None, ref_variable: str = 'v', source_loc: float = None,
                 delay=1.0, weight=1.0, rand_weight=None, threshold=10):
    """
    :param source:
        NetStim, VecStim or Sec. If None it will create a NetConn without the source.
    :param target:
        PointProcess object. If None - will create NetConn without target, it is used as a spike detector.
    :param ref_variable:
        Name of the variable which is reference to pass to the NetConn. In most cases it is voltage 'v'.
        If the source is NetStim or VecStim is the ref_variable is not used.
    :param source_loc:
        Loc on the Sec. If source is NetStim or VecStim it must remain None.
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

    if target is not None:
        if not isinstance(target, PointProcess):
            raise TypeError("target can be only None or type of PointProcess, but provided: %s"
                            % target.__class__.__name__)
        target = target.hoc

    if source is None:
        con = h.NetCon(None, target)
    else:
        if isinstance(source, (NetStim, VecStim)):
            if source_loc is not None:
                raise ValueError("If source is type of NetStim or VecStim you must remain 'source_loc' param None.")
            con = h.NetCon(source.hoc, target)

        elif isinstance(source, Sec):
            if source_loc is None:
                raise ValueError("If source is type of Sec you need to specify 'source_loc' param.")

            source_ref = getattr(source.hoc(source_loc), "_ref_%s" % ref_variable)
            con = h.NetCon(source_ref, target, sec=source.hoc)

        else:
            raise TypeError("Source can be only type of None, NetStim, VecStim or Sec, but provided: %s" %
                            source.__class__.__name__)

    if delay:
        con.delay = delay
    if weight:
        con.weight[0] = current_weight
    if threshold:
        con.threshold = threshold

    name = "%s->%s" % (source, target)
    con = NetConn(con, parent=parent, name=name)
    return con, name
