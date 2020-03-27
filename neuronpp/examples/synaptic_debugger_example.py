from neuronpp.cells.ebner2019_ach_da_cell import Ebner2019AChDACell
from neuronpp.utils.synaptic_debugger import SynapticDebugger


WEIGHT = 0.0035  # From Ebner et al. 2019


if __name__ == '__main__':
    # Prepare cell
    cell = Ebner2019AChDACell("cell")
    soma = cell.add_sec("soma", diam=20, l=20, nseg=10)

    syn = cell.add_synapse(source=None, netcon_weight=WEIGHT, seg=soma(0.5),
                           mod_name="Syn4PAChDa", **cell.params_4p_syn, ACh_tau=20, Da_tau=20)

    syn_ach = cell.add_synapse(source=None, seg=soma(0.5), netcon_weight=0.1, mod_name="SynACh")
    syn_da = cell.add_synapse(source=None, seg=soma(0.5), netcon_weight=0.01, mod_name="SynDa")

    cell.set_synaptic_pointers(syn, syn_ach, syn_da)
    cell.make_default_mechanisms()

    # Debug
    debug = SynapticDebugger(init_v=-80, warmup=200)

    debug.add_syn(syn, key_press='w', syn_variables="w")
    debug.add_syn(syn_ach, key_press='a', plot=False)
    debug.add_syn(syn_da, key_press='d', plot=False)

    debug.add_seg(soma(0.5))
    debug.debug_interactive()
