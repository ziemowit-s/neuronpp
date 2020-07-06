from typing import Optional, List, Union, Callable

from neuronpp.core.hocwrappers.seg import Seg
from neuronpp.core.hocwrappers.netstim import NetStim
from neuronpp.core.hocwrappers.synapses.synapse import Synapse
from neuronpp.core.hocwrappers.vecstim import VecStim
from neuronpp.core.populations.syn_adder import SynAdder
from neuronpp.core.populations.params.conn_params import ConnParams
from neuronpp.core.distributions import Dist, NormalTruncatedSegDist
from neuronpp.core.populations.utils import check_and_prepare_sources, check_and_prepare_target


class Connector:
    def __init__(self, population_ref, rule: str = "all",
                 cell_proba: Union[float, Dist] = 1.0,
                 seg_dist: Union[NormalTruncatedSegDist, str] = "uniform",
                 syn_num_per_source: Union[int, Dist] = 1):
        """
        Connector object required to build new connections for Population.

        THIS OBJECT SHOULD NOT BE BUILT BY THE USER, but rather retrieved by calling
        make_connection() method of Population object.

        After setup you need to call build() method to create NEURON objects.
        build() will call population_ref._build_connector() method to create those objects inside
        Population.

        :param population_ref:
            reference to the Population
        :param rule:
            default is 'all'
            'all' - all-to-all connections
            'one' - one-to-one connections
        :param cell_proba:
            default is 1.0
            can be a single number from 0 to 1 defining probability of connection.
            In this case it will assume UniformProba

            It can also be an instance of Dist class which defines specific distribution with
            an expected value
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
        :param syn_num_per_source:
            default is 1
            number of synapse per single source object
        """
        self._population_ref = population_ref

        self._syn_adders = []  # List[SynAdder]
        self._group_syns = False

        self._tag = None
        self._sources = None
        self._target = None
        self._synaptic_func = None

        self._conn_params = ConnParams(rule=rule, cell_proba=cell_proba, seg_dist=seg_dist,
                                       syn_num_per_source=syn_num_per_source)

    def set_source(self, source: Optional[Union[List[Union[Seg, VecStim, NetStim]], Seg, VecStim,
                                                NetStim]]):
        """
        Source object(s) which will call the Netcon(s) to initiate stimulation(s)
        :param source:
            can be: None or Seg, VecStim, NetStim, or list of Seg, VecStim, NetStim.
                    By default source is None.
        :return:
            self object (builder paradigm)
        """
        self._sources = check_and_prepare_sources(source)
        return self

    # TODO change for filter function(?)
    def set_target(self, target: Union[List[Seg], Seg]):
        """
        Target list of Segments
        :param target:
        :return:
            self object (builder paradigm)
        """
        self._target = check_and_prepare_target(target)
        return self

    def set_tag(self, tag):
        """
        Add tag to all synapses created by this Connector
        :param tag:
        :return:
            self object (builder paradigm)
        """
        self._tag = tag
        return self

    def set_synaptic_function(self, func: Callable[[List[Synapse]], None]):
        """
        Add function which will be called on all synapses created for single cell of the population.
        The function definition should be:

            def func(synapses: List[Synapse]):
                ...

        It maybe useful if you create more than a single PointProcess or more than a single NetCon.

        :param func:
            function to call for all synapses created for a single cell of the population, as:
                def func(synapses: List[Synapse]):
                    ...
        :return:
            self object (builder paradigm)
        """
        self._synaptic_func = func
        return self

    def group_synapses(self):
        """
        Group synapses as a single SynapticGroup. It is helpful if you have multiple synapses, which
        you want to group together, eg. AMPA and NMDA synapses.

        Single synapse consists of single PointProcess (MOD file) and 1 or more NetCons. If you have
        multiple PointProcesses (MOD files) which you want to group together and call them together
        you can group them as SynapticGroup with this function.

        This function group all synapses created with this Connector object.
        :return:
            self object (builder paradigm)
        """
        self._group_syns = True
        return self

    def add_synapse(self, mod_name: str) -> SynAdder:
        """
        Add new synapse adder object, which consists of single PointProcess and 1 or more NetCons
        :param mod_name:
            name of the MOD file which must be PointProcess
        :return:
            SynAdder object
        """
        syn_adder = SynAdder(mod_name=mod_name)
        self._syn_adders.append(syn_adder)
        return syn_adder

    def build(self):
        """
        Build this Connector object.
        Connector object can be build only once.

        :return:
            Population object which is the owner of this Connector (builder paradigm)
        """
        self._population_ref._build_connector(self)
        return self._population_ref
