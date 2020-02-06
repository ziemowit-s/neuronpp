from neuronpp.cells.ebner2019_cell import Ebner2019Cell
from neuronpp.cells.hay2011_cell import Hay2011Cell

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

freq = 50  # freqs.append(10, 20, 40, 50)
interval = 1000 / freq
delta_t = 10  # LTP


if __name__ == '__main__':
    cell = Ebner2019Cell(name="cell")
    cell.load_morpho(filepath='../commons/morphologies/asc/cell1.asc')
    cell.make_default_mechanisms()

    soma = cell.filter_secs("soma")[0]

    # Netstim to synapse
    stim = NetStimCell("stim").make_netstim(start=WARMUP, number=REPS, interval=interval)
    syn = cell.add_sypanse(source=stim, weight=WEIGHT, mod_name="Syn4P", delay=1, source_loc=0.5, sec='apic[1]')[0]

    # IClamp to soma
    iclamp = IClamp(segment=cell.filter_secs("soma")[0].hoc(0.5))
    for i in range(REPS):
        start_t = WARMUP + delta_t + i * interval
        iclamp.stim(delay=start_t, dur=DUR, amp=AMP)

    # Record
    rec = Record(cell.filter_secs("apic[1],apic[50]"), loc=0.5)

    # Run
    sim = RunSim(init_v=-70, warmup=WARMUP, dt=DT)
    total_time = REPS * interval + COOL_DOWN
    sim.run(total_time)

    # Plot
    rec.plot(position="merge")
