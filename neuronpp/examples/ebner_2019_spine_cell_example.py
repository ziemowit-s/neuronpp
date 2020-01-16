from neuron import h
from neuron.units import mV
import matplotlib.pyplot as plt

from neuronpp.cells.ebner2019_cell import Ebner2019Cell
from neuronpp.core.cells.netstim_cell import NetStimCell
from neuronpp.core.cells.spine_cell import SpineCell
from neuronpp.core.utils.record import Record
from neuronpp.core.utils.run_sim import RunSim


class Ebner2019SpineCell(Ebner2019Cell, SpineCell):
    def __init__(self, name):
        SpineCell.__init__(self, name)
        Ebner2019Cell.__init__(self, name)


WEIGHT = 0.0035		# µS, conductance of (single) synaptic potentials
WARMUP = 200


if __name__ == '__main__':
    h.load_file('stdrun.hoc')
    h.dt = 0.025

    # define cell
    cell = Ebner2019SpineCell(name="cell")
    cell.load_morpho(filepath='morphologies/swc/my.swc', seg_per_L_um=1, make_const_segs=11)
    cell.make_spines(spine_number=10, head_nseg=10, neck_nseg=10, sec='dend')
    cell.make_soma_mechanisms()
    cell.make_apical_mechanisms(sections='dend head neck')
    cell.make_4p_synapse(point_process_name="head", loc=1)  # add synapse at the top of each spine's head

    # stimulation
    stim = NetStimCell("stim_cell").make_netstim(start=WARMUP + 1, number=300, interval=1)
    cell.make_netcons(source=stim, weight=WEIGHT, mod_name="Syn4P", delay=1)  # stim all synapses of type Syn4P

    # make plots
    rec_w = Record(cell.filter_point_processes(mod_name="Syn4P", name="head[0][0]"), variables="w")
    rec_v = Record(cell.filter_secs(name="head[0]"), locs=1.0, variables="v")

    # init and run
    h.finitialize(-70 * mV)
    sim = RunSim(warmup=WARMUP)
    sim.run(runtime=500)

    # plot
    rec_w.plot()
    rec_v.plot()
    plt.show()
