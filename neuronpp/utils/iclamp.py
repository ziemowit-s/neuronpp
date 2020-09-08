from neuron import h
from neuron.units import ms

from neuronpp.core.decorators import distparams
from neuronpp.core.hocwrappers.seg import Seg
from neuronpp.core.neuron_removable import NeuronRemovable


class IClamp(NeuronRemovable):
    def __init__(self, segment: Seg):
        if not isinstance(segment, Seg):
            raise TypeError("Param 'segment' must be a Seg object, eg. soma(0.5).")

        self._segment = segment
        self.iclamps = []

    @distparams
    def stim(self, delay, dur, amp):
        """
        All IClamp stims must be setup before any run.

        Each default units can be override by the user eg. stim(delay=20*um, ...)
        :param delay:
            by default in ms
        :param dur:
            by default in ms
        :param amp:
            by default in nA
        :return:
        """
        clamp = h.IClamp(self._segment.hoc)
        clamp.delay = delay * ms
        clamp.dur = dur * ms
        clamp.amp = amp
        self.iclamps.append(clamp)
        return clamp
