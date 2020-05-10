from typing import Union

from neuronpp.core.distributions import Dist


class NetconParams:
    def __init__(self, weight: Union[float, Dist] = 1.0, delay: Union[float, Dist] = 1,
                 threshold: Union[float, Dist] = 10):
        self.weight = weight
        self.delay = delay
        self.threshold = threshold
