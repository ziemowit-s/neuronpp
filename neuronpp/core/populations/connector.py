from typing import Optional, List, Union, Callable

from neuronpp.core.distributions import Dist
from neuronpp.core.hocwrappers.seg import Seg
from neuronpp.core.hocwrappers.netstim import NetStim
from neuronpp.core.hocwrappers.synapse import Synapse
from neuronpp.core.hocwrappers.vecstim import VecStim
from neuronpp.core.populations.params.conn_params import ConnParams
from neuronpp.core.populations.mech_adder import SynAdder


class Connector:
    def __init__(self, population_ref, rule: str = "all", proba: Union[float, Dist] = 1.0,
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
        :param proba:
            default us 1.0
            can be a single number from 0 to 1 defining probability of connection.
            In this case it will assume UniformProba

            It can also be an instance of Dist class which defines specific distribution with
            an expected value
        :param syn_num_per_source:
            default is 1
            number of synapse per single source object
        """
        self._population_ref = population_ref

        self._mechs: List[SynAdder] = []
        self._group_syns = False

        self._tag = None
        self._source = None
        self._target = None
        self._synaptic_func = None

        self._conn_params = ConnParams(rule=rule, proba=proba,
                                       syn_num_per_source=syn_num_per_source)

    def source(self, source: Optional[List[Union[Seg, VecStim, NetStim]]] = None):
        """
        Source object(s) which will call the Netcon(s) to initiate stimulation(s)
        :param source:
        :return:
            self object (builder paradigm)
        """
        self._source = source
        return self

    # TODO change for filter function(?)
    def target(self, target: List[Seg]):
        """
        Target list of Segments
        :param target:
        :return:
            self object (builder paradigm)
        """
        self._target = target
        return self

    def tag(self, tag):
        """
        Add tag to all synapses created by this Connector
        :param tag:
        :return:
            self object (builder paradigm)
        """
        self._tag = tag
        return self

    def synaptic_function(self, func: Callable[[List[Synapse]], None]):
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

    def build(self):
        """
        Build this Connector object.
        Connector object can be build only once.

        :return:
            Population object which is the owner of this Connector (builder paradigm)
        """
        self._population_ref._build_connector(self)
        return self._population_ref

    def add_synapse(self, mod_name: str) -> SynAdder:
        """
        Add new synapse, which consists of single PointProcess and 1 or more NetCons
        :param mod_name:
            name of the MOD file which must be PointProcess
        :return:
            SynAdder object
        """
        mech = SynAdder(mod_name=mod_name)
        self._mechs.append(mech)
        return mech
