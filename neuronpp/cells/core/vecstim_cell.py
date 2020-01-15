from neuronpp.cells.core.cell import Cell
from neuronpp.cells.core.utils import get_vecstim
from neuronpp.hocs.vector import Vector
from neuronpp.hocs.vecstim import VecStim


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
