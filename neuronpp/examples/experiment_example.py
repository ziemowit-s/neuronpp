from neuronpp.cells.cell import Cell
from neuronpp.utils.record import Record
from neuronpp.utils.experiment import Experiment
from neuronpp.utils.simulation import Simulation


# Create cell
cell = Cell(name="cell")
cell.load_morpho(filepath="../commons/morphologies/asc/cell2.asc")
cell.insert("pas")
cell.insert("hh")

soma = cell.filter_secs("soma")
dend = cell.filter_secs("apic[10]")
syn = cell.add_synapse(source=None, mod_name="ExpSyn", seg=dend(0.5))

# Prepare EPSP and AP (IClamp) protocols
experiment = Experiment(iti=40)
experiment.add_epsp(num=3, synapse=syn, init=20, interval=20, weight=0.02)
experiment.add_iclamp(num=3, segment=soma(0.5), init=60, interval=20, dur=3, amp=1.6)
experiment.build()

# Prepare plots
rec = Record([soma(0.5), dend(0.5)], variables='v')

# Run
sim = Simulation(init_v=-70, warmup=20, with_neuron_gui=False, constant_timestep=True)
sim.run(runtime=100)

rec.plot()
v_soma = rec.as_numpy('v', segment_name=soma(.5).name)
v_dend = rec.as_numpy('v', segment_name=dend(.5).name)
