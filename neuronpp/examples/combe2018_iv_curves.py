from neuron import h
import numpy as np
import matplotlib.pyplot as plt
from neuronpp.cells.combe2018 import Combe2018Cell
from neuronpp.utils.simulation import Simulation
from neuronpp.utils.record import Record
from neuronpp.utils.iclamp import IClamp
# Create cell
h.CVode()
h.CVode().active(True)

cell = Combe2018Cell(name="cell1")
soma = cell.filter_secs("soma")

fig, ax = plt.subplots(1, 1)
injections = [-.1, 0, .100, .200]

for inj in injections:
    print(inj)
    ic = h.IClamp(soma.hoc(0.5))
    rec_v = h.Vector().record(soma.hoc(0.5)._ref_v)
    time =  h.Vector().record(h._ref_t)
    ic.delay = 300
    ic.dur = 1000
    ic.amp = inj
    h.finitialize(-70)
    h.fcurrent()
    h.tstop = 1500
    h.run()
    ax.plot(time, rec_v, label="%4.3fnA" % inj)

f1 = open("combe_mine_apic.txt", "w")
f2 = open("combe_mine_trunk.txt", "w")
f3 = open("combe_mine_dend.txt", "w")
f4 = open("combe_mine_sa.txt", "w")
for sec in cell.secs:
    if "trunk"  in sec.hoc.name():
        f = f2
    elif "apic" in sec.hoc.name():
        f = f1
    elif "dend" in sec.hoc.name():
        f = f3
    else:
        f = f4

    mechs = sec.hoc.psection()["density_mechs"]
    for key, value in mechs.items():
        f.write("%s %s " %(sec.hoc.name(), key) + str(value) + "\n")

ax.set_xlabel("time (s)")
ax.set_ylabel("V (mV)")
ax.legend()
plt.show()
