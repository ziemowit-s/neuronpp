import os
from neuronpp.cells.cell import Cell
from neuronpp.utils.synaptic_debugger import SynapticDebugger

path = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    # Prepare cell
    filepath = os.path.join(path, "..",
                            "commons/mods/sigma3syn")
    cell = Cell("cell", compile_paths=filepath)
    soma = cell.add_sec("soma", diam=20, l=20, nseg=10)
    cell.insert('pas')
    cell.insert('hh')

    w = 0.002
    ach_w = 0.1
    da_w = 0.1

    syn = cell.add_synapse(source=None, netcon_weight=w, seg=soma(0.5), mod_name="ExcSigma3Exp2SynAchDa",
                           tau1=1, tau2=5)
    pp = syn.point_process
    ach_netcon = cell.add_netcon(source=None, point_process=pp,
                                 netcon_weight=ach_w+pp.hoc.ach_substractor, delay=1)
    da_netcon = cell.add_netcon(source=None, point_process=pp,
                                netcon_weight=da_w+pp.hoc.da_substractor, delay=1)

    debug = SynapticDebugger(init_v=-70, warmup=10)
    debug.add_syn(syn, key_press='w', syn_variables="w")
    debug.add_con(ach_netcon, key_press='a')
    debug.add_con(da_netcon, key_press='d')
    debug.add_seg(soma(0.5))

    debug.debug_interactive()
