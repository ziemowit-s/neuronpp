from typing import List, Callable

from neuronpp.core.hocwrappers.wrapper import Wrapper
from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper


class GroupHocWrapper(Wrapper, dict):
    def __init__(self, objs: List[HocWrapper], name: str,
                 key_func: Callable[[HocWrapper], str] = lambda o: o.name):
        """
        HocWrapper is a wrapper for a single HOC object.

        :param objs:
            a list of HOCWrapper objects
        :param name:
            string name of this HOC object
        :param key_func:
            a function which defines a string key for the name of each object. Default is obj.name.
            over each string a dictionary entry will be created, containing a list()
            of objects with the same string as entry.
        """
        for o in objs:
            val = key_func(o)
            if val not in self:
                self[val] = []
            self[val].append(o)

        Wrapper.__init__(self, parent=None, name=name)

