from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper


class Seg(HocWrapper):
    def __init__(self, obj, parent):
        # force change all comas to dots
        # for native systems where coma is utilize as decimal the name is inconsistent with x loc
        name = str(obj).replace(",", ".")
        HocWrapper.__init__(self, hoc_obj=obj, parent=parent, name=name)

    @property
    def area(self) -> float:
        return self.hoc.area()

    @property
    def x(self) -> float:
        return self.hoc.x
