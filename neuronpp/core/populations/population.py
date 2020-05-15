import numpy as np
from typing import Union, TypeVar, cast, List

from neuronpp.cells.cell import Cell
from neuronpp.core.hocwrappers.synapse import Synapse
from neuronpp.utils.record import Record
from neuronpp.core.template import Template
from neuronpp.core.populations.connector import Connector
from neuronpp.core.distributions import Dist, UniformProba, NormalProba

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

    def connect(self, rule: str = "all", proba: Union[float, Dist] = 1.0,
                syn_num_per_source: Union[int, Dist] = 1) -> Connector:
        """
        Make a new connection by returning Connector object and adjust it afterwards.

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
        :return:
            Connector object
        """
        return Connector(population_ref=self, rule=rule, proba=proba,
                         syn_num_per_source=syn_num_per_source)

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

    def _make_conn(self, rule: str, target, connector) -> List[List[Synapse]]:
        """
        :param target:
            single target element
        :param connector:
            Connector object
        :return:
            list of added synapses
        """
        result = []
        target_len = len(target)
        for target_i, t in enumerate(target):
            if not self._is_connect(connector._conn_params.proba):
                continue
            cell = t.parent.cell

            syns = []
            for mech in connector._mechs:
                for i in range(connector._conn_params.syn_num_per_source):
                    spine_params = mech._spine_params

                    if spine_params:
                        # TODO rethink connectivity: here - for each target (seg) spine is added
                        spine = cell.add_spines(segs=t, head_nseg=spine_params.head_nseg,
                                                neck_nseg=spine_params.neck_nseg)[0]
                        target = spine.head(1.0)

                    for netcon_params in mech._netcon_params:
                        source = connector._source
                        if hasattr(netcon_params, "source"):
                            source = netcon_params.source

                        if rule == 'all':
                            # iterate over all source
                            pass
                        elif rule == 'one':
                            if target_len != len(source):
                                raise ValueError("For rule 'one' target and source need to be "
                                                 "of the same size.")
                            source = source[target_i]
                        else:
                            raise ValueError("The only allowed rule is all or one, "
                                             "but provided %s" % rule)

                        for s in source:
                            # TODO rethink connectivity: here - for each target (seg) syn is added
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
