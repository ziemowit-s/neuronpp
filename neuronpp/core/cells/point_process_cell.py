from neuron import h
from nrn import Segment, Section
from collections import defaultdict

from neuronpp.core.cells.section_cell import SectionCell
from neuronpp.core.cells.utils import get_default
from neuronpp.core.hocwrappers.point_process import PointProcess
from neuronpp.core.hocwrappers.sec import Sec


class PointProcessCell(SectionCell):
    def __init__(self, name=None, compile_paths=None):
        """
        :param name:
            Name of the cell
        """
        SectionCell.__init__(self, name, compile_paths=compile_paths)
        self.pps = []
        self._pp_num = defaultdict(int)

    def filter_point_processes(self, mod_name: str = None, name: str = None, parent: str = None, obj_filter=None,
                               **kwargs):
        """
        Currently all filter passed are treated as AND statements.

        * Whole object callable function passed to the obj_filter param.
            eg. (lambda expression) returns sections which name contains 'apic' or their distance > 1000 um from the soma:
          ```
           soma = cell.filter_secs("soma")
           cell.filter_secs(obj_filter=lambda o: 'apic' in o.name or h.distance(soma(0.5), o(0.5)) > 1000)
          ```

        * Single object field filter based on callable function passed to the obj_filter param.
          eg. (lambda expression) returns sections which parent's name contains less than 10 characters
          ```
          cell.filter_secs(parent=lambda o: len(o.parent.name) < 10)
          ```

        :param mod_name:
            single string defining name of point process type name, eg. concere synaptic mechanisms like Syn4PAChDa
        :param obj_filter:
            Whole object callable functional filter. If you added also any kwargs they will be together with the
            obj_filter treated as AND statement.
        :param name:
            start with 'regex:any pattern' to use regular expression. If without 'regex:' - will look which Hoc objects contain the str
        :return:
        """
        return self.filter(searchable=self.pps, obj_filter=obj_filter, mod_name=mod_name, name=name, parent=parent,
                           **kwargs)

    def add_point_process(self, mod_name: str, sec, tag: str = None, **point_process_params):
        """
        :param mod_name:
        :param sec:
            Segment where to put point process. If section is provided the default loc will be sec(0.5)
            Can be only a Segment, Section or Sec.
        :param point_process_params:
            Dictionary containing params for the mod point_process
        :param tag:
            custom string tag added to this point_process
        :return:
            Created Point Process
        """
        if mod_name is None:
            raise AttributeError("To create a point_process you need to define mod_name param.")
        if not hasattr(h, mod_name):
            raise LookupError("There is no Point Process of name %s. Maybe you forgot to compile or copy mod files?" % mod_name)

        pp_obj = getattr(h, mod_name)
        if not isinstance(sec, (Sec, Segment, Section)):
            raise TypeError("Param 'segment' can be only a Segment, Section or Sec, but provided %s" % sec.__class__)

        sec = get_default(sec)
        hoc_pp = pp_obj(sec)
        pp = self._append_pp(hoc_point_process=hoc_pp, mod_name=mod_name, segment=sec, tag=tag)

        for key, value in point_process_params.items():
            if not hasattr(pp.hoc, key):
                raise LookupError("Point Process of type %s has no attribute of type %s. "
                                  "Check if MOD file contains %s as a RANGE variable" % (mod_name, key, key))
            setattr(pp.hoc, key, value)

        return pp

    def _append_pp(self, hoc_point_process, mod_name, segment, tag=None):
        sec_name = "%s(%s)" % (segment.sec.name(), segment.x)
        current_mod_name = "%s_%s" % (mod_name, segment.sec.name())

        result_name = "%s[%s]" % (sec_name, self._pp_num[current_mod_name])
        self._pp_num[current_mod_name] += 1

        if tag:
            result_name = "%s[%s]" % (result_name, tag)

        pp = PointProcess(hoc_point_process, seg=segment, name=result_name, mod_name=mod_name, cell=self)
        self.pps.append(pp)
        return pp
