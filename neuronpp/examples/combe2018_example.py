from neuronpp.cells.combe2018_cell import Combe2018Cell
from neuronpp.utils.run_sim import RunSim


cell = Combe2018Cell(name="cell", spine_number=200, spine_sec="apic", spine_seed=13, compile=False)

first_syn = cell.filter_complex_synapses(tag="combe")[0]

sim = RunSim(with_neuron_gui=True)
sim.run(runtime=500)

