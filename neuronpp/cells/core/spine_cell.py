from random import randint

from neuronpp.cells.core.basic_cell import BasicCell


class SpineCell(BasicCell):
    def __init__(self, name):
        BasicCell.__init__(self, name)
        self.heads = []
        self.necks = []

    def add_spines(self, spine_number, sections, head_nseg=2, neck_nseg=2):
        """
        Single spine is 2 x cylinder:
          * head: L=1um diam=1um
          * neck: L=0.5um diam=0.5um

        :param spine_number:
            The number of spines to create
        :param sections:
            list of sections or string defining single section name or sections names separated by space
            param 'all' - takes all sections
        :param head_nseg
        :param neck_nseg
        """
        if sections == 'all':
            sections = self.secs
        else:
            sections = self.filter_secs(sections)
        sections = sections.values()

        for i in range(spine_number):
            head = self.add_sec(name="head[%s]" % i, diam=1, l=1, nseg=head_nseg)
            neck = self.add_sec(name="neck[%s]" % i, diam=0.5, l=0.5, nseg=neck_nseg)
            self.heads.append(head)
            self.necks.append(neck)
            self.connect_secs(source='head[%s]' % i, target='neck[%s]' % i)
            self._connect_necks_rand_uniform(neck, sections)

    @staticmethod
    def _connect_necks_rand_uniform(necks, sections):
        """
        Connect necks list to sections list with uniform random distribution
        :param necks:
        :param sections:
        """
        max_l = int(sum([s.L for s in sections]))
        added = dict([(s.name(), []) for s in sections])

        i = 0
        r = randint(0, max_l)
        for s in sections:
            i += s.L
            if i > r:
                loc = (r - i + s.L) / s.L
                if loc in added[s.name()]:
                    break
                necks.connect(s(loc), 0.0)
                added[s.name()].append(loc)
                break
