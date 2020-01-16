from neuron import h
from nrn import Section

from neuronpp.core.cells.section_cell import SectionCell
from neuronpp.core.wrappers.sec import Sec


class HOCCell(SectionCell):
    def make_hoc(self, hoc_file, seg_per_L_um=1.0, make_const_segs=11):
        """
        :param hoc_file:
            paths to hoc file
        :param seg_per_L_um:
            how many segments per single um of L, Length.  Can be < 1. None is 0.
        :param make_const_segs:
            how many segments have each section by default.
            With each um of L this number will be increased by seg_per_L_um
        """
        h.load_file(hoc_file)

        result = []
        # add potential new Sections from hoc file to self.secs dictionary
        for d in dir(h):
            try:
                f = getattr(h, d)
                if isinstance(f, Section):
                        sec = Sec(f, parent=self, name=f.name())
                        self.secs.append(sec)
                        result.append(sec)

                        add = int(sec.hoc.L * seg_per_L_um) if seg_per_L_um is not None else 0
                        sec.hoc.nseg = make_const_segs + add

                elif len(f) > 0 and isinstance(f[0], Section):
                    for ff in f:
                        sec = Sec(f, parent=self, name=ff.name())
                        self.secs.append(sec)
                        result.append(sec)

                        add = int(sec.hoc.L * seg_per_L_um) if seg_per_L_um is not None else 0
                        sec.hoc.nseg = make_const_segs + add
            except TypeError:
                continue

        return result
