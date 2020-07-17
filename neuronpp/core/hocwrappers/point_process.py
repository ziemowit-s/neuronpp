from neuronpp.core.hocwrappers.seg import Seg
from neuronpp.core.decorators import non_removable_fields
from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper


@non_removable_fields("seg", "cell")
class PointProcess(HocWrapper):
    def __init__(self, hoc_obj, name, parent: Seg, cell, mod_name):
        HocWrapper.__init__(self, hoc_obj=hoc_obj, parent=parent, name=name)
        self.seg = parent
        self.cell = cell
        self.mod_name = mod_name

    def __repr__(self):
        return "{}+{}+{}+{}".format(self.parent, self.__class__.__name__, self.mod_name, self.name)
