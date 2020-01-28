from neuronpp.cells.ebner2019_cell import Ebner2019Cell
from neuronpp.utils.synaptic_debugger import SynapticDebugger

if __name__ == '__main__':
    # Prepare cell
    cell = Ebner2019Cell("cell", "../commons/mods/ebner2019")
    cell.make_sec("soma", diam=20, l=20, nseg=10)
    syn_4p = cell.make_sypanses(source=None, target_sec="soma", target_loc=0.5,
                                weight=0.1, mod_name="Syn4P", delay=1, **cell.params_4p_syn)
    cell.make_soma_mechanisms()

    # Debug
    debug = SynapticDebugger(syns=syn_4p, secs=cell.filter_secs("soma"), init_v=-83, warmup=200)
    debug.debug_interactive(stim_key='w')
