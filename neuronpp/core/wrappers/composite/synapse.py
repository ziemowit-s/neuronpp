from neuronpp.core.wrappers.hoc import Hoc


class Synapse:
    def __init__(self, obj, parent, name):
        Hoc.__init__(self, obj, parent=parent, name=name)
