import abc
from typing import List, Union

import numpy as np

from neuronpp.cells.cell import Cell
from neuronpp.core.hocwrappers.netstim import NetStim
from neuronpp.core.hocwrappers.seg import Seg
from neuronpp.core.hocwrappers.vecstim import VecStim
from neuronpp.utils.record import Record
from neuronpp.core.distributions.distribution import AllDist, OneDist, Dist, Proba, UniformProba, \
    UniformDist, NormalDist, NormalProba

ALL_DIST = AllDist()
ONE_DIST = OneDist()


class Population:
    def __init__(self, name):
        self.name = name
        self.cell_counter = 0
        self.cells = []
        self.syns = []
        self.recs = {}

    def create(self, cell_num, **kwargs):
        result = []
        for i in range(cell_num):
            cell = self.cell_definition(**kwargs)
            cell.name = "%s[%s][%s]" % (self.name, cell.name, self.cell_counter)
            self.cell_counter += 1
            self.cells.append(cell)
            result.append(cell)

        return result

    def connect(self, source: List[Union[Seg, VecStim, NetStim]], target: List[Seg],
                mod_name, conn_dist: Dist, syn_num_per_source=1, tag=None,
                with_spine=False, netcon_weight=1, delay=0, threshold=10,
                conn_proba: Proba = UniformProba(expected=1), **kwargs):
        """
        :param conn_dist:
        :return:
            list of list of synapses
        """
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

        if isinstance(conn_dist, AllDist):
            for s in source:
                for t in target:
                    if not self._is_connect(conn_proba):
                        continue
                    syn = self._add_syn(source=s, target=t, mod_name=mod_name,
                                        netcon_weight=netcon_weight,
                                        delay=delay, threshold=threshold, tag=tag,
                                        with_spine=with_spine, **kwargs)
                    result.append(syn)

        elif isinstance(conn_dist, OneDist):
            if len(source) != len(target):
                raise LookupError(
                    "for rule 'one' len of sources and population cells must be the same, "
                    "but it was %s and %s respectively." % (len(source), len(self.cells)))

            for s, t in zip(source, target):
                if not self._is_connect(conn_proba):
                    continue
                syn = self._add_syn(source=s, target=t, mod_name=mod_name,
                                    netcon_weight=netcon_weight,
                                    delay=delay, threshold=threshold, tag=tag,
                                    with_spine=False, **kwargs)
                result.append(syn)
        elif isinstance(conn_dist, UniformDist):
            pass
        elif isinstance(conn_dist, NormalDist):
            pass
        else:
            raise TypeError("Wrong type of conn_dist")

        self.syns.extend(result)
        return result

    # TODO Kazdy parametr moze podlegac losowaniu z rozkladu
    # TODO syn_num_per_source
    def _add_syn(self, source: (Seg, VecStim, NetStim), target: Seg, mod_name, netcon_weight,
                 delay, threshold, tag, with_spine, **kwargs) -> list:
        cell = target.parent.cell

        if with_spine:
            spines = cell.add_spines(segs=target, head_nseg=2, neck_nseg=2)
            target = spines[0].head

        syn = cell.add_synapse(source=source, seg=target, mod_name=mod_name, delay=delay,
                               netcon_weight=netcon_weight,
                               threshold=threshold, tag=tag, **kwargs)
        return syn

    @staticmethod
    def _is_connect(conn_proba):
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

    @abc.abstractmethod
    def syn_definition(self, source: (Seg, VecStim, NetStim), target: Seg, **kwargs) -> list:
        """
        Must return syns list.
        :param target:
        :param source:
            Can be only: hocwrappers.NetStim, hocwrappers.VecStim, hocwrappers.Seg or None
        :return:
            Must return a list of synapses.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def cell_definition(self, **kwargs) -> Cell:
        """
        You can pass any param you like to this this method
        as long as you provide default param during the method definition.
        :return:
            Must return a single cell created by the population.
        """
        raise NotImplementedError()
