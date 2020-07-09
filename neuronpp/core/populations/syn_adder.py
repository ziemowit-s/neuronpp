from typing import Union

from neuronpp.core.distributions import Dist
from neuronpp.core.populations.params.spine_params import SpineParams
from neuronpp.core.populations.params.netcon_params import NetconParams


class SynAdder:
    def __init__(self, point_process_name):
        """
        Create synapse with single Point Process and one or more Netcons.

        :param point_process_name:
            Name of the Point Process defined in MOD file or default Point Process existing
            in NEURON
        """
        self.point_process_name = point_process_name

        self._netcon_params = []
        self._spine_params = None
        self._point_process_params = {}

    def add_netcon(self, weight: Union[float, Dist] = 1.0, delay: Union[float, Dist] = 1,
                   threshold: Union[float, Dist] = 10, **kwargs):
        """
        :param weight:
            default is 1.0
        :param delay:
            default is 1
            delay in ms
        :param threshold:
            default is 10
            threshold in mV
        :param kwargs:
            'custom_source': can be: None or Seg, VecStim, NetStim, or list of Seg, VecStim,
                             NetStim.
                             By default it is not set meaning that default source from Connector
                             will be used.
        """
        ncp = NetconParams(weight=weight, delay=delay, threshold=threshold, **kwargs)
        self._netcon_params.append(ncp)
        return self

    def add_point_process_params(self, **point_process_params):
        """
        :param point_process_params:
            kwargs params for MOD PointProcess parameters
        """
        self._point_process_params.update(point_process_params)
        return self

    def spine_params(self, head_nseg: Union[int, Dist] = 2, neck_nseg: Union[int, Dist] = 2):
        """
        Experimental feature.

        if called - it will add single spine to each synapse and put synapse on top of the spine.

        :param head_nseg:
            number of segments for head of the spine
        :param neck_nseg:
            number of segments for neck of the spine
        """
        self._spine_params = SpineParams(head_nseg=head_nseg, neck_nseg=neck_nseg)
        return self
