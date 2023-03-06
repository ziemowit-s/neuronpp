import nrn
import numpy as np

from neuronpp.core.hocwrappers.hoc_wrapper import HocWrapper


def get_lambda(diam, Ra, Rm=None, g_pas=None, tau_m=None, cm=1):
    """
    :param diam:
        um
    :param Ra:
        Ohm cm
    :param Rm:
        Ohm cm^2
    :param g_pas:
        S/cm2
    :param tau_m:
        ms
    :param cm:
    :return:
        electrotonic length in um
    """
    if Ra is None and g_pas is None and tau_m is None:
        raise ValueError("You must specify Ra or g_pas or tau_m")

    if tau_m is not None:
        g_pas = (cm / tau_m) * 1e-3

    if g_pas is not None:
        Rm = 1 / g_pas

    return np.sqrt(((diam / 1e4) * Rm) / (4 * Ra)) * 1e4


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
        result = False
        if self.area > 0 and hasattr(self.hoc, name) and \
                isinstance(getattr(self.hoc, name), nrn.Mechanism):
            # area check is required for custom created cell: if children section is
            # connected to different parent_loc than 0.0 or 1.0, then the children_loc
            # copies parent mechanisms, eg. if:
            # cell.connect_secs(child=trunk, parent=soma, parent_loc=0.5)
            # then trunk(1) has the same mechanisms as soma(0.5)

            if '_ion' not in name:
                # to not confuse real mechanism with ion name
                result = True

        return result

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
            raise ValueError("Segment with area 0 have no length")
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

    @property
    def electrotonic_L(self):
        """

        :return:
            length of the segment normalized by lambda
        """
        if self.area == 0:
            raise ValueError("Segment with area 0 have no electrotonic length")
        if not self.has_mechanism("pas"):
            raise ValueError("Segment must have 'pas' mechanism "
                             "in order to get electrotonic length")
        return self.L / self.get_lambda()

    def get_lambda(self):
        """

        :return:
            lambda value in um
        """
        return get_lambda(diam=self.diam, Ra=self.Ra, g_pas=self.get_mechanism("pas").g)

