from neuronpp.hocs.hoc import Hoc


class Vector(Hoc):
    def __init__(self, hoc_obj, parent, name):
        Hoc.__init__(self, hoc_obj=hoc_obj, parent=parent, name=name)