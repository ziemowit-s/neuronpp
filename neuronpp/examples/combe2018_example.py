from neuronpp.utils.utils import make_shape_plot

from neuronpp.cells.combe2018_cell import Combe2018Cell
from neuronpp.utils.run_sim import RunSim


cell = Combe2018Cell(name="cell", spine_number=10, spine_sec="apic", spine_seed=13, compile=False)

make_shape_plot()
sim = RunSim(with_neuron_gui=True)
sim.run(runtime=500)

