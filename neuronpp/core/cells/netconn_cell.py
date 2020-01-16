from collections import defaultdict

from neuronpp.core.cells.point_process_cell import PointProcessCell
from neuronpp.core.cells.utils import make_conn
from neuronpp.core.hocwrappers.netconn import NetConn


class NetConnCell(PointProcessCell):
    def __init__(self, name=None):
        PointProcessCell.__init__(self, name)
        self.ncs = []
        self._nc_num = defaultdict(int)

    def filter_netcons(self, mod_name: str, name: str):
        """
        :param mod_name:
            single string defining name of target point process type name, eg. concere synaptic mechanisms like Syn4PAChDa
        :param name:
            start with 'regex:any pattern' to use regular expression. If without 'regex:' - will look which Hoc objects contain the str
        :return:
        """
        return self.filter(searchable=self.ncs, mod_name=mod_name, name=name)

    def make_netcons(self, source, weight, point_process=None, mod_name: str = None, delay=0):
        """
        All name must contains index of the point process of the specific type.
        eg. head[0][0] where head[0] is name and [0] is index of the point process of the specific type.

        :param source:
            hoc object or None. If None it will create NetConn with no source, which can be use as external event source
        :param weight:
        :param mod_name:
            single string defining name of point process type name, eg. concrete synaptic mechanisms like Syn4PAChDa
            If None - it assumes that point_process has list of point processes objects
        :param point_process:
            start with 'regex:any pattern' to use regular expression. If without 'regex:' - will look which Hoc objects contain the str
        :param delay:
        return:
            A list of added NetConns.
        """
        if point_process is None and mod_name is None:
            raise LookupError("If point_process is None you need to provide mod_name string param.")

        if isinstance(point_process, str) or point_process is None:
            if mod_name is None:
                raise LookupError("If point_process is str you need to provide mod_name string param.")
            point_process = self.filter_point_processes(mod_name=mod_name, name=point_process)

        source_hoc = None if source is None else source.hoc

        results = []
        for pp in point_process:
            conn_hoc = make_conn(source=source_hoc, target=pp.hoc, delay=delay, weight=weight)
            name = "%s->%s" % (source, pp)
            conn = NetConn(conn_hoc, parent=self, name=name)
            results.append(conn)

            self.ncs.append(conn)
            self._nc_num[name] += 1

        return results
