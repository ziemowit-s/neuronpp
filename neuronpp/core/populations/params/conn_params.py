from typing import Union

from neuronpp.core.distributions import Dist, NormalTruncatedSegDist


class ConnParams:
    def __init__(self, rule: str = "all",
                 cell_connection_proba: Union[float, Dist] = 1.0,
                 seg_dist: Union[NormalTruncatedSegDist, str] = "uniform",
                 syn_num_per_cell_source: Union[int, Dist] = 1):
        """
        :param rule:
            'all' or 'one'
        :param cell_connection_proba:
            probability of connecting source and target
        :param seg_dist:
            distribution of single connection between provided target segments.

            "all" - str: means all provided segments will be taken.

            "uniform" - str: means all segs are equally probable
                        Uniform distribution for segment choosing. Uniform means that all
                        provided segments have equal probability.

            NormalDist - object: probability of choose seg with mean and std provided
                        Normal distribution for segment choosing.
                        Normal means that choosing segments are clustered around mean with standard
                        deviation std.
                        :param mean:
                            Provided in normalized arbitrary unit between 0-1.
                            It is normalized mean (between 0-1), where all provided segments are
                            organized as list
                            and first element has location=0 and the last location=1
                            During computation this number will be change for appropriate mean in
                            um.
                        :param std:
                            Provided in um.
                            standard deviation of the cluster of distribution.

        :param syn_num_per_cell_source:
            how many synapses single source should have
        """
        self.rule = rule
        self.cell_connection_proba = cell_connection_proba
        if isinstance(seg_dist, str) and seg_dist not in ['all', 'uniform'] and \
                not isinstance(seg_dist, NormalTruncatedSegDist):
            raise TypeError("Param seg_dist can be only str: 'all', 'uniform' or "
                            "object: NormalTruncatedSegDist, but provided: %s" % seg_dist.__class__)
        self.seg_dist = seg_dist
        self.syn_num_per_cell_source = syn_num_per_cell_source
