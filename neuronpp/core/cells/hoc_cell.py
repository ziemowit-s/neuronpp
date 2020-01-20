from neuron import h
from neuronpp.core.cells.point_process_cell import PointProcessCell
from nrn import Section

from neuronpp.core.hocwrappers.sec import Sec
from neuronpp.core.cells.section_cell import SectionCell


class HocCell(PointProcessCell):
    def __init__(self, name):
        SectionCell.__init__(self, name)
        self._hoc_loaded = False

    def make_hoc(self, hoc_file, cell_template_name: str = None):
        """
        This method allows to load a single cell to your model. It is experimental function so may not work stable.
        It is useful when loading a hoc file with a single cell declaration.
        It is currently intented to use it only once per object, otherwise may produce errors
        :param hoc_file:
            paths to hoc file
        :param cell_template_name:
            the name of the cell template. Default is None meaning that all sections are defined in the plain h.* object
        """
        if self._hoc_loaded:
            raise RuntimeError("make_hoc() function can be called only once per Cell object and it have been called earlier.")

        h.load_file(hoc_file)

        obj = h
        if cell_template_name:
            if not hasattr(h, cell_template_name):
                raise AttributeError("Hoc main object 'h' has no template of '%s'." % cell_template_name)

            obj = getattr(h, cell_template_name)

            if len(obj) == 0:
                raise LookupError("Hoc main object 'h' has no template '%s' created, hovewer it was defined." % cell_template_name)
            if len(obj) > 1:
                raise LookupError("Hoc main object 'h' has %s objects of template '%s', hovewer currently this mechanisms support "
                                  "a only single template object creation in Hoc." % (len(obj), cell_template_name))
            obj = obj[0]

        result = self._add_new_sections(obj)
        self._hoc_loaded = True
        return result

    def _add_new_sections(self, obj):
        result = []
        for d in dir(obj):
            try:
                if d.startswith("_") or d == 'h':
                    continue
                f = getattr(obj, d)

                if isinstance(f, Section):
                    sec = self._append_sec_and_point_processes(f)
                    result.append(sec)

                elif len(f) > 0 and isinstance(f[0], Section):
                    for ff in f:
                        sec = self._append_sec_and_point_processes(ff)
                        result.append(sec)

            except (TypeError, IndexError):
                continue
        return result

    def _append_sec_and_point_processes(self, hoc_sec_obj):
        pps = hoc_sec_obj.psection()['point_processes']
        if len(pps) > 0:
            for mod_name, hoc_obj in pps.items():
                self._append_pp(hoc_point_process=hoc_obj, mod_name=mod_name, single_sec=hoc_sec_obj)

        sec = Sec(hoc_sec_obj, parent=self, name=hoc_sec_obj.name())
        self.secs.append(sec)
        return sec
