from typing import Union

from neuronpp.core.distributions import Dist


class ConnParams:
    def __init__(self, rule: str = "all",
                 cell_proba: Union[float, Dist] = 1.0,
                 seg_proga: Union[float, Dist] = 1.0,
                 syn_num_per_source: Union[int, Dist] = 1):
        self.rule = rule
        self.cell_proba = cell_proba
        self.syn_num_per_source = syn_num_per_source
