from typing import Union, Optional, List

from neuronpp.core.distributions import Dist
from neuronpp.core.hocwrappers.netstim import NetStim
from neuronpp.core.hocwrappers.seg import Seg
from neuronpp.core.hocwrappers.vecstim import VecStim


class NetconParams:
    def __init__(self, source: Optional[Union[List[Union[Seg, VecStim, NetStim]], str]] = "default",
                 weight: Union[float, Dist] = 1.0, delay: Union[float, Dist] = 1,
                 threshold: Union[float, Dist] = 10):
        self.source = source
        self.weight = weight
        self.delay = delay
        self.threshold = threshold
