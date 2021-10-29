from os import path
from neuron import h
from typing import Union

from neuronpp.core.hocwrappers.sec import Sec
from neuronpp.core.decorators import distparams
from neuronpp.core.cells.core_cell import CoreCell

h.load_file('stdlib.hoc')
h.load_file('import3d.hoc')


class SectionCell(CoreCell):
    def __init__(self, name=None, compile_paths=None):
        """
        :param name:
            Name of the cell
        """
        CoreCell.__init__(self, name, compile_paths=compile_paths)
        # if Cell (named core_cell) have been built before on the stack of super() objects
        if not hasattr(self, '_core_cell_builded'):
            self.secs = []
            self._core_cell_builded = True

    def filter_secs(self, name=None, obj_filter=None, **kwargs):
        """
        Currently all filter passed are treated as AND statements.

        * Whole object callable function passed to the obj_filter param.
            eg. (lambda expression) returns sections which name contains 'apic' or
            their distance > 1000 um from the soma:
          ```
           soma = cell.filter_secs("soma")
           cell.filter_secs(obj_filter=lambda o: 'apic' in o.name or h.distance(soma.hoc(0.5),
                                                o.hoc(0.5)) > 1000)
          ```

        * Single object field filter based on callable function passed to the obj_filter param.
          eg. (lambda expression) returns sections which parent's name contains less than 10
          characters
          ```
          cell.filter_secs(parent=lambda o: len(o.parent.name) < 10)
          ```

        :param name:
            start with 'regex:any pattern' to use regular expression. If without 'regex:'
             will look which Hoc objects contain the str
        :param obj_filter:
            Whole object callable functional filter. If you added also any kwargs they will be
            together with the
            obj_filter treated as AND statement.
        :return:
        """
        return self.filter(searchable=self.secs, obj_filter=obj_filter, name=name, **kwargs)

    def remove_secs(self, name=None, obj_filter=None, **kwargs):
        """
        Currently all filter passed are treated as AND statements.

        * Whole object callable function passed to the obj_filter param.
            eg. (lambda expression) returns sections which name contains 'apic' or
            their distance > 1000 um from the soma:
          ```
           soma = cell.filter_secs("soma")
           cell.filter_secs(obj_filter=lambda o: 'apic' in o.name or h.distance(soma.hoc(0.5),
                                                o.hoc(0.5)) > 1000)
          ```

        * Single object field filter based on callable function passed to the obj_filter param.
          eg. (lambda expression) returns sections which parent's name contains less than 10
          characters
          ```
          cell.filter_secs(parent=lambda o: len(o.parent.name) < 10)
          ```

        :param name:
            start with 'regex:any pattern' to use regular expression. If without 'regex:'
             will look which Hoc objects contain the str
        :param obj_filter:
            Whole object callable functional filter. If you added also any kwargs they will be
            together with the
            obj_filter treated as AND statement.
        """
        self.remove(searchable=self.secs, obj_filter=obj_filter, name=name, **kwargs)

    def insert(self, mechanism_name: str, sec=None, **params):
        if isinstance(sec, Sec):
            sec = [sec]
        elif sec is None or isinstance(sec, str):
            sec = self.filter_secs(name=sec, as_list=True)

        for s in sec:
            s.hoc.insert(mechanism_name)
            for name, val in params.items():
                for seg in s.hoc:
                    mech = getattr(seg, mechanism_name)
                    setattr(mech, name, val)
        return self

    @distparams
    def set_pas(self, section, Rm=None, g_pas=None, E_rest=None):
        if isinstance(section, str):
            section_list = self.filter_secs(name=section, as_list=True)
        elif isinstance(section, Sec):
            section_list = [section]
        else:
            section_list = [Sec(section, cell=self, name=section.name)]

        # Set any non-default parameters
        for n_sec in section_list:
            if E_rest is not None:
                n_sec.hoc.e_pas = E_rest
            if Rm is not None:
                n_sec.hoc.g_pas = 1 / Rm
            if g_pas is not None:
                n_sec.hoc.g_pas = g_pas

    @distparams
    def add_sec(self, name: str, diam: float = None, l: float = None, rm: float = None,
                g_pas: float = None, E_rest: float = None, ra: float = None, cm: float = None,
                nseg: int = None, add_pas: bool = False):
        """
        Create a new section.

        :param name:
            str name of the section. If the name already exists - the number (as a str)
            will be added, eg. if name "dend" exists it will creates "dend1"
        :param diam:
        :param l:
        :param rm:
        :param g_pas:
        :param E_rest:
        :param ra:
        :param cm:
        :param nseg:
        :param add_pas:
        :return:
            newly created section as a wrapper object Sec
        """
        if name is None:
            raise ValueError("Section's name cannot be None.")

        num_name = len(self.filter_secs(name=name, as_list=True))
        if num_name > 0:
            name = "%s%s" % (name, num_name + 1)

        hoc_sec = h.Section(name=name, cell=self)
        if l is not None:
            hoc_sec.L = l
        if diam is not None:
            hoc_sec.diam = diam
        if nseg is not None:
            hoc_sec.nseg = nseg
        if cm is not None:
            hoc_sec.cm = cm
        if ra is not None:
            hoc_sec.Ra = ra
        if rm is not None:
            g_pas = 1 / rm

        if add_pas is True or g_pas is not None or E_rest is not None:
            hoc_sec.insert('pas')
            self.set_pas(hoc_sec, E_rest=E_rest, g_pas=g_pas)

        if len(self.filter_secs(name, as_list=True)) > 0:
            raise LookupError(
                "The name '%s' is already taken by another section of the cell: '%s' of type: '%s'."
                % (name, self.name, self.__class__.__name__))
        sec = Sec(hoc_sec, cell=self, name=name)
        self.secs.append(sec)
        return sec

    @distparams
    def connect_secs(self, child: Union[Sec, str], parent: Union[Sec, str], child_loc: float = 1.0,
                     parent_loc: float = 0.0):
        """
        child_loc can be: [0 or 1]
        parent_loc can be: between [0 and 1]

        default: child.connect(parent(0.0), [0 or 1])

        If you specify 1.0 for source_loc or target_loc it will assume 0.999 loc instead.
        This is because NEURON do not insert any mechanisms to the 1.0 end (it is dimension-less).

        NEURON allows to connect section to the 1.0, however this raise problems while copying
        parameters between sections. So any 1.0 loc will be changed to 0.999 instead.

        :param child:
            child section
        :param parent:
            parent section
        :param child_loc:
            source location. Can be 1 or 0, representing both ends of child section. Default is 1.0
        :param parent_loc:
            target location. It must be between 0 and 1. Default is 0.0
        :return:
        """
        if child_loc != 1 and child_loc != 0:
            raise ValueError("child_loc must [0 or 1]")
        if parent_loc > 1.0 or parent_loc < 0.0:
            raise ValueError("parent_loc must be in range [0, 1]")

        if child is None or parent is None:
            raise LookupError("source and target must be specified. Can't be None.")

        if isinstance(child, str):
            child = self.filter_secs(name=child)
            if isinstance(child, list):
                raise LookupError("To connect sections source name must return exactly 1 Section, "
                                  "but returned %s elements for name=%s" % (len(child), child))

        if isinstance(parent, str) or parent is None:
            parent = self.filter_secs(name=parent)
            if isinstance(parent, list):
                raise LookupError("To connect sections target name must return exactly 1 Section, "
                                  "but returned %s elements for name=%s" % (len(child), child))

        parent_loc = float(parent_loc)
        child_loc = float(child_loc)

        child.hoc.connect(parent(parent_loc).hoc, child_loc)

    def load_morpho(self, filepath):
        """
        :param filepath:
            swc or asc file path
            to load HOC-based morphology use HocCell object
        """
        if not path.exists(filepath):
            raise FileNotFoundError(filepath)

        # SWC
        fileformat = filepath.split('.')[-1]
        if fileformat == 'swc':
            morpho = h.Import3d_SWC_read()
        # Neurolucida
        elif fileformat == 'asc':
            morpho = h.Import3d_Neurolucida3()
        else:
            raise Exception('file format `%s` not recognized' % filepath)

        self.all = []
        morpho.input(filepath)
        i3d = h.Import3d_GUI(morpho, 0)
        i3d.instantiate(self)

        for hoc_sec in self.all:
            name = hoc_sec.name().split('.')[-1]  # eg. name="dend[19]"
            if len(self.filter_secs(name)) > 0:
                raise LookupError(
                    "The name '%s' is already taken by another section of the cell: '%s' of "
                    "type: '%s'." % (name, self.name, self.__class__.__name__))
            sec = Sec(hoc_sec, cell=self, name=name)
            self.secs.append(sec)

        del self.all

    @distparams
    def set_cell_position(self, x, y, z):
        h.define_shape()
        for sec in self.secs:
            for i in range(sec.n3d()):
                sec.pt3dchange(i,
                               x - sec.x3d(i),
                               y - sec.y3d(i),
                               z - sec.z3d(i),
                               sec.diam3d(i))

    @distparams
    def rotate_cell_z(self, theta):
        h.define_shape()
        """Rotate the cell about the Z axis."""
        for sec in self.secs:
            for i in range(sec.n3d()):
                x = sec.x3d(i)
                y = sec.y3d(i)
                c = h.cos(theta)
                s = h.sin(theta)
                xprime = x * c - y * s
                yprime = x * s + y * c
                sec.pt3dchange(i, xprime, yprime, sec.z3d(i), sec.diam3d(i))

    def copy_mechanisms(self, secs_to, sec_from='parent'):
        """
        Copy mechanisms from the sec_from to all sections specified in the secs_to param.
        If sec_from is 'parent' it will copy mechanisms from the parent of each sections in the
        secs_to param.
        """
        for sec in secs_to:

            if sec_from == 'parent':
                segment_from = sec.hoc.psection()['morphology']['parent']
                current_sec_from = segment_from.sec
            elif isinstance(sec_from, Sec):
                current_sec_from = sec_from.hoc
                segment_from = self._get_first_segment(current_sec_from)
            else:
                raise TypeError("The param sec_from can be only type of Sec or string 'parent', "
                                "but provided %s" % sec_from)

            all_mechs = current_sec_from.psection()['density_mechs']

            if segment_from.x == 1.0:
                segment_from = current_sec_from(0.999)
            if segment_from.x == 0:
                segment_from = current_sec_from(0.001)

            for mech_name, params in all_mechs.items():
                self.insert(mech_name, sec)
                from_mech = getattr(segment_from, mech_name)

                for param_name in params.keys():
                    value = getattr(from_mech, param_name)

                    for to_segment in sec.hoc:
                        to_mech = getattr(to_segment, mech_name)

                        try:
                            setattr(to_mech, param_name, value)
                        except ValueError:
                            continue

    @staticmethod
    def _hasmech(sec: Sec, mech_name: str):
        for s in sec.hoc:
            return hasattr(s, mech_name)

    @staticmethod
    def _get_first_segment(sec: Sec):
        for s in sec.hoc:
            return s
