from neuron import h
from nrn import Section
import numpy as np
from neuronpp.core.hocwrappers.sec import Sec


def get_netstim(start, number, interval, noise):
    stim = h.NetStim()
    stim.start = start
    stim.number = number
    stim.interval = interval
    stim.noise = noise
    return stim


def get_vecstim(ping_array):
    stim = h.VecStim()
    vec = h.Vector(ping_array)
    stim.play(vec)

    return stim, vec


def get_spine_number(section: Sec, density, area_density=False):
    """
    Calculate expected number of spines based on section dimensions and
    spine density. This function works for both linear density and surface
    density. To specify whether linear or surface density is passed use
    are_density switch. As a default linear density is used.

    if calculated spine_number is lower than 1, Monte Carlo is used
    to establish whether a spine will be added to section.

    :param section:
        Sec
    :param density:
        linear or surface dendsity
    :area_density:
        if True density is treated as surface density. Otherwise density
        is linear density.
    :return spine_number:
        integer
    """
    if area_density:
        area = section.hoc.L*np.pi*section.hoc.diam
        spine_number = int(np.round(area * density))
    else:
        spine_number = int(np.round(section.hoc.L * density))

    # if spine density is low (less than 1 per comp)
    # use random number to determine whether to add a spine
    if not spine_number:
        rand = np.random.uniform()
        if rand > spine_number:
            return 1
        return 0
    return spine_number


def establish_electric_properties(section: Sec, spine_E_pas, spine_g_pas,
                                  spine_ra, spine_cm):
    """
    Find appropriate electric properties for a spine that will be added to
    section. If any of the spine parameters is not provided, appropriate
    section parameter is returned.

    :param section:
    :param spine_E_pas:
         Resting potential of the spine
    :param spine_g_pas:
         Spine conductance (1/R_m)
    :param spine_ra:
         Axial resistance
    :param spine_cm:
         Spine membrane conductance
    :return:
       E_pas, g_pas, ra, cm
    """
    if spine_E_pas is None:
        try:
            E_pas = section.hoc.e_pas
        except AttributeError:
            E_pas = None
    else:
        E_pas = spine_E_pas

    if spine_g_pas is None:
        try:
            g_pas = section.hoc.g_pas
        except AttributeError:
            g_pas = None
    else:
        g_pas = spine_g_pas

    if spine_ra is None:
        ra = section.hoc.Ra
    else:
        ra = spine_ra

    if spine_cm is None:
        cm = section.hoc.cm
    else:
        cm = spine_cm

    return E_pas, g_pas, ra, cm
