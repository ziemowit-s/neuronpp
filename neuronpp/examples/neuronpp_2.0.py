import matplotlib.pyplot as plt

from neuronpp.core.cells.netstim_cell import NetStimCell
from neuronpp.core.cells.synaptic_cell import SynapticCell
from neuronpp.core.utils.record import Record
from neuronpp.core.utils.run_sim import RunSim

cell = SynapticCell(name="cell")
cell.load_morpho(filepath='morphologies/swc/my.swc', seg_per_L_um=1, make_const_segs=11)
cell.make_sec("dend[1]", diam=10, l=10, nseg=10)
cell.connect_secs(source="dend[1]", target="soma")
cell.insert("pas")
cell.insert("hh")

# Two examples of synapses with NetStim:
stim_cell = NetStimCell("stim_cell")

# 1) Hoc-like
cell.make_point_processes(name="example_pp", mod_name="Syn4P", sec="soma", loc=0.5)
cell.make_netcons(source=stim_cell.make_netstim(start=200, number=3, interval=1),
                  mod_name="Syn4P", point_process="example_pp", weight=0.01, delay=1)

# 2) Synapse-like
syn_netstim = cell.make_sypanse(source=stim_cell.make_netstim(start=300, number=3, interval=1),
                                weight=0.01, mod_name="Syn4P", sec="soma", loc=0.5, delay=1)[0]

# simple Event synapse example
syn_event = cell.make_sypanse(source=None, weight=0.01, mod_name="Syn4P", sec="soma", loc=0.5, delay=1)[0]

# prepare plots
rec_v = Record(cell.filter_secs(name="soma"), locs=0.5, variables="v")

# run
sim = RunSim(init_v=-70, warmup=20)

# Making external events to the synapse
syn_event.netconn.hoc.event(sim.t + 10)
syn_event.netconn.hoc.event(sim.t + 20)
syn_event.netconn.hoc.event(sim.t + 30)
syn_event.netconn.hoc.event(sim.t + 40)

sim.run(runtime=500)


# plot
rec_v.plot()
plt.show()


