from neuronpp.core.neuron_removable import NeuronRemovable


class Wrapper(NeuronRemovable):
    def __init__(self, parent, name):
        self.add_non_removable_field("parent")
        try:
            self.parent = parent
        except AttributeError:
            pass
        self.name = name

    def __repr__(self):
        return "{}[{}]".format(self.__class__.__name__, self.name)
