import matplotlib.pyplot as plt

from neuronpp.cells.cell import Cell
from neuronpp.utils.record import Record
from neuronpp.utils.iclamp import IClamp
from neuronpp.utils.simulation import Simulation

# Create cell
cell = Cell(name="cell")
soma = cell.add_sec("soma", diam=20, l=20, nseg=100)
cell.insert("pas")
cell.insert("hh")

# Create IClamp
ic = IClamp(segment=soma(0.5))
ic.stim(delay=30, dur=100, amp=0.9)

# prepare plots and spike detector
rec_v = Record(soma(0.5), variables="v")

# run
sim = Simulation(init_v=-65, warmup=20)
sim.run(runtime=500)

# plot
rec_v.plot()
plt.show()


