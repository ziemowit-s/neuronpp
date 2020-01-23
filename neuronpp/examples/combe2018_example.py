from neuronpp.utils.record import Record
from neuronpp.utils.run_sim import RunSim
from neuronpp.electrodes.iclamp import IClamp
from neuronpp.cells.combe2018_cell import Combe2018Cell
from neuronpp.utils.utils import stdp_protocol

cell = Combe2018Cell(name="cell", spine_number=10, spine_sec="apic", spine_seed=13)
soma = cell.filter_secs("soma")[0]
first_syn = cell.filter_complex_synapses(tag="combe")[0]

stdp_protocol(protocol="3xEPSP[int=10] 3xAP[int=10,dur=3,amp=1.6]", start=1, isi=10, iti=3000,
              synapse=first_syn,
              section=cell.filter_secs("soma")[0])

# Prepare run
v_rec = Record([soma, first_syn.parent], variables='v', locs=0.5)
cai_head0_rec = Record(first_syn.parent, variables='cai', locs=0.5)

sim = RunSim(init_v=-70, warmup=20, with_neuron_gui=True, constant_timestep=False)

# Run and plot
sim.run(runtime=100, debug=True)

v_rec.plot()
cai_head0_rec.plot()

v_rec.to_csv("vrec.csv")

