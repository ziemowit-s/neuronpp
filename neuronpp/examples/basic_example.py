import matplotlib.pyplot as plt

from neuronpp.cells.cell import Cell
from neuronpp.utils.run_sim import RunSim

from neuronpp.utils.record import Record
from neuronpp.utils.iclamp import IClamp
from neuronpp.utils.utils import make_shape_plot
from neuronpp.core.cells.netstim_cell import NetStimCell

# Create cell
cell = Cell(name="cell")
cell.load_morpho(filepath='../commons/morphologies/asc/cell2.asc')
cell.insert("pas")
cell.insert("hh")

# Create stim and synapses
stim = NetStimCell("stim_cell").make_netstim(start=30, number=5, interval=10)
syns = cell.add_synapses_with_spine(source=stim, secs=cell.filter_secs("apic"), mod_name="ExpSyn", weight=0.01, delay=1,
                                    number=100)
soma = cell.filter_secs("soma")

# Create IClamp
ic = IClamp(segment=soma(0.5))
ic.stim(delay=100, dur=10, amp=0.1)

# prepare plots and spike detector
rec_v = Record(soma, loc=0.5, variables="v")
cell.make_spike_detector(soma(0.5))

# run
sim = RunSim(init_v=-65, warmup=20, init_sleep=2, with_neuron_gui=True, shape_plots=[make_shape_plot()])
sim.run(runtime=200, stepsize=1, delay_between_steps=500)

# plot
cell.plot_spikes()
rec_v.plot()
plt.show()


