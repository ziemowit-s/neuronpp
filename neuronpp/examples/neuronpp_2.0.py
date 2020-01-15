from neuronpp.cells.core.netstim_cell import NetStimCell

from neuronpp.cells.core.netcon_cell import NetConnCell


cell = NetConnCell(name="cell")
cell.load_morpho(filepath='morphologies/swc/my.swc', seg_per_L_um=1, add_const_segs=11)
cell.add_sec("dend", diam=10, l=10, nseg=10, target_name="soma")
cell.add_point_processes(mod_name="Syn4P", name="soma", loc=0.5)

stim_cell = NetStimCell("stim_cell")
source_stim = stim_cell.add_netstim("stim1", start=0, number=300, interval=1)

cell.add_netcons(source=source_stim, name="soma", weight=1.0, delay=1)

