import nrn

from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper


class Seg(HocWrapper):
    def __init__(self, obj: nrn.Segment, parent):
        # force change all comas to dots
        # for native systems where coma is utilize as decimal the name is inconsistent with x loc
        name = str(obj).replace(",", ".")
        HocWrapper.__init__(self, hoc_obj=obj, parent=parent, name=name)

    @property
    def area(self) -> float:
        return self.hoc.area()

    @property
    def L(self) -> float:
        # because NEURON's segment has always 1 and 0 locations with area=0 and L=0
        # we discard them from the count
        return self.parent.hoc.L / (len(self.parent.segs) - 2)

    @property
    def diam(self) -> float:
        return self.hoc.diam

    @property
    def Ra(self) -> float:
        return self.parent.hoc.Ra

    @property
    def x(self) -> float:
        return self.hoc.x
