from typing import Union

from neuronpp.core.distributions import Dist


class ConnParams:
    def __init__(self, rule: str = "all", proba: Union[float, Dist] = 1.0,
                 syn_num_per_source: Union[int, Dist] = 1):
        self.rule = rule
        self.proba = proba
        self.syn_num_per_source = syn_num_per_source
