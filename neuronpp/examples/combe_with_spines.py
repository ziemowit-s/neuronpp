import matplotlib.pyplot as plt
from neuronpp.cells.combe2018_cell_python_from_scratch import Combe2018Cell
from neuronpp.utils.simulation import Simulation
from neuronpp.utils.record import Record
from neuronpp.utils.iclamp import IClamp
from neuronpp.utils.utils import make_shape_plot
# Create cell
cell = Combe2018Cell(name="cell1")

soma = cell.filter_secs("soma")

ic = IClamp(segment=soma(0.5))

ic.stim(delay=500, dur=1000, amp=0.1)

rec_v = Record(soma(0.5), variables="v")
sim = Simulation(init_v=-70, warmup=20)
sim.run(runtime=2000, stepsize=1)
rec_v.plot()
plt.show()
