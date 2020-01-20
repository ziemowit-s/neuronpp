from neuronpp.utils.utils import make_shape_plot

from neuronpp.cells.combe2018_cell import Combe2018Cell
from neuronpp.utils.run_sim import RunSim


cell = Combe2018Cell(name="cell", compile=True)
syns, heads = cell.make_spine_with_synapse(source=None, weight=0.01, number=1000, mod_name="ExpSyn", delay=1, sec="apic")

make_shape_plot()
sim = RunSim(with_neuron_gui=True)
sim.run(runtime=500)

