from collections import defaultdict

from neuron import h

from cells.core.basic_cell import BasicCell


class PointProcessCell(BasicCell):
    def __init__(self, name):
        """
        :param name:
            Name of the cell
        """
        BasicCell.__init__(self, name)
        self.point_processes = {}
        self._pprocs_num = defaultdict(int)

    def filter_point_processes(self, pp_type_name: str, sec_names, as_list=False):
        """
        All sec_names must contains index of the point process of the specific type.
        eg. head[0][0] where head[0] is sec_name and [0] is index of the point process of the specific type.

        :param pp_type_name:
            single string defining name of point process type name, eg. concere synaptic mechanisms like Syn4PAChDa
        :param sec_names:
            List of string names as list or separated by space.
            Filter will look for self.pprocs keys which contains each point_process_names.
            None or 'all' will add to all point processes.
        :param as_list:
        :return:
        """
        return self._filter_obj_dict("point_processes", mech_type=pp_type_name, names=sec_names, as_list=as_list)

    def add_point_processes(self, pp_type_name, sec_names, loc, **kwargs):
        """
        :param pp_type_name:
        :param sec_names:
            List of string names as list or separated by space.
            Filter will look for obj_dict keys which contains each sec_name.
            None or 'all' will add point process to all secs.
        :param loc:
        :param kwargs:
        :return:
            A list of added Point Processes
        """
        result = []
        if not hasattr(h, pp_type_name):
            raise LookupError("There is no Point Process of name %s. "
                              "Maybe you forgot to compile or copy mod files?" % pp_type_name)
        pp = getattr(h, pp_type_name)
        sec_names = self._filter_obj_dict("secs", names=sec_names)

        for sec_name, sec in sec_names.items():
            pp_instance = pp(sec(loc))
            result.append(pp_instance)

            for key, value in kwargs.items():
                if not hasattr(pp_instance, key):
                    raise LookupError("Point Process of type %s has no attribute of type %s. "
                                      "Check if MOD file contains %s as a RANGE variable" % (pp_type_name, key, key))
                setattr(pp_instance, key, value)

            type_name = "%s_%s" % (pp_type_name, sec_name)
            self.point_processes["%s[%s]" % (type_name, self._pprocs_num[type_name])] = pp_instance
            self._pprocs_num[type_name] += 1

        return result
