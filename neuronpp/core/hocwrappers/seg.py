from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper


class Seg(HocWrapper):
    def __init__(self, obj, parent):
        HocWrapper.__init__(self, hoc_obj=obj, parent=parent, name=str(obj))

    @property
    def area(self) -> float:
        return self.hoc.area()

    @property
    def x(self) -> float:
        return self.hoc.x
