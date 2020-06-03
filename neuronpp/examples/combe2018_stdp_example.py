from neuron import h
import numpy as np
import matplotlib.pyplot as plt
from neuronpp.utils.experiment import Experiment
from neuronpp.utils.record import Record
from neuronpp.utils.simulation import Simulation
from neuronpp.cells.combe2018_cell import Combe2018Cell
from neuronpp.utils.iclamp import IClamp

# Create cell
cell = Combe2018Cell(name="cell", spine_number=10, spine_secs_names="apic", spine_seed=13)

soma = cell.filter_secs("soma")

for sec in cell.secs:
    if "km" in sec.hoc.psection()["density_mechs"]:
        print(sec.hoc.name(), sec.hoc.psection()["density_mechs"]["km"]["gbar"])
    else:
        print(sec, "no km")
ic = IClamp(segment=soma(0.5))

fig, ax = plt.subplots(1, 1)
injections = [ .100]
rec_v = h.Vector().record(soma.hoc(0.5)._ref_v)
time =  h.Vector().record(h._ref_t)
for inj in injections:
    ic.stim(delay=300, dur=1000, amp=inj)
    sim = Simulation(init_v=-70)
    sim.run(runtime=1500, stepsize=1)
    for key in soma.hoc.psection()["density_mechs"]:
        print(key, soma.hoc.psection()["density_mechs"][key])
    ax.plot(time, rec_v, label="%4.2fnA"%inj)
ax.set_xlabel("time (s)")
ax.set_ylabel("V (mV)")
ax.legend()

plt.show()

# syns = cell.filter_complex_synapses(tag="combe")

# # Prepare STDP protocol
# stdp = Experiment()
# stdp.make_protocol("3xEPSP[int=10] 3xAP[int=10,dur=3,amp=1.6]", start=1, isi=10, epsp_synapse=syns[0], i_clamp_section=soma)

# # Prepare plots
# v_soma_rec = Record([soma(0.5), syns[0].parent], variables='v')
# cai_head0_rec = Record(syns[0].parent, variables='cai')

# # Run
# sim = Simulation(init_v=-70, warmup=20, with_neuron_gui=True, constant_timestep=False)
# sim.run(runtime=100, debug=True)

# # Plot
# cai_head0_rec.plot()
# v_soma_rec.plot()
# v_soma_rec.to_csv("vrec.csv")
