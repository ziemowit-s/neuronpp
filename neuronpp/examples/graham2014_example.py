from neuronpp.cells.graham2014_cell import Graham2014Cell
from neuronpp.utils.simulation import Simulation


cell = Graham2014Cell(name="cell")
ampa_pp, nmda_pp = cell.filter_point_processes(parent="head[0]")

sim = Simulation()
sim.run(runtime=500)

