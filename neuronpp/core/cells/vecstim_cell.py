from neuron import h

from neuronpp.core.cells.core_cell import CoreCell
from neuronpp.core.cells.utils import get_vecstim
from neuronpp.core.hocwrappers.vecstim import VecStim
from neuronpp.core.hocwrappers.vector import Vector


class VecStimCell(CoreCell):
    def __init__(self, name=None):
        CoreCell.__init__(self, name)
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

    def make_vecstim(self, ping_array):
        """
        :param ping_array
            numpy array when ping must start
        """
        if h.t > 0:
            raise ConnectionRefusedError("NetStim cannot be created after simulation have been initiated. "
                                         "You need to specify NetStim before creation of SimRun object.")
        vs_hoc, vec_hoc = get_vecstim(ping_array)
        name = str(len(self.vss))
        vs = VecStim(vs_hoc, parent=self, name=name)
        vec = Vector(vec_hoc, parent=self, name=name)

        self.vss.append(vs)
        self.vecs.append(vec)
        return vs
