from neuronpp.hocs.hoc import Hoc


class Synapse(Hoc):
    def __init__(self, obj, parent, name):
        Hoc.__init__(self, obj, parent=parent, name=name)
