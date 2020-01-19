import matplotlib.pyplot as plt
from neuronpp.utils.run_sim import RunSim

from neuronpp.cells.cell import Cell
from neuronpp.utils.record import Record
from neuronpp.electrodes.iclamp import IClamp
from neuronpp.utils.utils import make_shape_plot
from neuronpp.core.cells.netstim_cell import NetStimCell

cell = Cell(name="cell")
cell.load_morpho(filepath='commons/morphologies/swc/my.swc', seg_per_L_um=1, make_const_segs=11)
cell.insert("pas")
cell.insert("hh")

SYNAPSE_MECH = "ExpSyn"
stim = NetStimCell("stim_cell").make_netstim(start=300, number=5, interval=10)

syn1 = cell.make_spine_with_synapse(source=stim, weight=0.01, mod_name=SYNAPSE_MECH,
                                    sec="dend", delay=1, head_nseg=10, neck_nseg=10, number=10)[0]

ic = IClamp(segment=cell.filter_secs("soma")[0].hoc(0.5))
ic.stim(delay=100, dur=10, amp=0.1)

# prepare plots
rec_v = Record(cell.filter_secs(name="soma"), locs=0.5, variables="v")

# Spike detector
cell.make_spike_detector(sec="soma", loc=0.5)
make_shape_plot()

# run
sim = RunSim(init_v=-65, warmup=20, with_neuron_gui=True)
sim.run(runtime=500)

# plot
cell.plot_spikes()
rec_v.plot()
plt.show()


