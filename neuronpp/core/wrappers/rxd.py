from neuronpp.core.wrappers.hoc import Hoc


class RxD(Hoc):
    def __init__(self, hoc_obj, parent, name):
        Hoc.__init__(self, hoc_obj=hoc_obj, parent=parent, name=name)
