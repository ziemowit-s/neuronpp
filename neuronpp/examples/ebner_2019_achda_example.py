import numpy as np
import matplotlib.pyplot as plt

from neuronpp.utils.run_sim import RunSim

from neuronpp.utils.record import Record
from neuronpp.core.cells.netstim_cell import NetStimCell
from neuronpp.core.cells.vecstim_cell import VecStimCell
from neuronpp.cells.ebner2019_ach_da_cell import Ebner2019AChDACell


WEIGHT = 0.0035		# µS, conductance of (single) synaptic potentials
WARMUP = 200


if __name__ == '__main__':
    # define cell
    cell = Ebner2019AChDACell(name="cell")
    cell.load_morpho(filepath='../commons/morphologies/swc/my.swc', seg_per_L_um=1, make_const_segs=11)
    cell.make_spines(spine_number=10, head_nseg=10, neck_nseg=10, sec='dend')

    # make NetStim stims
    ns_cell = NetStimCell("netstim_cell")
    stim1 = ns_cell.make_netstim(start=WARMUP + 1, number=1)

    # make VecStim
    vs_cell = VecStimCell("vecstim_cell")
    stim2 = vs_cell.make_vecstim(np.array([WARMUP+50]))

    # make synapses with spines
    syn_4p, heads = cell.make_spine_with_synapse(source=None, number=100, weight=WEIGHT,
                                                 mod_name="Syn4PAChDa", delay=1, **cell.params_4p_syn)
    syn_ach = cell.make_sypanses(source=stim1, weight=0.1, mod_name="SynACh", target_sec=heads, delay=1)
    syn_da = cell.make_sypanses(source=stim2, weight=0.1, mod_name="SynDa", target_sec=heads, delay=1)
    cell.set_synaptic_pointers(syn_4p, syn_ach, syn_da)

    # add mechanisms
    cell.make_soma_mechanisms()
    cell.make_apical_mechanisms(sections='dend head neck')

    # make plots
    rec_4psyn = Record(cell.filter_point_processes(mod_name="Syn4PAChDa", name="head[0][0]"), variables="w")

    # init and run
    sim = RunSim(init_v=-70, warmup=WARMUP)
    sim.run(runtime=200)

    # Event delivery
    syn_4p[0].make_event(10)

    sim.run(runtime=200)

    # plot
    rec_4psyn.plot()
    plt.show()
