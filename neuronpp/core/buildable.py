import queue
from copy import deepcopy


class Buildable:
    def __init__(self, build_on_the_fly=True):
        if not hasattr(self, "_build_on_the_fly"):
            self._build_on_the_fly = build_on_the_fly
            self._builds = []

    def build(self):
        result = []
        if not self._build_on_the_fly:
            for func, args, kwargs in self._builds:
                r = func(self, *args, **kwargs)
                result.append(r)

        self._builds = []
        self._build_on_the_fly = True
        return result

    def __deepcopy__(self, memo):
        builds = self._builds
        deepcopy_func = self.__deepcopy__

        self._builds = None
        self.__deepcopy__ = None

        cp = deepcopy(self)

        cp._builds = builds
        self._builds = builds

        cp.__deepcopy__ = deepcopy_func
        self.__deepcopy__ = deepcopy_func

        return cp
