from collections import defaultdict

from neuronpp.cells.core.point_process_cell import PointProcessCell
from neuronpp.cells.core.utils import get_conn


class NetConnCell(PointProcessCell):
    def __init__(self, name):
        PointProcessCell.__init__(self, name)
        self.netcons = {}
        self._conn_num = defaultdict(int)

    def filter_netcons(self, pp_type, sec_names, as_list=False):
        """
        :param pp_type:
            single string defining name of target point process type name, eg. concere synaptic mechanisms like Syn4PAChDa
        :param sec_names:
            List of string names as list or separated by space.
            Filter will look for obj_dict keys which contains each sec_name.
            None or 'all' will return all conns.
        :param as_list:
        :return:
        """
        return self._filter_obj_dict("netcons", mech_type=pp_type, names=sec_names, as_list=as_list)

    def add_netcons(self, source, weight, pp_type_name=None, sec_names=None, delay=0):
        """
        All sec_names must contains index of the point process of the specific type.
        eg. head[0][0] where head[0] is sec_name and [0] is index of the point process of the specific type.

        :param source:
        :param weight:
        :param pp_type_name:
            single string defining name of point process type name, eg. concere synaptic mechanisms like Syn4PAChDa
        :param sec_names:
            List of string names as list or separated by space.
            Filter will look for self.pprocs keys which contains each point_process_names.
            None or 'all' will add to all point processes.
        :param delay:
        return:
            A list of added NetConns.
        """
        results = []
        conn_names = self.filter_point_processes(pp_type_name=pp_type_name, sec_names=sec_names)

        for name, syn in conn_names.items():
            conn = get_conn(source=source, target=syn, delay=delay, weight=weight)
            results.append(conn)

            type_name = "%s_%s" % (pp_type_name, name)
            self.netcons["%s[%s]" % (type_name, self._conn_num[type_name])] = conn
            self._conn_num[type_name] += 1

        return results
