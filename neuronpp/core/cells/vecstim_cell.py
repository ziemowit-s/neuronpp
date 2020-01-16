from neuronpp.core.cells.cell import Cell
from neuronpp.core.cells.utils import get_vecstim
from neuronpp.core.wrappers.vecstim import VecStim
from neuronpp.core.wrappers.vector import Vector


class VecStimCell(Cell):
    def __init__(self, name):
        Cell.__init__(self, name)
        self.vss = []
        self.vecs = []

    def filter_vecstims(self, name: str):
        """
        :param name:
            start with 'regex:any pattern' to use regular expression. If without 'regex:' - will look which Hoc objects contain the str
        :return:
        """
        return self.filter(searchable=self.vss, names=name)

    def filter_vectors(self, name: str):
        """
        :param name:
            start with 'regex:any pattern' to use regular expression. If without 'regex:' - will look which Hoc objects contain the str
        :return:
        """
        return self.filter(self.vecs, names=name)

    def add_vecstim(self, name: str, ping_array):
        """
        :param name:
        :param ping_array
            numpy array when ping must start
        :return:
            Created vecstim
        """
        vs_hoc, vec_hoc = get_vecstim(ping_array)
        name = "%s[%s]" % (name, len(self.vss))
        vs = VecStim(vs_hoc, parent=self, name=name)
        vec = Vector(vec_hoc, parent=self, name=name)

        self.vss.append(vs)
        self.vecs.append(vec)
        return vs
