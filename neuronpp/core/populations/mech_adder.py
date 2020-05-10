from typing import Union

from neuronpp.core.distributions import Dist
from neuronpp.core.populations.params.netcon_params import NetconParams
from neuronpp.core.populations.params.spine_params import SpineParams


class SynAdder:
    def __init__(self, mod_name):
        self.mod_name = mod_name

        self._netcon_params = []
        self._spine_params = None
        self._synaptic_params = {}

    def add_netcon(self, weight: Union[float, Dist] = 1.0, delay: Union[float, Dist] = 1,
                   threshold: Union[float, Dist] = 10):
        """
        :param weight:
            default is 1.0
        :param delay:
            default is 1
            delay in ms
        :param threshold:
            default is 10
            threshold in mV
        """
        ncp = NetconParams(weight=weight, delay=delay, threshold=threshold)
        self._netcon_params.append(ncp)
        return self

    def add_synaptic_params(self, **kwargs):
        """
        kwargs for MOD PointProcess parameters
        """
        self._synaptic_params.update(kwargs)
        return self

    def spine_params(self, head_nseg: Union[int, Dist] = 2, neck_nseg: Union[int, Dist] = 2):
        """
        :param head_nseg:
            number of segments for head of the spine
        :param neck_nseg:
            number of segments for neck of the spine
        """
        self._spine_params = SpineParams(head_nseg=head_nseg, neck_nseg=neck_nseg)
        return self