from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper
from neuronpp.core.hocwrappers.sec import Sec


class Seg(HocWrapper):
    def __init__(self, obj, parent: Sec, name):
        HocWrapper.__init__(self, hoc_obj=obj, parent=parent, name=name)