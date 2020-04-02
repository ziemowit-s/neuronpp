import os

import matplotlib.pylab as plt

from neuronpp.utils.iclamp import IClamp
from neuronpp.utils.record import Record
from neuronpp.utils.simulation import Simulation
from neuronpp.cells.ebner2019_cell import Ebner2019Cell
from neuronpp.core.cells.netstim_cell import NetStimCell

path = os.path.dirname(os.path.abspath(__file__))

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
    filepath = os.path.join(path, "..",
                            "commons/morphologies/asc/cell1.asc")
    cell.load_morpho(filepath=filepath)
    cell.make_default_mechanisms()

    soma = cell.filter_secs("soma")

    # Netstim to synapse
    stim = NetStimCell("stim").make_netstim(start=WARMUP, number=REPS, interval=interval)
    syn = cell.add_synapse(source=stim, netcon_weight=WEIGHT, mod_name="Syn4P", delay=1, seg=cell.filter_secs('apic[1]')(0.5))

    # IClamp to soma
    iclamp = IClamp(segment=cell.filter_secs("soma")(0.5))
    for i in range(REPS):
        start_t = WARMUP + delta_t + i * interval
        iclamp.stim(delay=start_t, dur=DUR, amp=AMP)

    # Record
    rec = Record([s(0.5) for s in cell.filter_secs("apic[1],apic[50]")])

    # Run
    sim = Simulation(init_v=-70, warmup=WARMUP, dt=DT)
    total_time = REPS * interval + COOL_DOWN
    sim.run(total_time)

    # Plot
    rec.plot(position="merge")
    plt.plot()
