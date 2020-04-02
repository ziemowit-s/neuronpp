from neuron import h
from collections import defaultdict

from neuronpp.core.cells.section_cell import SectionCell
from neuronpp.core.hocwrappers.point_process import PointProcess
from neuronpp.core.hocwrappers.seg import Seg


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
           cell.filter_secs(obj_filter=lambda o: 'apic' in o.name or h.distance(soma.hoc(0.5), o.hoc(0.5)) > 1000)
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

    def add_point_process(self, mod_name: str, seg, tag: str = None, **point_process_params):
        """
        :param mod_name:
        :param seg:
            Segment where to put point process. If section is provided the default loc will be sec(0.5)
            Can be only Seg object.
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
        if not isinstance(seg, Seg):
            raise TypeError("Param 'segment' can be only Seg object, but provided %s" % seg.__class__)

        hoc_pp = pp_obj(seg.hoc)
        pp = self._append_pp(hoc_point_process=hoc_pp, mod_name=mod_name, segment=seg, tag=tag)

        for key, value in point_process_params.items():
            if not hasattr(pp.hoc, key):
                raise LookupError("Point Process of type %s has no attribute of type %s. "
                                  "Check if MOD file contains %s as a RANGE variable" % (mod_name, key, key))
            setattr(pp.hoc, key, value)

        return pp

    def _append_pp(self, hoc_point_process, mod_name, segment, tag=None):
        seg_name = "%s(%s)" % (segment.parent.name, segment.hoc.x)
        current_mod_name = "%s_%s" % (mod_name, segment.parent.name)

        result_name = "%s[%s][%s]" % (mod_name, seg_name, self._pp_num[current_mod_name])
        self._pp_num[current_mod_name] += 1

        if tag:
            result_name = "%s[%s]" % (result_name, tag)

        pp = PointProcess(hoc_point_process, parent=segment, name=result_name, mod_name=mod_name, cell=self)
        self.pps.append(pp)
        return pp
