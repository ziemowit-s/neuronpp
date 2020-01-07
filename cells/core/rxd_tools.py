import abc
import numpy as np
from neuron import rxd
import matplotlib.pyplot as plt
from neuron.rxd.node import Node3D
from neuron.units import nM, ms, sec


class RxDTool:
    @abc.abstractmethod
    def load(self, secs, dx_3d_size, rxds=None):
        """
        Must be called after all secs are set.
        :param secs:
        :param dx_3d_size:
            If 3D geometry is True, define the size of the single compartment size.
        :param rxds:
            dictionary which contains previously added RxDTool objects
        """
        raise NotImplementedError


class RxDCa(RxDTool):

    def load(self, secs, dx_3d_size, rxds=None):
        """
        Must be called after all secs are set.
        :param secs:
            List of sections (real HOC objects)
        :param dx_3d_size:
            If 3D geometry is True, define the size of the single compartment size.
        :param rxds:
            dictionary which contains previously added RxDTool objects
        """
        self.cyt = rxd.Region(secs=secs, nrn_region='i', dx=dx_3d_size)

        # 1/nM = 1 × 1/10^-9M = 10^3/10^3 × 1/10^-9M = 1000/(10^3×10^-9M) = 1000/10^-6M = 1000/uM

        # Ca2+
        self.ca = rxd.Species(regions=self.cyt, initial=75 * nM, name='ca', charge=2, d=174.3 / sec)

        # Calbindin buffer
        self.calbindin = rxd.Species(regions=self.cyt, initial=159982 * nM, name='calbindin', charge=0, d=9.3 / sec)
        self.calbindin_ca = rxd.Species(regions=self.cyt, initial=18 * nM, name='calbindin_ca', charge=0, d=9.3 / sec)
        self.calbindin_ca_reaction = rxd.Reaction(self.ca + self.calbindin, self.calbindin_ca, 0.028e-3 / (nM * ms),
                                                  19.6 / (nM * ms))

        # Calmodulin buffer
        self.calmodulin = rxd.Species(regions=self.cyt, initial=12600 * nM, name='calmodulin', charge=0, d=4 / sec)
        self.calmodulin_ca2 = rxd.Species(regions=self.cyt, initial=200 * nM, name='calmodulin_ca2', charge=0,
                                          d=4 / sec)
        self.calmodulin_ca4 = rxd.Species(regions=self.cyt, initial=3 * nM, name='calmodulin_ca4', charge=0, d=4 / sec)
        self.calmodulin_ca2_reaction = rxd.Reaction(2 * self.ca + self.calmodulin, self.calmodulin_ca2,
                                                    6e-6 / (nM * ms), 9.1e-3 / (nM * ms))
        self.calmodulin_ca4_reaction = rxd.Reaction(2 * self.ca + self.calmodulin_ca2, self.calmodulin_ca4,
                                                    0.1e-3 / (nM * ms), 1000e-3 / (nM * ms))


class RxDpmca(RxDTool):

    def load(self, secs, dx_3d_size, rxds=None):
        """
        Must be called after all secs are set.
        :param secs:
        :param dx_3d_size:
            If 3D geometry is True, define the size of the single compartment size.
        :param rxds:
            dictionary which contains previously added RxDTool objects
        """

        rxdca = rxds['RxDCa']

        # PMCA Pump
        self.pmca = rxd.Species(regions=rxdca.cyt, initial=760 * nM, name='pmca', charge=0, d=0)
        self.pmca_ca = rxd.Species(regions=rxdca.cyt, initial=120 * nM, name='pmca_ca', charge=0, d=0)

        self.pmca_ca_reaction = rxd.Reaction(rxdca.ca + self.pmca, self.pmca_ca, 0.05e-3 / (nM * ms), 9e-3 / (nM * ms))
        self.pmca_ca__pmca_reaction = rxd.Reaction(self.pmca_ca, self.pmca, 3.0e-3 / (nM * ms), 0)  # CaOut


class RxDncx(RxDTool):

    def load(self, secs, dx_3d_size, rxds=None):
        """
        Must be called after all secs are set.
        :param secs:
        :param dx_3d_size:
            If 3D geometry is True, define the size of the single compartment size.
        :param rxds:
            dictionary which contains previously added RxDTool objects
        """
        rxdca = rxds['RxDCa']

        # NCX Pump
        self.ncx = rxd.Species(regions=rxdca.cyt, initial=14980 * nM, name='ncx', charge=0, d=0)
        self.ncx_ca = rxd.Species(regions=rxdca.cyt, initial=120 * nM, name='ncx_ca', charge=0, d=0)

        self.ncx_ca_reaction = rxd.Reaction(rxdca.ca + self.ncx, self.ncx_ca, 0.011e-3 / (nM * ms), 11.2e-3 / (nM * ms))
        self.ncx_ca_ncx_reaction = rxd.Reaction(self.ncx_ca, self.ncx, 5.6e-3 / (nM * ms), 0)  # CaOut


def plot_contours(species: rxd.Species):
    r = species.nodes[0].region
    if not hasattr(r, '_xs'):
        raise LookupError("For RxD ionic contour plot - you must use 3D RxD model.")
    xz = np.empty((max(r._xs) + 1, max(r._zs) + 1))
    xz.fill(np.nan)

    def replace_nans(a, b):
        if np.isnan(a):
            return b
        return max(a, b)

    for node in species.nodes:
        if isinstance(node, Node3D):
            xz[node._i, node._k] = replace_nans(xz[node._i, node._k], node.value)

    xs, ys = np.meshgrid(range(xz.shape[1]), range(xz.shape[0]))
    plt.contour(xs, ys, np.nan_to_num(xz), 0.5, colors='k', linewidths=0.5)
    plt.axis('equal')
    plt.axis('off')
