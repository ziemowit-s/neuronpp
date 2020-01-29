from neuronpp.core.cells.netstim_cell import NetStimCell

from neuronpp.cells.hoc_cell import HocCell
from neuronpp.utils.record import Record
from neuronpp.utils.iclamp import IClamp
from neuronpp.utils.run_sim import RunSim

REPS = 5		# Number of pre- and postsynaptic spikes
DT = 0.025		# ms, integration step.
AMP = 2.7		# nA, amplitude of current injection to trigger postsynaptic spikes
DUR = 5.0		# ms, duration of the current injection
WARM_UP = 2300 	# ms, silence phase before stimulation
COOL_DOWN = 100	# ms, silence phase after stimulation
WEIGHT = 0.0035	# ?S, conductance of (single) synaptic potentials
LOCATION = 1	# 1 ... proximal (90 ?m) / 2 ... distal (669 ?m)

if __name__ == '__main__':
    freq = 10
    
    cell = HocCell("cell", compile_paths="../commons/mods/hay2011 ../commons/mods/ebner2019")
    cell.load_hoc("../commons/hocmodels/ebner2019/load_model.hoc", cell_template_name="L5PCtemplate")
    
    stim = NetStimCell("stim")
    st = stim.make_netstim(start=WARM_UP, number=REPS, interval=1000/freq)
    cell.make_netcons(source=st, weight=WEIGHT, point_process="aaa")

    iclamp = IClamp(segment=cell.filter_secs("soma")[0].hoc(0.5))
    iclamp.stim(delay=0, dur=1e9, amp=AMP)

    rec = Record(soma, loc=0.5)
    sim = RunSim(init_v=-70, warmup=WARMUP)
    sim.run(50)
    rec.plot()
