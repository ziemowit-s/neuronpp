from typing import Optional, List, Callable

from neuronpp.core.hocwrappers.wrapper import Wrapper
from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper


class GroupHocWrapper(Wrapper, dict):
    def __init__(self, name: str,
                 key_func: Callable[[HocWrapper], str] = lambda o: o.name,
                 *objs: List[HocWrapper]):
        """
        HocWrapper is a wrapper for a single HOC object.

        :param name:
            string name of this HOC object
        :param key_func:
            a function which defines a string key for the name of each object. Default is obj.name.
            over each string a dictionary entry will be created, containing a list()
            of objects with the same string as entry.
        :param objs:
            a list of HOCWrapper objects
        """
        parent = None
        for o in objs:
            if not isinstance(o, HocWrapper):
                raise TypeError("All objects must derived from HocWrapper")
            if parent is None:
                parent = o.parent
            else:
                if o.parent.name != parent.name:
                    raise TypeError("All objects must have the same parent.")

            if key_func(o) not in self:
                self[key_func(o)] = []
            self[key_func(o)].append(o)

        Wrapper.__init__(self, parent=parent, name=name)

