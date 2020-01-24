from neuron import h
from neuron.units import ms
from nrn import Segment


class IClamp:
    def __init__(self, segment: Segment):
        if not isinstance(segment, Segment):
            raise TypeError("Segment must be a valid NEURON segment with location defined, eg. soma(0.5).")

        self._segment = segment
        self.iclamps = []

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
        clamp = h.IClamp(self._segment)
        clamp.delay = delay * ms
        clamp.dur = dur * ms
        clamp.amp = amp
        self.iclamps.append(clamp)