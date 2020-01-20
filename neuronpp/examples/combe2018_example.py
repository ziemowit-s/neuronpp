from neuronpp.utils.record import Record
from neuronpp.utils.run_sim import RunSim
from neuronpp.electrodes.iclamp import IClamp
from neuronpp.cells.combe2018_cell import Combe2018Cell


cell = Combe2018Cell(name="cell", spine_number=1, spine_sec="apic", spine_seed=13, compile=True)

# Prepare synapse
first_syn = cell.filter_complex_synapses(tag="combe")[0]

# Prepare IClamp
iclamp = IClamp(cell.filter_secs("soma")[0].hoc(0.5))
iclamp.stim(delay=200, dur=3, amp=1.6)
iclamp.stim(delay=300, dur=3, amp=1.6)

# Prepare run
v_head0 = Record(first_syn.parent, variables='v', locs=0.5)
cai_head0 = Record(first_syn.parent, variables='cai', locs=0.5)

sim = RunSim(init_v=-70, warmup=10, with_neuron_gui=True, constant_timestep=False)

# Make event
first_syn.make_event(10)

# Run and plot
sim.run(runtime=500)
v_head0.plot()
cai_head0.plot()

