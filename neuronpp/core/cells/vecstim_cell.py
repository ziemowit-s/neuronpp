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

    def filter_vecstims(self, name: str, obj_filter=None, **kwargs):
        """
        Currently all filter passed are treated as AND statements.

        * Whole object callable function passed to the obj_filter param.
            eg. (lambda expression) returns sections which name contains 'apic' or their distance > 1000 um from the soma:
          ```
           soma = cell.filter_secs("soma")
           cell.filter_secs(obj_filter=lambda o: 'apic' in o.name or h.distance(soma.hoc(0.5), o.hoc(0.5)) > 1000)
          ```

        * Single object field filter based on callable function passed to the obj_filter param.
          eg. (lambda expression) returns sections which parent's name contains less than 10 characters
          ```
          cell.filter_secs(parent=lambda o: len(o.parent.name) < 10)
          ```

        :param name:
            start with 'regex:any pattern' to use regular expression. If without 'regex:' - will look which Hoc objects contain the str
        :param obj_filter:
            Whole object callable functional filter. If you added also any kwargs they will be together with the
            obj_filter treated as AND statement.
        :return:
        """
        return self.filter(searchable=self.vss, obj_filter=obj_filter, names=name, **kwargs)

    def filter_vectors(self, name: str, obj_filter=None, **kwargs):
        """
        Currently all filter passed are treated as AND statements.

        * Whole object callable function passed to the obj_filter param.
            eg. (lambda expression) returns sections which name contains 'apic' or their distance > 1000 um from the soma:
          ```
           soma = cell.filter_secs("soma")
           cell.filter_secs(obj_filter=lambda o: 'apic' in o.name or h.distance(soma(0.5), o(0.5)) > 1000)
          ```

        * Single object field filter based on callable function passed to the obj_filter param.
          eg. (lambda expression) returns sections which parent's name contains less than 10 characters
          ```
          cell.filter_secs(parent=lambda o: len(o.parent.name) < 10)
          ```
          
        :param name:
            start with 'regex:any pattern' to use regular expression. If without 'regex:' - will look which Hoc objects contain the str
        :param obj_filter:
            Whole object callable functional filter. If you added also any kwargs they will be together with the
            obj_filter treated as AND statement.
        :return:
        """
        return self.filter(self.vecs, obj_filter=obj_filter, names=name, **kwargs)

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
