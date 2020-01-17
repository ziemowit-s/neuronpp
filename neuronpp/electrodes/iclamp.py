from neuron import h
from neuron.units import ms
from nrn import Segment


class IClamp:
    def __init__(self, segment: Segment):
        if not isinstance(segment, Segment):
            raise TypeError("Segment must be a valid NEURON segment with location defined, eg. soma(0.5).")

        self._clamp = h.IClamp(segment)

    def stim(self, delay, dur, amp):
        """
        Each default units can be override by the user eg. cl.stim(delay=20*um, ...)
        :param delay:
            by default in ms
        :param dur:
            by default in ms
        :param amp:
            by default in nA
        :return:
        """
        self._clamp.delay = delay * ms
        self._clamp.dur = dur * ms
        self._clamp.amp = amp

    @property
    def delay(self):
        return self._clamp.delay

    @property
    def dur(self):
        return self._clamp.dur

    @property
    def amp(self):
        return self._clamp.amp
