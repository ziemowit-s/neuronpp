import os

from neuron import h
from neuronpp.core.cells.point_process_cell import PointProcessCell
from nrn import Section

from neuronpp.core.hocwrappers.sec import Sec
from neuronpp.core.cells.section_cell import SectionCell
from neuronpp.core.hocwrappers.seg import Seg


class CoreHocCell(PointProcessCell):
    def __init__(self, name, compile_paths=None):
        SectionCell.__init__(self, name, compile_paths=compile_paths)
        self._hoc_loaded = False

    def load_hoc(self, hoc_file, cell_template_name: str = None, reinitialize=True):
        """
        This method allows to load a single cell to your model. It is experimental function so may not work stable.
        It is useful when loading a hoc file with a single cell declaration.
        It is currently intented to use it only once per object, otherwise may produce errors
        :param hoc_file:
            paths to hoc file
        :param cell_template_name:
            the name of the cell template. Default is None meaning that all sections are defined in the plain h.* object
        :param reinitialize:
            reinitialize NEURON after HOC import. Some HOC files perform computation, to avoid problems with
            eg. NetStim definition it is recommended to reinitialize NEURON after HOC import
        """
        if self._hoc_loaded:
            raise RuntimeError("make_hoc() function can be called only once per Cell object and it have been called earlier.")

        if not os.path.isfile(hoc_file):
            raise FileNotFoundError("There is no HOC file %s." % hoc_file)

        h.load_file(hoc_file)
        if reinitialize:
            h.finitialize()

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
        def get_sec_list_objects(f):
            is_section_list = False
            if "SectionList" in str(f):
                secs = [i for i in f]
                for i, hoc_sec in enumerate(secs):
                    if not get_sec_list_objects(f=hoc_sec):
                        self._add_sec(result, hoc_sec)
                    is_section_list = True
            return is_section_list

        result = {}
        for d in dir(obj):
            try:
                if d.startswith("_") or d == 'h':
                    continue
                f = getattr(obj, d)

                if isinstance(f, Section):
                    hoc_sec = f
                    self._add_sec(result, hoc_sec)
                else:
                    get_sec_list_objects(f=f)

            except (TypeError, IndexError):
                continue

        return result

    def _add_sec(self, result, hoc_sec):
        if str(hoc_sec) not in result:
            obj_sec = self._append_sec_and_point_processes(hoc_sec)
            result[str(hoc_sec)] = obj_sec

    def _append_sec_and_point_processes(self, hoc_sec_obj):
        pps = hoc_sec_obj.psection()['point_processes']
        if len(pps) > 0:
            for mod_name, hoc_obj in pps.items():
                try:
                    loc = list(hoc_obj)[0].get_segment().x
                    seg = Seg(obj=hoc_sec_obj(loc), parent=hoc_sec_obj, name="%s(%s)" % (hoc_sec_obj.name(), loc))
                    self._append_pp(hoc_point_process=list(hoc_obj)[0], mod_name=mod_name, segment=seg)
                except Exception as e:
                    print("Error while trying to retrieve PointProcess. This is en experimental feature, error %s" % e)

        sec_name = hoc_sec_obj.name()
        if len(self.filter_secs(sec_name)) > 0:
            raise LookupError("The name '%s' is already taken by another section of the cell: '%s' of type: '%s'."
                              % (sec_name, self.name, self.__class__.__name__))
        sec = Sec(hoc_sec_obj, cell=self, name=sec_name)
        self.secs.append(sec)
        return sec
