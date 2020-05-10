from typing import Union

from neuronpp.core.distributions import Dist


class SpineParams:
    def __init__(self, head_nseg: Union[int, Dist] = 2, neck_nseg: Union[int, Dist] = 2):
        self.head_nseg = head_nseg
        self.neck_nseg = neck_nseg
