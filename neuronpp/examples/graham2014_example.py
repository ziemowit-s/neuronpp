from neuronpp.cells.graham2014_cell import Graham2014Cell
from neuronpp.utils.run_sim import RunSim


cell = Graham2014Cell(name="cell", compile=True)
sim = RunSim()
sim.run(runtime=500)

