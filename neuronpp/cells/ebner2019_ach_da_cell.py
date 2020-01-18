from neuron import h
from neuronpp.core.hocwrappers.composed.synapse import Synapse

from neuronpp.cells.hay2011_cell import Hay2011Cell


class Ebner2019AChDACell(Hay2011Cell):
    def __init__(self, name=None):
        """
        In order to run you need to call set_synaptic_pointers() which takes 3 synapses as arguments.
        Otherwise it will generate HOC error and cause SIGKILL exit to console.

        :param name:
        """
        Hay2011Cell.__init__(self, name)

        self.params_ach = {"tau": 1000}
        self.params_da = {"tau": 1000}

        self.params_4p_syn = {
            "tau_a": 0.2,  # time constant of EPSP rise
            "tau_b": 2,  # time constant of EPSP decay
            "e": 0,  # reversal potential
            "w_pre_init": 0.5,  # pre factor initial value
            "w_post_init": 2.0,  # post factor initial value
            "s_ampa": 0.5,  # contribution of AMPAR currents
            "s_nmda": 0.5,  # contribution of NMDAR currents
            "tau_G_a": 2,  # time constant of presynaptic event G (rise)
            "tau_G_b": 50,  # time constant of presynaptic event G (decay)
            "m_G": 10,  # slope of the saturation function for G
            "A_LTD_pre": 3e-3,  # amplitude of pre-LTD
            "A_LTP_pre": 33e-4,  # amplitude of pre-LTP
            "A_LTD_post": 36e-5,  # amplitude of post-LTD
            "A_LTP_post": 2e-1,  # amplitude of post-LTP
            "tau_u_T": 10,  # time constant for filtering u to calculate T
            "theta_u_T": -60,  # voltage threshold applied to u to calculate T
            "m_T": 1.7,  # slope of the saturation function for T
            "theta_u_N": -30,  # voltage threshold applied to u to calculate N
            "tau_Z_a": 1,  # time constant of presynaptic event Z (rise)
            "tau_Z_b": 15,  # time constant of presynaptic event Z (decay)
            "m_Z": 6,  # slope of the saturation function for Z
            "tau_N_alpha": 7.5,  # time constant for calculating N-alpha
            "tau_N_beta": 30,  # time constant for calculating N-beta
            "m_N_alpha": 2,  # slope of the saturation function for N_alpha
            "m_N_beta": 10,  # slope of the saturation function for N_beta
            "theta_N_X": 0.2,  # threshold for N to calculate X
            "theta_u_C": -68,  # voltage threshold applied to u to calculate C
            "theta_C_minus": 15,  # threshold applied to C for post-LTD (P activation)
            "theta_C_plus": 35,  # threshold applied to C for post-LTP (K-alpha activation)
            "tau_K_alpha": 15,  # time constant for filtering K_alpha to calculate K_alpha_bar
            "tau_K_gamma": 20,  # time constant for filtering K_beta to calculate K_gamma
            "m_K_alpha": 1.5,  # slope of the saturation function for K_alpha
            "m_K_beta": 1.7,  # slope of the saturation function for K_beta
            "s_K_beta": 100,  # scaling factor for calculation of K_beta
        }

    def set_synaptic_pointers(self, syn_4p: Synapse, syn_ach: Synapse, syn_da: Synapse):
        h.setpointer(syn_ach.hoc._ref_w, 'ACh', syn_4p.hoc)
        h.setpointer(syn_da.hoc._ref_w, 'Da', syn_4p.hoc)

        h.setpointer(syn_ach.hoc._ref_flag_D, 'flag_D_ACh', syn_4p.hoc)
        h.setpointer(syn_da.hoc._ref_flag_D, 'flag_D_Da', syn_4p.hoc)

        h.setpointer(syn_ach.hoc._ref_last_max_w, 'last_max_w_ACh', syn_4p.hoc)
        h.setpointer(syn_da.hoc._ref_last_max_w, 'last_max_w_Da', syn_4p.hoc)
