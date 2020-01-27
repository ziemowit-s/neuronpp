from neuronpp.utils.experiment import Experiment
from neuronpp.utils.record import Record
from neuronpp.utils.run_sim import RunSim
from neuronpp.cells.combe2018_cell import Combe2018Cell

# Create cell
cell = Combe2018Cell(name="cell", spine_number=10, spine_sec="apic", spine_seed=13)

soma = cell.filter_secs("soma")[0]
syn = cell.filter_complex_synapses(tag="combe")[0]

# Prepare STDP protocol
stdp = Experiment()
stdp.make_protocol("3xEPSP[int=10]", start=1, isi=10, epsp_synapse=syn, i_clamp_section=soma)

# Prepare plots
v_soma_rec = Record([soma, syn.parent], variables='v', locs=0.5)
cai_head0_rec = Record(syn.parent, variables='cai', locs=0.5)

# Run
sim = RunSim(init_v=-70, warmup=20, with_neuron_gui=True, constant_timestep=False)
sim.run(runtime=100, debug=True)

# Plot
cai_head0_rec.plot()
v_soma_rec.plot()
v_soma_rec.to_csv("vrec.csv")
