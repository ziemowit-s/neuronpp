class NeuronRemovable:
    def remove_from_neuron(self):
        """
        Removes this object and all its components from NEURON.
        then delete it completely from the Python.
        """
        for k, v in self.__dict__.items():
            if hasattr(v, "remove_from_neuron"):
                getattr(v, "remove_from_neuron")()
            if hasattr(v, "__del__"):
                getattr(v, "__del__")()
            del v
        self.__dict__ = {}
        del self

    def __del__(self):
        self.remove_from_neuron()
