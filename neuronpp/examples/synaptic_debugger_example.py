from neuronpp.cells.ebner2019_ach_da_cell import Ebner2019AChDACell
from neuronpp.utils.synaptic_debugger import SynapticDebugger

if __name__ == '__main__':
    # Prepare cell
    cell = Ebner2019AChDACell("cell")
    soma = cell.add_sec("soma", diam=20, l=20, nseg=10)

    syn = cell.add_sypanse(source=None, weight=0.0035, seg=soma(0.5), mod_name="Syn4PAChDa", **cell.params_4p_syn)
    syn_ach = cell.add_sypanse(source=None, seg=soma(0.5), weight=0.1, mod_name="SynACh")
    syn_da = cell.add_sypanse(source=None, seg=soma(0.5), weight=0.1, mod_name="SynDa")

    cell.set_synaptic_pointers(syn, syn_ach, syn_da)
    cell.make_default_mechanisms()

    # Debug
    debug = SynapticDebugger(init_v=-80, warmup=200)

    debug.add_syn(syn, key_press='w', syn_variables="w")
    debug.add_syn(syn_ach, key_press='a', plot=False)
    debug.add_syn(syn_da, key_press='d', plot=False)

    debug.add_sec(soma(0.5))
    debug.debug_interactive()
