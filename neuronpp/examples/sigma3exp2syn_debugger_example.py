from neuronpp.cells.cell import Cell
from neuronpp.utils.synaptic_debugger import SynapticDebugger

if __name__ == '__main__':
    # Prepare cell
    cell = Cell("cell", compile_paths='../commons/mods/sigma3syn')
    soma = cell.add_sec("soma", diam=20, l=20, nseg=10)
    cell.insert('pas')
    cell.insert('hh')

    syn = cell.add_synapse(source=None, netcon_weight=0.002, seg=soma(0.5), mod_name="inh_sigma3exp2syn")

    debug = SynapticDebugger(init_v=-70, warmup=100)
    debug.add_syn(syn, key_press='w', syn_variables="w")
    debug.add_sec(soma(0.5))

    debug.debug_interactive()
