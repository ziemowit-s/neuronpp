import matplotlib.pyplot as plt

from neuronpp.utils.run_sim import RunSim

from neuronpp.cells.cell import Cell
from neuronpp.utils.record import Record
from neuronpp.core.cells.netstim_cell import NetStimCell


# Prepare cell
cell = Cell(name="cell", compile_paths="../commons/mods/ebner2019")
cell.load_morpho(filepath='../commons/morphologies/swc/my.swc', seg_per_L_um=1, make_const_segs=11)
cell.make_sec("dend[1]", diam=10, l=10, nseg=10)
cell.connect_secs(source="dend[1]", target="soma")
cell.insert("pas")
cell.insert("hh")

# Two examples of synapses with NetStim:
stim_cell = NetStimCell("stim_cell")

# 1) Hoc-like
cell.make_point_processes(tag="example_pp", mod_name="ExpSyn", sec="soma", loc=0.5)
cell.make_netcons(source=stim_cell.make_netstim(start=250, number=3, interval=1),
                  mod_name="ExpSyn", point_process="example_pp", weight=0.01, delay=1)

# 2) Synapse-like
syn1 = cell.make_sypanses(source=stim_cell.make_netstim(start=300, number=3, interval=1),
                          weight=0.01, mod_name="Syn4P", sec="soma", target_loc=0.5, delay=1)[0]

# simple Event synapse example
syn2 = cell.make_sypanses(source=None, weight=0.01, mod_name="Syn4P", sec="soma", target_loc=0.5, delay=1)[0]

# prepare plots
rec_v = Record(cell.filter_secs(name="soma"), locs=0.5, variables="v")

# run
sim = RunSim(init_v=-55, warmup=20)

# Making external events to the synapse
syn2.make_event(10)
syn2.make_event(20)
syn2.make_event(30)
syn2.make_event(40)

for i in range(1000):
    sim.run(runtime=1)
    # plot
    rec_v.plot()
