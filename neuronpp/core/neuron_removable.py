from typing import List

NON_REMOVABLE_FIELD_NAME = "_non_removable_fields"


class NeuronRemovable:
    def remove_immediate_from_neuron(self):
        """
        Removes this (self) object's fields from the Python and all its components from the NEURON.

        By default calling remove_immediate_from_neuron() method or deleting object will remove all
        its fields (attributes) of the object, however by decorating class with
        @non_removable_field() you can specify fields not to remove:

        eg. if you don't want to remove fields of cell in MySec object add on top of the class:

            @non_removable_field("cell")
            class MySec(NeuronRemovable):
                ...

        After using remove_immediate_from_neuron() method all references to this object won't work
        any more, so you need to also set a new value to any reference to the self object, eg.

            cell = Cell()
            cell.remove_from_neuron()
            cell = None

        WARNING: the only guaranteed method for on demand deletion is calling the method
        remove_immediate_from_neuron(), if you delete the reference (eg. del obj) or assign a new
        value to the reference (obj = None) the deletion may not work on demand (immediate) but
        rather when the Python's garbage collector starts.

        So methods below may not work on demand, it depends of the garbage collector:
            1. You can also make regular deletion like:
               cell = Cell()
               del cell
            2. Or reset reference to None:
               cell = Cell()
               cell = None
        """
        noremove = None
        if hasattr(self, NON_REMOVABLE_FIELD_NAME):
            noremove = getattr(self, NON_REMOVABLE_FIELD_NAME)
            if noremove is not None:
                if not isinstance(noremove, List):
                    raise AttributeError("%s can be None or List[str]." % NON_REMOVABLE_FIELD_NAME)
                elif len(noremove) > 0 and not isinstance(noremove[0], str):
                    raise AttributeError("%s can be None or List[str]." % NON_REMOVABLE_FIELD_NAME)
        
        for k, v in self.__dict__.items():
            if noremove and k in noremove:
                continue

            if hasattr(v, "remove_from_neuron"):
                getattr(v, "remove_from_neuron")()
            elif hasattr(v, "__del__"):
                getattr(v, "__del__")()
            setattr(self, k, None)
        self.__dict__ = {}

    def __del__(self):
        self.remove_immediate_from_neuron()
