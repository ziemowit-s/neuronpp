from typing import Union

from neuronpp.core.distributions import Dist
from neuronpp.core.populations.utils import check_and_prepare_sources


class NetconParams:
    def __init__(self, weight: Union[float, Dist] = 1.0,
                 delay: Union[float, Dist] = 1,
                 threshold: Union[float, Dist] = 10, **kwargs):
        """
        NetCon params used for Population configuration.
        :param weight:
        :param delay:
        :param threshold:
        :param kwargs:
            'custom_source': can be: None or Seg, VecStim, NetStim, or list of Seg, VecStim,
            NetStim. By default it is not set meaning that default source from Connector will be
            used.
        """
        if "custom_source" in kwargs:
            self.custom_source = check_and_prepare_sources(kwargs['custom_source'])
        self.weight = weight
        self.delay = delay
        self.threshold = threshold
