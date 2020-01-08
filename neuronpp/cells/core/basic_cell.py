from os import path

from neuron import h

from neuronpp.cells.core.cell import Cell

h.load_file('stdlib.hoc')
h.load_file('import3d.hoc')


class BasicCell(Cell):
    def __init__(self, name):
        """
        :param name:
            Name of the cell
        """
        Cell.__init__(self, name)
        # if Cell (named core_cell) have been built before on the stack of super() objects
        if not hasattr(self, '_core_cell_builded'):
            self.secs = {}
            self._core_cell_builded = True

    def filter_secs(self, sec_names=None, as_list=False):
        """
        :param sec_names:
            List of string names as list or separated by space.
            Filter will look for obj_dict keys which contains each sec_name.
            None or 'all' will return all sections.
        :param as_list:
            if return as list. Otherwise will return as dict with name as key
        :return
            dict[sec_name] = sec
        """
        return self._filter_obj_dict("secs", names=sec_names, as_list=as_list)

    def get_sec_types(self):
        return set([s.split('[')[0] for s in self.filter_secs(None)])

    def add_sec(self, name, diam=None, l=None, nseg=1):
        """

        :param name:
        :param diam:
        :param l:
        :param nseg:
        :return:
        """
        sec = h.Section(name=name, cell=self)
        sec.L = l
        sec.diam = diam
        sec.nseg = nseg
        self.secs[name] = sec
        return sec

    def connect_secs(self, source, target, source_loc=1.0, target_loc=0.0):
        """default: source(0.0) -> target(1.0)"""
        target_loc = float(target_loc)
        source_loc = float(source_loc)
        source = list(self.filter_secs(source).values())[0]
        target = list(self.filter_secs(target).values())[0]
        source.connect(target(source_loc), target_loc)

    def load_morpho(self, filepath, seg_per_L_um=1.0, add_const_segs=11):
        """
        :param filepath:
            swc file path
        :param seg_per_L_um:
            how many segments per single um of L, Length.  Can be < 1. None is 0.
        :param add_const_segs:
            how many segments have each section by default.
            With each um of L this number will be increased by seg_per_L_um
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

        morpho.input(filepath)
        h.Import3d_GUI(morpho, 0)
        i3d = h.Import3d_GUI(morpho, 0)
        i3d.instantiate(self)

        # add all SWC sections to self.secs; self.all is defined by SWC import
        new_secs = {}
        for sec in self.all:
            name = sec.name().split('.')[-1]  # eg. name="dend[19]"
            new_secs[name] = sec

        # change segment number based on seg_per_L_um and add_const_segs
        for sec in new_secs.values():
            add = int(sec.L * seg_per_L_um) if seg_per_L_um is not None else 0
            sec.nseg = add_const_segs + add

        self.secs.update(new_secs)
        del self.all

    def set_cell_position(self, x, y, z):
        h.define_shape()
        for sec in self.secs.values():
            for i in range(sec.n3d()):
                sec.pt3dchange(i,
                               x - sec.x3d(i),
                               y - sec.y3d(i),
                               z - sec.z3d(i),
                               sec.diam3d(i))

    def rotate_cell_z(self, theta):
        h.define_shape()
        """Rotate the cell about the Z axis."""
        for sec in self.secs.values():
            for i in range(sec.n3d()):
                x = sec.x3d(i)
                y = sec.y3d(i)
                c = h.cos(theta)
                s = h.sin(theta)
                xprime = x * c - y * s
                yprime = x * s + y * c
                sec.pt3dchange(i, xprime, yprime, sec.z3d(i), sec.diam3d(i))

