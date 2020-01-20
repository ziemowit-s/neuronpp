import random
from random import randint

from neuronpp.core.cells.section_cell import SectionCell
from neuronpp.core.hocwrappers.sec import Sec


class SpineCell(SectionCell):
    def __init__(self, name=None):
        SectionCell.__init__(self, name)
        self.heads = []
        self.necks = []

    def make_spines(self, spine_number, sec: str = None, head_nseg=2, neck_nseg=2, seed: int = None):
        """
        Currently the only supported spine distribution is random_uniform

        Single spine is 2 x cylinder:
          * head: L=1um diam=1um
          * neck: L=0.5um diam=0.5um

        :param spine_number:
            The number of spines to make
        :param sec:
        :param head_nseg
        :param neck_nseg
        :param seed:
            seed int for random uniform distribution of the spines.
        :return:
            list of added spine heads
        """
        if isinstance(sec, str) or sec is None:
            sec = self.filter_secs(name=sec)

        if seed:
            random.seed(seed)
        for i in range(spine_number):
            head = self.make_sec(name="head[%s]" % i, diam=1, l=1, nseg=head_nseg)
            neck = self.make_sec(name="neck[%s]" % i, diam=0.5, l=0.5, nseg=neck_nseg)
            self.heads.append(head)
            self.necks.append(neck)
            self.connect_secs(source=head, target=neck)
            self._connect_necks_rand_uniform(neck, sec)

        return self.heads, self.necks

    @staticmethod
    def _connect_necks_rand_uniform(neck: Sec, sections):
        """
        Connect necks list to sections list with uniform random distribution
        :param neck:
        :param sections:
        """
        max_l = int(sum([s.hoc.L for s in sections]))
        added = dict([(s.hoc.name(), []) for s in sections])

        i = 0
        r = randint(0, max_l)
        for s in sections:
            s = s.hoc
            i += s.L
            if i > r:
                loc = (r - i + s.L) / s.L
                if loc in added[s.name()]:
                    break
                neck.hoc.connect(s(loc), 0.0)
                added[s.name()].append(loc)
                break
