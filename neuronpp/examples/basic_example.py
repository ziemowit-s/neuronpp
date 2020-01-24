import matplotlib.pyplot as plt
from neuronpp.utils.run_sim import RunSim

from neuronpp.cells.cell import Cell
from neuronpp.utils.record import Record
from neuronpp.utils.iclamp import IClamp
from neuronpp.utils.utils import make_shape_plot
from neuronpp.core.cells.netstim_cell import NetStimCell

# Create cell
cell = Cell(name="cell")
cell.load_morpho(filepath='commons/morphologies/asc/cell2.asc')
cell.insert("pas")
cell.insert("hh")

# Create stim and synapses
stim = NetStimCell("stim_cell").make_netstim(start=30, number=5, interval=10)
syn1 = cell.make_spine_with_synapse(source=stim, weight=0.01, mod_name="ExpSyn",
                                    sec="apic", delay=1, head_nseg=1, neck_nseg=1, number=100)[0]

# Create IClamp
ic = IClamp(segment=cell.filter_secs("soma")[0].hoc(0.5))
ic.stim(delay=100, dur=10, amp=0.1)

# prepare plots and spike detector
rec_v = Record(cell.filter_secs(name="soma"), locs=0.5, variables="v")
cell.make_spike_detector(sec="soma", loc=0.5)

# run
sim = RunSim(init_v=-65, warmup=20, with_neuron_gui=True, shape_plots=[make_shape_plot()])
sim.run(runtime=200)

# plot
cell.plot_spikes()
rec_v.plot()
plt.show()


