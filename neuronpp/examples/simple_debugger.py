from neuronpp.cells.cell import Cell

from neuronpp.utils.synaptic_debugger import SynapticDebugger


if __name__ == '__main__':
    # Prepare cell
    cell = Cell("cell")
    soma = cell.add_sec("soma", diam=20, l=20, nseg=100)
    cell.insert("pas")
    cell.insert("hh")

    syn1 = cell.add_synapse(source=None, netcon_weight=0.002, seg=soma(0.1), mod_name="Exp2Syn")
    syn2 = cell.add_synapse(source=None, netcon_weight=0.002, seg=soma(0.9), mod_name="Exp2Syn")
    syn3 = cell.add_synapse(source=None, netcon_weight=0.002, seg=soma(0.5), mod_name="Exp2Syn")

    # Debug
    debug = SynapticDebugger(init_v=-70, warmup=10, delay_between_steps=15)
    debug.add_syn(syn1, key_press='1', plot=False)
    debug.add_syn(syn2, key_press='2', plot=False)
    debug.add_syn(syn3, key_press='3', plot=False)
    debug.add_seg(soma(0.5))
    debug.debug_interactive()
