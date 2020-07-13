from typing import Optional

from neuronpp.core.hocwrappers.wrapper import Wrapper


class HocWrapper(Wrapper):
    def __init__(self, hoc_obj, parent: Optional, name: str):
        """
        HocWrapper is a wrapper for a single HOC object.

        :param hoc_obj:
            HOC object
        :param parent:
            parent object to the hoc_obj.
            If it is a Section, the parent=None
        :param name:
            string name of this HOC object
        """
        Wrapper.__init__(self, parent=parent, name=name)
        self.hoc = hoc_obj

    def __hash__(self):
        return self.hoc.__hash__()

    def __lt__(self, other):
        return self.hoc.__lt__(other.hoc)

    def __le__(self, other):
        return self.hoc.__le__(other.hoc)

    def __eq__(self, other):
        return self.hoc.__eq__(other.hoc)

    def __ne__(self, other):
        return self.hoc.__ne__(other.hoc)

    def __gt__(self, other):
        return self.hoc.__gt__(other.hoc)

    def __ge__(self, other):
        return self.hoc.__ge__(other.hoc)

