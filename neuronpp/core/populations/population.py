import numpy as np
from typing import Union, TypeVar, List, Iterable, Callable

from neuronpp.cells.cell import Cell
from neuronpp.core.hocwrappers.synapses.synapse import Synapse
from neuronpp.utils.record import Record
from neuronpp.core.populations.connector import Connector
from neuronpp.core.distributions import Dist, UniformProba, NormalProba, NormalTruncatedSegDist

T_Cell = TypeVar('T_Cell', bound=Cell)


class Population:
    def __init__(self, name):
        self.name = name
        self.cells = []
        self.syns = []
        self.recs = {}

        self.cell_counter = 0

    def add_cells(self, num: int, cell_function: Callable[[], T_Cell]):
        """
        :param num:
            number of cells to create
        :param cell_function
        """
        for i in range(num):
            cell = cell_function()
            cell.population = self
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
            position of all subplots ON EACH figure (each figure is created for each variable
            separately).
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
            default is 1.0
            can be a single float between 0 to 1 (defining probability of connection), it will
            assume UniformProba.
            It can also be an instance of Dist class which defines specific distribution with an
            expected value.
        :param seg_dist:
            default is "uniform"
            distribution of a single connection from source to target segments

            "all" - str: means all provided segments will be taken.

            "uniform" - str: means all segs are equally probable
                        Uniform distribution for segment choosing. Uniform means that all
                        provided segments have equal probability.

            NormalDist - object: probability of choose seg with mean and std provided
                        Normal distribution for segment choosing.
                        Normal means that choosing segments are clustered around mean with standard
                        deviation std.
                        :param mean:
                            Provided in normalized arbitrary unit between 0-1, where all provided
                            segments are organized as list. The first element has location=0,
                            the last location=1.
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

    def _make_conn(self, source_rule: str, cells_targets, connector) -> List[List[Synapse]]:
        """
        TODO refactoring required:
          * method is too extensive
          * rethink connection rule provision because currently there is:
            * source_rule as string - defines rule for source -to-> target connection
            * connector.conn_params.cell_proba - defines distribution for cell connection
            (yes or no)
            * connector.conn_params.seg_dist - defines distribution for target selection
              (while cell is selected to connect)

        Creates connection based on provided source_rule, cells' target segments and connection rule

        :param source_rule:
            string which defines connection rule for source

            "all" - means all to all connection between each source and each target
            "one" - means one to one connection between one source and one target
        :param cells_targets:
            Each element of cells_targets contains a list of target segments
        :param connector:
            Connector object containing rules for connection
        :return:
            list of added synapses
        """
        result = []
        cell_num = len(cells_targets)
        conn_params = connector._conn_params

        for cell_i, potential_target_segments in enumerate(cells_targets):
            # based on cell_proba - decide if we want to make a connection with that cell
            if not self._is_make_cell_connection(conn_params.cell_proba):
                continue
            cell = potential_target_segments.parent.cell

            # TODO Hack - which ensures that there is the same seg_dist_mean for all synapses with
            #  the same cell
            seg_dist_mean = None
            if isinstance(conn_params.seg_dist,
                          NormalTruncatedSegDist) and conn_params.seg_dist.mean is None:
                seg_dist_mean = np.random.uniform(size=1)[0]

            # create syn_num_per_source number of synapses per single source
            for synapse_i in range(conn_params.syn_num_per_source):

                # based on seg_dist - decide with what target_segment(s) we want to make connection
                target_segments = self._get_current_target_segments(potential_target_segments,
                                                                    seg_dist=conn_params.seg_dist,
                                                                    normal_mean=seg_dist_mean)

                for target_segment in target_segments:
                    syns = []
                    # iter over all point processes provided
                    # each target_segment will receive all provided point processes
                    for mech in connector._syn_adders:
                        spine_params = mech._spine_params

                        if spine_params:
                            spine = cell.add_spines(segs=target_segment,
                                                    head_nseg=spine_params.head_nseg,
                                                    neck_nseg=spine_params.neck_nseg)[0]
                            target_segment = spine.head(1.0)

                        # iter over all netcons - for each netcon create a new connection
                        # eg. single point process can have netconn from the real source
                        # and from the outside stimuli (netcon with source=None)
                        for netcon_params in mech._netcon_params:
                            sources = connector._sources

                            # if netcon has custom sources, different than the default connector
                            # sources it will use only netconn's sources in that case
                            if hasattr(netcon_params, "source"):
                                sources = netcon_params.custom_sources

                            # Based on source_rule - decide with which source we want to make c
                            # onnection
                            if source_rule == 'all':
                                pass  # iterate over all sources provided
                            elif source_rule == 'one':
                                if cell_num != len(sources):
                                    raise ValueError("For rule 'one' target and source need to be "
                                                     "of the same size.")
                                sources = [sources[cell_i]]  # select only a particular source
                            else:
                                raise ValueError("The only allowed rule is all or one, "
                                                 "but provided %s" % source_rule)

                            # iter over all sources
                            for s in sources:
                                syn = cell.add_synapse(source=s, seg=target_segment,
                                                       mod_name=mech.mod_name,
                                                       tag=connector.set_tag,
                                                       delay=netcon_params.delay,
                                                       netcon_weight=netcon_params.weight,
                                                       threshold=netcon_params.threshold,
                                                       **mech._point_process_params)
                                syns.append(syn)

                    # group synapses if required for each target_segment
                    # eg. for multi-netcons synapses (like ACh+Da+hebbian synapse)
                    # This requirement need to be directly define by the user
                    if connector._group_syns:
                        cell.group_synapses(tag=connector.set_tag, *syns)

                    # perform a custom function on created synapses if required for each
                    # target_segment
                    # This requirement need to be directly define by the user
                    if connector._synaptic_func:
                        connector._synaptic_func(syns)

                    result.extend(syns)

        return result

    @staticmethod
    def _get_current_target_segments(potential_target_segments, seg_dist, normal_mean=None):
        """
        TODO It requires refactoring in the future
          * returning all potential_target_segments or only one from that list - seems to be a
          bad practice
          * passing mean as a param only for NormalTruncatedSegDist distribution - seems to be a
          bad practice

        Returns a list of target section to connect.

        It returns a list of single element: target section if seg_dist is "uniform" or NormalDist
        It returns a list of all targets provided in the potential_target_segments if seg_dist is
        "all"

        :param potential_target_segments:
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
        :return:
            target section list based on the provided distribution type
        """
        if not isinstance(potential_target_segments, Iterable):
            potential_target_segments = [potential_target_segments]

        if seg_dist == 'all':
            return np.array(potential_target_segments)
        elif seg_dist == 'uniform':
            return np.random.choice(potential_target_segments, 1)
        elif isinstance(seg_dist, NormalTruncatedSegDist):
            if normal_mean is None:
                normal_mean = seg_dist.mean
            value = np.abs(np.random.normal(loc=normal_mean, scale=seg_dist.std, size=1))[0]
            if len(potential_target_segments) == 1:
                index = 0
            else:
                index = round(len(potential_target_segments) * value) - 1
            return np.array([potential_target_segments[index]])
        else:
            raise TypeError("Param seg_dist can be only str: 'all', 'uniform' or "
                            "object: NormalTruncatedSegDist, but provided: %s" % seg_dist.__class__)

    @staticmethod
    def _is_make_cell_connection(conn_proba: Union[float, int, Dist]):
        """
        Determine if there should be a connection between single tuple of (source and target) based
        on conn_proba type and conn_proba.expected value.

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
