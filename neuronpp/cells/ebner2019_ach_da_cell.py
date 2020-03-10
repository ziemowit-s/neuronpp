import os

from neuron import h
from neuronpp.core.hocwrappers.composed.synapse import Synapse

from neuronpp.cells.hay2011_cell import Hay2011Cell

path = os.path.dirname(os.path.abspath(__file__))
model_path1 = os.path.join(path, "..", "commons/mods/hay2011")
model_path2 = os.path.join(path, "..", "commons/mods/ebner2019")
model_path3 = os.path.join(path, "..", "commons/mods/4p_ach_da_syns")
combined_path = "%s %s %s" % (model_path1,
                              model_path2,
                              model_path3)


class Ebner2019AChDACell(Hay2011Cell):
    def __init__(self, name=None, compile_paths=combined_path):
        """
        Experimental cell of Ebner2019 rewrited to Python with ACh Da neuromodulation.

        In order to run you need to call set_synaptic_pointers() which takes 3 synapses as arguments.
        Otherwise it will generate HOC error and cause SIGKILL exit to console.
        :param name:
        """
        Hay2011Cell.__init__(self, name=name, compile_paths=compile_paths)

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

    @staticmethod
    def set_synaptic_pointers(syn_4p: Synapse, syn_ach: Synapse, syn_da: Synapse):
        """
        POINTER ach_stdp
        POINTER da_stdp
        POINTER flag_D_ACh
        POINTER flag_D_Da

        POINTER last_max_w_ACh
        POINTER last_max_w_Da
        """
        h.setpointer(syn_ach.point_process.hoc._ref_w, 'ACh_w', syn_4p.point_process.hoc)
        h.setpointer(syn_da.point_process.hoc._ref_w, 'Da_w', syn_4p.point_process.hoc)

        h.setpointer(syn_ach.point_process.hoc._ref_flag_D, 'flag_D_ACh', syn_4p.point_process.hoc)
        h.setpointer(syn_da.point_process.hoc._ref_flag_D, 'flag_D_Da', syn_4p.point_process.hoc)

        h.setpointer(syn_ach.point_process.hoc._ref_last_max_w, 'last_max_w_ACh', syn_4p.point_process.hoc)
        h.setpointer(syn_da.point_process.hoc._ref_last_max_w, 'last_max_w_Da', syn_4p.point_process.hoc)
