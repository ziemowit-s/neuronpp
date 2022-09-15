import nrn

from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper


class Seg(HocWrapper):
    def __init__(self, obj: nrn.Segment, parent):
        # force change all comas to dots
        # for native systems where coma is utilize as decimal the name is inconsistent with x loc
        name = str(obj).replace(",", ".")
        HocWrapper.__init__(self, hoc_obj=obj, parent=parent, name=name)

    def has_mechanism(self, name):
        """
        If the Segment has mechanism with the name defined
        :param name:
            name of the mechanism
        """
        if self.area > 0 and hasattr(self.hoc, name):
            # area check is required for custom created cell: if children section is
            # connected to different parent_loc than 0.0 or 1.0, then the children_loc
            # copies parent mechanisms, eg. if:
            # cell.connect_secs(child=trunk, parent=soma, parent_loc=0.5)
            # then trunk(1) has the same mechanisms as soma(0.5)
            return True
        else:
            return False

    def get_mechanism(self, name):
        if self.has_mechanism(name=name):
            return getattr(self.hoc, name)
        else:
            raise ValueError(f"Segment of name: {self.name} has no mechanism of name: {name}")

    @property
    def area(self) -> float:
        return self.hoc.area()

    @property
    def L(self) -> float:
        # because NEURON's segment has always 1 and 0 locations with area=0 and L=0
        # we discard them from the count
        if self.area == 0:
            return 0
        else:
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
