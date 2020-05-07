from copy import deepcopy
from typing import List, Union

import numpy as np

from neuronpp.core.cells.core_cell import CoreCell
from neuronpp.core.hocwrappers.netstim import NetStim
from neuronpp.core.hocwrappers.seg import Seg
from neuronpp.core.hocwrappers.vecstim import VecStim
from neuronpp.utils.record import Record
from neuronpp.core.distributions import Dist, UniformProba, NormalProba


class ConnParams:
    def __init__(self, rule: str = "all", proba: Union[float, Dist] = 1.0,
                 syn_num_per_source: Union[int, Dist] = 1):
        self.rule = rule
        self.proba = proba
        self.syn_num_per_source = syn_num_per_source


class NetconParams:
    def __init__(self, weight: Union[float, Dist] = 1.0, delay: Union[float, Dist] = 1,
                 threshold: Union[float, Dist] = 10):
        self.weight = weight
        self.delay = delay
        self.threshold = threshold


class SpineParams:
    def __init__(self, head_nseg: Union[int, Dist] = 2, neck_nseg: Union[int, Dist] = 2):
        self.head_nseg = head_nseg
        self.neck_nseg = neck_nseg


class Population:
    def __init__(self, name):
        self.name = name
        self.cell_counter = 0
        self.cells = []
        self.syns = []
        self.recs = {}

    def add_cells(self, template: CoreCell, num: int):
        """
        :param template:
        :param num:
        :return:
            created list of cells
        """
        if template._build_on_the_fly:
            raise AttributeError("Param build_on_the_fly must be set to False for "
                                 "cell passed as a template to the Population.")

        result = []
        for i in range(num):
            cell = deepcopy(template)
            results = cell.build()

            cell.name = "%s[%s][%s]" % (self.name, template.name, self.cell_counter)
            self.cell_counter += 1

            self.cells.append(cell)
            result.append(results)

        return result

    def connect(self, source: List[Union[Seg, VecStim, NetStim]], target: List[Seg],
                mod_name, tag=None,
                netcon_params: NetconParams = None, conn_params: ConnParams = None,
                spine_params: SpineParams = None, **point_process_params):
        """
        :param source
        :param target
        :param mod_name
        :param tag

        :param netcon_params:
            object of type NetconParams
            :param weight:
                default is 1.0
            :param delay:
                default is 1
                delay in ms
            :param threshold:
                default is 10
                threshold in mV
                
        :param conn_params:
            object of type ConnParams:
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

        :param spine_params:
            object of type SpineParams:
                :param head_nseg:
                    number of segments for head of the spine
                :param neck_nseg:
                    number of segments for neck of the spine

        :return:
            list of list of synapses
        """
        if netcon_params is None:
            netcon_params = NetconParams()
        if conn_params is None:
            conn_params = ConnParams()
        if spine_params is None:
            spine_params = SpineParams()

        cell_num = len(self.cells)
        if cell_num == 0:
            raise LookupError(
                "Population %s has no cells, cannot make connections. Add cells first." % self.name)

        result = []
        if source is None:
            source = [None for _ in range(cell_num)]
        if not isinstance(source, list):
            source = [source]
        if not isinstance(target, list):
            target = [target]

        if conn_params.rule == 'all':
            for s in source:
                # TODO syn_num_per_source
                for t in target:
                    if not self._is_connect(conn_params.proba):
                        continue
                    syn = self._add_syn(s, t, mod_name,
                                        netcon_params, spine_params, tag, **point_process_params)
                    result.append(syn)

        elif conn_params.rule == 'one':
            if len(source) != len(target):
                raise LookupError(
                    "for rule 'one' len of sources and population cells must be the same, "
                    "but it was %s and %s respectively." % (len(source), len(self.cells)))

            # TODO syn_num_per_source
            for s, t in zip(source, target):
                if not self._is_connect(conn_params.proba):
                    continue
                syn = self._add_syn(s, t, mod_name,
                                    netcon_params, spine_params, tag, **point_process_params)
                result.append(syn)
        else:
            raise TypeError("Wrong type of conn_dist")

        self.syns.extend(result)
        return result

    @staticmethod
    def _add_syn(source: Union[Seg, VecStim, NetStim], target: Seg, mod_name,
                 netcon_params, spine_params, tag, **kwargs) -> list:
        cell = target.parent.cell

        if spine_params:
            spine = cell.add_spines(segs=target, head_nseg=spine_params.head_nseg,
                                    neck_nseg=spine_params.neck_nseg)[0]
            target = spine.head(1.0)

        syn = cell.add_synapse(source=source, seg=target, mod_name=mod_name,
                               delay=netcon_params.delay, netcon_weight=netcon_params.weight,
                               threshold=netcon_params.threshold, tag=tag, **kwargs)
        return syn

    @staticmethod
    def _is_connect(conn_proba: Union[float, int, Dist]):
        """
        Determin if make connection between single tuple of (source and target) based on conn_proba

        :param conn_proba:
            can be a single number from 0 to 1 defining probability of connection.
            In this case it will assume UniformProba

            It can also be an instance of Dist class which defines specific distribution with
            an expected value
        :return:
        """
        if conn_proba == 1:
            return True
        elif isinstance(conn_proba, (float, int)):
            conn_proba = UniformProba(expected=conn_proba)

        if isinstance(conn_proba, UniformProba):
            result = np.random.uniform(size=1)[0]
        elif isinstance(conn_proba, NormalProba):
            result = np.random.normal(loc=conn_proba.mean, scale=conn_proba.std)
        else:
            raise TypeError("Not allowed conn_proba.")

        return conn_proba.expected > result

    def record(self, sec_name="soma", loc=0.5, variable='v'):
        d = [cell.filter_secs(sec_name, as_list=True)[0](loc) for cell in self.cells]
        rec = Record(d, variables=variable)
        self.recs[variable] = rec

    def plot(self, animate=False, **kwargs):
        """
        Plots each recorded variable for each neurons in the population.

        If animate=True it will live update graphs. Other params are for live update purpose.

        :param animate:
            If True it will live update graphs.
        :param steps:
            how many timesteps to see on the graph
        :param y_lim:
            tuple of limits for y axis. Default is (-80, 50)
        :param position:
            position of all subplots ON EACH figure (each figure is created for each variable separately).
            * position=(3,3) -> if you have 9 neurons and want to display 'v' on 3x3 matrix
            * position='merge' -> it will display all figures on the same graph.
            * position=None -> Default, each neuron has separated  axis (row) on the figure.
        """
        for r in self.recs.values():
            r.plot(animate=animate, **kwargs)
