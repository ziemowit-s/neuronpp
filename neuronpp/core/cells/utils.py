import numpy as np
from neuron import h
from nrn import Section
from neuronpp.core.hocwrappers.netcon import NetCon

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


def get_default(seg):
    if isinstance(seg, (Sec, Section)):
        seg = seg.hoc(0.5)
    return seg
