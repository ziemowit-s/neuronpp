from neuronpp.core.cells.netconn_cell import NetConnCell
from neuronpp.core.cells.netstim_cell import NetStimCell

cell = NetConnCell(name="cell")
cell.load_morpho(filepath='morphologies/swc/my.swc', seg_per_L_um=1, make_const_segs=11)
cell.make_sec("dend[1]", diam=10, l=10, nseg=10)
cell.connect_secs(source="dend[1]", target="soma")
cell.make_point_processes(mod_name="Syn4P", sec="soma", loc=0.5)

stim_cell = NetStimCell("stim_cell")
source_stim = stim_cell.make_netstim(start=0, number=300, interval=1)

cell.make_netcons(source=source_stim, mod_name="Syn4P", weight=1.0, delay=1)

