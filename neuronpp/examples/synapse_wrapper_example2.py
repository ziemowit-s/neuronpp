import matplotlib.pyplot as plt

from neuronpp.core.cells.netstim_cell import NetStimCell
from neuronpp.core.cells.synaptic_spine_cell import SynapticSpineCell
from neuronpp.core.utils.record import Record
from neuronpp.core.utils.run_sim import RunSim
from neuronpp.core.utils.utils import make_shape_plot

cell = SynapticSpineCell(name="cell")
cell.load_morpho(filepath='morphologies/swc/my.swc', seg_per_L_um=1, make_const_segs=11)
cell.insert("pas")
cell.insert("hh")

SYNAPSE_MECH = "ExpSyn"
stim = NetStimCell("stim_cell").make_netstim(start=300, number=5, interval=10)

syn1 = cell.make_spine_with_synapse(source=stim, weight=0.01, mod_name=SYNAPSE_MECH,
                                    sec="dend", loc=0.5, delay=1, head_nseg=10, neck_nseg=10, spine_number=10)[0]

# prepare plots
rec_v = Record(cell.filter_secs(name="soma"), locs=0.5, variables="v")
make_shape_plot()

# run
sim = RunSim(init_v=-65, warmup=20, with_neuron_gui=True)
sim.run(runtime=500)

# plot
rec_v.plot()
plt.show()


