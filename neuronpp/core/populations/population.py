import numpy as np
from typing import Union, TypeVar, cast, List, Iterable

from neuronpp.cells.cell import Cell
from neuronpp.core.hocwrappers.synapse import Synapse
from neuronpp.utils.record import Record
from neuronpp.core.template import Template
from neuronpp.core.populations.connector import Connector
from neuronpp.core.distributions import Dist, UniformProba, NormalProba, NormalTruncatedSegDist, \
    UniformDist

T_Cell = TypeVar('T_Cell', bound=Cell)


class Population:
    def __init__(self, name):
        self.name = name
        self.cells = []
        self.syns = []
        self.recs = {}

        self.cell_counter = 0

    def add_cells(self, template: T_Cell, num: int):
        """
        Add cells base on provided template cell.
        The template cell must have build_on_the_fly param set to False.

        :param template:
            must be of type Template and Cell, it can derive from Cell.
        :param num:
            number of cells to create
        """
        if not isinstance(template, Template) or not isinstance(template, Cell):
            raise AttributeError("Param template must be of type Template and Cell.")
        template = cast(Template, template)

        for i in range(num):
            cell, results = template.build()
            cell.name = "%s[%s][%s]" % (self.name, cell.name, self.cell_counter)
            self.cell_counter += 1
            self.cells.append(cell)

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

    def connect(self, rule: str = "all",
                cell_proba: Union[float, Dist] = 1.0,
                seg_dist: Union[NormalTruncatedSegDist, str] = "uniform",
                syn_num_per_source: Union[int, Dist] = 1) -> Connector:
        """
        Make a new connection by returning Connector object and adjust it afterwards.

        :param rule:
            default is 'all'
            'all' - all-to-all connections
            'one' - one-to-one connections
        :param cell_proba:
            default us 1.0
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
        :return:
            Connector object
        """
        return Connector(population_ref=self, rule=rule, cell_proba=cell_proba,
                         seg_dist=seg_dist, syn_num_per_source=syn_num_per_source)

    def _build_connector(self, conn: Connector):
        """
        Make new connection by adding existing Connector object created in advance
        :param conn:
            Connector object
        :return:
            list of all created synapses
        """
        target = conn._target
        conn_params = conn._conn_params

        cell_num = len(self.cells)
        if cell_num == 0:
            raise LookupError(
                "Population %s has no cells, cannot make connections. Add cells first." % self.name)

        result_syns = self._make_conn(conn_params.rule, target, conn)
        self.syns.extend(result_syns)
        return result_syns

    def _make_conn(self, rule: str, cells_targets, connector) -> List[List[Synapse]]:
        """
        :param cells_targets:
            single target element
        :param connector:
            Connector object
        :return:
            list of added synapses
        """
        result = []
        cell_num = len(cells_targets)
        conn_params = connector._conn_params

        for target_i, targets in enumerate(cells_targets):
            current_targets = self._get_current_targets(targets, seg_dist=conn_params.seg_dist)

            for t in current_targets:
                if not self._is_connect(conn_params.cell_proba):
                    continue
                cell = targets.parent.cell

                syns = []
                for mech in connector._mechs:
                    for i in range(conn_params.syn_num_per_source):
                        spine_params = mech._spine_params

                        if spine_params:
                            spine = cell.add_spines(segs=t, head_nseg=spine_params.head_nseg,
                                                    neck_nseg=spine_params.neck_nseg)[0]
                            t = spine.head(1.0)

                        for netcon_params in mech._netcon_params:
                            source = connector._source
                            if hasattr(netcon_params, "source"):
                                source = netcon_params.source

                            if rule == 'all':
                                # iterate over all source
                                pass
                            elif rule == 'one':
                                if cell_num != len(source):
                                    raise ValueError("For rule 'one' target and source need to be "
                                                     "of the same size.")
                                source = source[target_i]
                            else:
                                raise ValueError("The only allowed rule is all or one, "
                                                 "but provided %s" % rule)

                            for s in source:
                                syn = cell.add_synapse(source=s, seg=t, mod_name=mech.mod_name,
                                                       delay=netcon_params.delay,
                                                       netcon_weight=netcon_params.weight,
                                                       threshold=netcon_params.threshold,
                                                       tag=connector.set_tag,
                                                       **mech._synaptic_params)
                                syns.append(syn)

                if connector._group_syns:
                    cell.group_synapses(tag=connector.set_tag, *syns)
                if connector._synaptic_func:
                    connector._synaptic_func(syns)

                result.extend(syns)

        return result

    @staticmethod
    def _get_current_targets(targets, seg_dist):
        """
        :param targets:
        :param seg_dist:
        :return:
            current target list based on the provided distribution type
        """
        mean = None
        if not isinstance(targets, Iterable):
            targets = [targets]

        if seg_dist == 'all':
            return targets
        elif seg_dist == 'uniform':
            return np.random.choice(targets, 1)
        elif isinstance(seg_dist, NormalTruncatedSegDist):
            if not mean:
                mean = np.random.uniform(size=1)[0]
            targets[0].parent.hoc.n3d()
            xyz = np.random.normal(loc=mean, scale=seg_dist.std, size=3)
            return ""
        else:
            raise TypeError("Param seg_dist can be only str: 'all', 'uniform' or "
                            "object: NormalTruncatedSegDist, but provided: %s" % seg_dist.__class__)

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
