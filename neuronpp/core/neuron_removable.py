from typing import List


class NeuronRemovable:
    def remove_immediate_from_neuron(self):
        """
        Removes this object's fields from the Python and all its components from the NEURON.

        Class which implements NeuronRemovable may handle fields which should not be removed
        from the NEURON by calling: add_non_removable_field(field_name: str)

        After using this method all references to this object won't work any more, so you need to
        also set a new value to any reference, eg.

           cell = Cell()
           cell.remove_from_neuron()
           cell = None

        WARNING: the only guaranteed method for on demand deletion is the above method.

        Methods below may not work on demand, it depends of the garbage collector:
        1. You can also make regular deletion like:
           cell = Cell()
           del cell
        2. Or reset reference to None:
           cell = Cell()
           cell = None
        However bear in mind that those methods will clear references and the NEURON when the
        garbage collector started to work.
        """
        noremove = None
        if hasattr(self, "_non_removable_fields"):
            noremove = self._non_removable_fields
            if noremove is not None:
                if not isinstance(noremove, List):
                    raise AttributeError("_non_removable_fields can be None or List[str].")
                elif len(noremove) > 0 and not isinstance(noremove[0], str):
                    raise AttributeError("_non_removable_fields can be None or List[str].")
        
        for k, v in self.__dict__.items():
            if noremove and k in noremove:
                continue

            if hasattr(v, "remove_from_neuron"):
                getattr(v, "remove_from_neuron")()
            elif hasattr(v, "__del__"):
                getattr(v, "__del__")()
            del v
        self.__dict__ = {}
        del self

    def add_non_removable_field(self, field_name: str):
        """
        Add fieldname which be non removable during deletion of this object.
        :param field_name:
            string name of the field
        """
        if not hasattr(self, "_non_removable_fields"):
            self._non_removable_fields = []
        self._non_removable_fields.append(field_name)

    def __del__(self):
        self.remove_immediate_from_neuron()
