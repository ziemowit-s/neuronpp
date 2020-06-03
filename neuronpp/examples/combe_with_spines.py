from neuron import h
import numpy as np
import matplotlib.pyplot as plt
from neuronpp.cells.combe2018_cell_python_from_scratch import Combe2018Cell
from neuronpp.utils.simulation import Simulation
from neuronpp.utils.record import Record
from neuronpp.utils.iclamp import IClamp
# Create cell
cell = Combe2018Cell(name="cell1")

soma = cell.filter_secs("soma")
axon = cell.filter_secs("axon")
ic = IClamp(segment=soma(0.5))

fig, ax = plt.subplots(1, 1)
injections = [ .100]
rec_v = h.Vector().record(soma.hoc(0.5)._ref_v)
time =  h.Vector().record(h._ref_t)
for inj in injections:
    ic.stim(delay=300, dur=1000, amp=inj)
    sim = Simulation(init_v=-70)
    sim.run(runtime=1500, stepsize=1)
    for key in axon.hoc.psection()["density_mechs"]:
        print(key, axon.hoc.psection()["density_mechs"][key])
    ax.plot(time, rec_v, label="%4.2fnA"%inj)
ax.set_xlabel("time (s)")
ax.set_ylabel("V (mV)")
ax.legend()
plt.show()
