from collections import defaultdict

from neuron import h

from neuronpp.core.cells.section_cell import SectionCell
from neuronpp.core.hocwrappers.point_process import PointProcess


class PointProcessCell(SectionCell):
    def __init__(self, name):
        """
        :param name:
            Name of the cell
        """
        SectionCell.__init__(self, name)
        self.pps = []
        self._pp_num = defaultdict(int)

    def filter_point_processes(self, mod_name: str, name):
        """
        All name must contains index of the point process of the specific type.
        eg. head[0][0] where head[0] is name and [0] is index of the point process of the specific type.

        :param mod_name:
            single string defining name of point process type name, eg. concere synaptic mechanisms like Syn4PAChDa
        :param name:
            start with 'regex:any pattern' to use regular expression. If without 'regex:' - will look which Hoc objects contain the str
        :return:
        """
        return self.filter(searchable=self.pps, mod_name=mod_name, name=name)

    def make_point_processes(self, mod_name: str, loc, sec=None, name=None, **synaptic_params):
        """
        :param mod_name:
        :param sec:
        :param loc:
        :param synaptic_params:
            Dictionary containing params for the mod point_process
        :param name:
            custom name added to this point_process
        :return:
            A list of added Point Processes
        """
        if not hasattr(h, mod_name):
            raise LookupError("There is no Point Process of name %s. "
                              "Maybe you forgot to compile or copy mod files?" % mod_name)
        pp_obj = getattr(h, mod_name)

        if isinstance(sec, str) or sec is None:
            sec = self.filter_secs(name=sec)

        result = []
        for sec in sec:
            hoc_pp = pp_obj(sec.hoc(loc))

            current_mod_name = "%s_%s" % (mod_name, sec.name)
            sec_name = "%s[%s]" % (sec.name, self._pp_num[current_mod_name])
            self._pp_num[current_mod_name] += 1

            if name:
                sec_name = "%s[%s]" % (sec_name, name)

            pp = PointProcess(hoc_pp, parent=self, name=sec_name, mod_name=mod_name)
            result.append(pp)
            self.pps.append(pp)

            for key, value in synaptic_params.items():
                if not hasattr(pp.hoc, key):
                    raise LookupError("Point Process of type %s has no attribute of type %s. "
                                      "Check if MOD file contains %s as a RANGE variable" % (mod_name, key, key))
                setattr(pp.hoc, key, value)

        return result
