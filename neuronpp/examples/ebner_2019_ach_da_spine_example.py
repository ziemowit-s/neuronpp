import numpy as np
import matplotlib.pyplot as plt

from neuronpp.cells.ebner2019_ach_da_cell import Ebner2019AChDACell
from neuronpp.core.cells.netstim_cell import NetStimCell
from neuronpp.core.cells.spine_cell import SpineCell
from neuronpp.core.cells.vecstim_cell import VecStimCell
from neuronpp.core.utils.record import Record
from neuronpp.core.utils.run_sim import RunSim


class Ebner2019AChDaSpineCell(Ebner2019AChDACell, SpineCell):
    def __init__(self, name=None):
        SpineCell.__init__(self, name)
        Ebner2019AChDACell.__init__(self, name)


WEIGHT = 0.0035		# µS, conductance of (single) synaptic potentials
WARMUP = 200


if __name__ == '__main__':
    # define cell
    cell = Ebner2019AChDaSpineCell(name="cell")
    cell.load_morpho(filepath='morphologies/swc/my.swc', seg_per_L_um=1, make_const_segs=11)
    cell.make_spines(spine_number=10, head_nseg=10, neck_nseg=10, sec='dend')
    cell.make_soma_mechanisms()
    cell.make_apical_mechanisms(sections='dend head neck')
    cell.make_4p_ach_da_synapse(point_process_name="head", loc=1)  # add synapse at the top of each spine's head

    # make stims
    ns_cell = NetStimCell("netstim_cell")
    stim1 = ns_cell.make_netstim(start=WARMUP + 1, number=1)

    vs_cell = VecStimCell("vecstim_cell")
    stim2 = vs_cell.make_vecstim(np.array([WARMUP+50]))

    # stimulation
    cell.make_netcons(source=stim1, weight=WEIGHT, delay=1, mod_name="SynACh", point_process="head[0][0]")
    cell.make_netcons(source=stim2, weight=WEIGHT, delay=1, mod_name="SynDa", point_process="head[0][0]")
    # empty source for events
    ncons = cell.make_netcons(source=None, weight=WEIGHT, delay=1, mod_name="Syn4PAChDa", point_process="head[0][0]")

    # make plots
    rec_4psyn = Record(cell.filter_point_processes(mod_name="Syn4PAChDa", name="head[0][0]"), variables="w")

    # init and run
    sim = RunSim(init_v=-70, warmup=WARMUP)
    sim.run(runtime=200)

    # Event delivery
    ncons[0].hoc.event(sim.t + 10)

    sim.run(runtime=200)

    # plot
    rec_4psyn.plot()
    plt.show()
