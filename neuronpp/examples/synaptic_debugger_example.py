from neuronpp.cells.ebner2019_ach_da_cell import Ebner2019AChDACell
from neuronpp.utils.synaptic_debugger import SynapticDebugger

if __name__ == '__main__':
    # Prepare cell
    cell = Ebner2019AChDACell("cell")
    cell.make_sec("soma", diam=20, l=20, nseg=10)
    syns = cell.make_sypanses(source=None, weight=0.1, target_sec="soma", target_loc=0.5, mod_name="Syn4PAChDa",
                              **cell.params_4p_syn)
    syn_ach = cell.make_sypanses(source=None, weight=0.1, target_sec="soma", target_loc=0.5, mod_name="SynACh")
    syn_da = cell.make_sypanses(source=None, weight=0.1, target_sec="soma", target_loc=0.5, mod_name="SynDa")
    cell.set_synaptic_pointers(syns, syn_ach, syn_da)
    cell.make_soma_mechanisms()

    # Debug
    debug = SynapticDebugger(init_v=-80, warmup=200)

    debug.add_syns(syns, key_press='w')
    debug.add_syns(syn_ach, key_press='a')
    debug.add_syns(syn_da, key_press='d')

    debug.add_secs(cell.filter_secs("soma"))

    debug.debug_interactive()
