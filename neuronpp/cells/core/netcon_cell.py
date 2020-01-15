from collections import defaultdict

from neuronpp.cells.core.point_process_cell import PointProcessCell
from neuronpp.cells.core.utils import make_conn
from neuronpp.hocs.hoc import Hoc
from neuronpp.hocs.netconn import NetConn


class NetConnCell(PointProcessCell):
    def __init__(self, name):
        PointProcessCell.__init__(self, name)
        self.ncs = []
        self._nc_num = defaultdict(int)

    def filter_netcons(self, mod_name, name_filter, regex=False):
        """
        :param mod_name:
            single string defining name of target point process type name, eg. concere synaptic mechanisms like Syn4PAChDa
        :param name_filter:
            Filter will look for obj_dict keys which contains each name_filter.
        :param regex:
            If True: pattern will be treated as regex expression, if False: pattern str must be in field str
        :return:
        """
        return self.filter(searchable=self.ncs, mod_name=mod_name, name=name_filter, regex=regex)

    def add_netcons(self, source, weight, mod_name=None, name_filter:str=None, regex=False, delay=0):
        """
        All name_filter must contains index of the point process of the specific type.
        eg. head[0][0] where head[0] is name_filter and [0] is index of the point process of the specific type.

        :param source:
            hoc object or None
        :param weight:
        :param mod_name:
            single string defining name of point process type name, eg. concere synaptic mechanisms like Syn4PAChDa
        :param name_filter:
            Filter will look for self.pprocs keys which contains each point_process_names.
        :param regex:
            If True: pattern will be treated as regex expression, if False: pattern str must be in field str
        :param delay:
        return:
            A list of added NetConns.
        """
        results = []
        pps = self.filter_point_processes(mod_name=mod_name, name_filter=name_filter, regex=regex)
        source_hoc = None if source is None else source.hoc

        for pp in pps:
            conn_hoc = make_conn(source=source_hoc, target=pp.hoc, delay=delay, weight=weight)
            name = "%s->%s" % (source, pp)
            conn = NetConn(conn_hoc, parent=self, name=name)
            results.append(conn)

            self.ncs.append(conn)
            self._nc_num[name] += 1

        return results
