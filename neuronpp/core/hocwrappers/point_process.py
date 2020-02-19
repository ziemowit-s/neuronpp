from neuronpp.core.hocwrappers.seg import Seg
from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper


class PointProcess(HocWrapper):
    def __init__(self, hoc_obj, name, parent: Seg, cell, mod_name):
        HocWrapper.__init__(self, hoc_obj=hoc_obj, parent=parent, name=name)
        self.seg = parent
        self.mod_name = mod_name
        self.cell = cell

    def __repr__(self):
        return "{}+{}+{}+{}".format(self.parent, self.__class__.__name__, self.mod_name, self.name)
