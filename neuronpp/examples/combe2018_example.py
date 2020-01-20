from neuronpp.cells.combe2018_cell import Combe2018Cell
from neuronpp.utils.run_sim import RunSim


cell = Combe2018Cell(name="cell", compile=True)
sim = RunSim()
sim.run(runtime=500)

