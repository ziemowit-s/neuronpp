from neuronpp.core.cells.netstim_cell import NetStimCell

from neuronpp.cells.hoc_cell import HocCell
from neuronpp.utils.record import Record
from neuronpp.utils.iclamp import IClamp
from neuronpp.utils.run_sim import RunSim

REPS = 5  # Number of pre-and postsynaptic spikes
DT = 0.025
AMP = 2.7
DUR = 5.0
WARMUP = 2300
COOL_DOWN = 100
WEIGHT = 0.0035

if __name__ == '__main__':
    freq = 10

    # Cell definition
    cell = HocCell("cell", compile_paths="../commons/mods/hay2011 ../commons/mods/ebner2019")
    cell.load_hoc("../commons/hocmodels/ebner2019/load_model.hoc", cell_template_name="L5PCtemplate")

    # Netstim to synapse
    stim = NetStimCell("stim")
    st = stim.make_netstim(start=WARMUP, number=REPS, interval=1000/freq)
    cell.make_netcons(source=st, weight=WEIGHT, mod_name="Syn4P")

    # IClamp to soma
    iclamp = IClamp(segment=cell.filter_secs("soma")[0].hoc(0.5))
    iclamp.stim(delay=0, dur=DUR, amp=AMP)

    # Record
    rec = Record(cell.filter_secs("apic[1]")+cell.filter_secs("apic[50]"), loc=0.5)

    # Run
    total_time = WARMUP + REPS * (1000.0 / freq) + COOL_DOWN
    sim = RunSim(init_v=-70, warmup=WARMUP, dt=DT)
    sim.run(1)

    # Plot
    rec.plot(position="grid")
