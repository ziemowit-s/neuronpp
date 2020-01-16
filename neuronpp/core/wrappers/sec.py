from neuronpp.core.wrappers.hoc import Hoc


class Sec(Hoc):
    def __init__(self, obj, parent, name):
        Hoc.__init__(self, hoc_obj=obj, parent=parent, name=name)
