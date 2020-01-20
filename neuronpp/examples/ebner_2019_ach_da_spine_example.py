import os

import numpy as np
import matplotlib.pyplot as plt
from neuronpp.utils.compile_mod import CompileMOD

from neuronpp.utils.run_sim import RunSim

from neuronpp.utils.record import Record
from neuronpp.core.cells.netstim_cell import NetStimCell
from neuronpp.core.cells.vecstim_cell import VecStimCell
from neuronpp.cells.ebner2019_ach_da_cell import Ebner2019AChDACell


WEIGHT = 0.0035		# µS, conductance of (single) synaptic potentials
WARMUP = 200

# Compile mods
comp = CompileMOD()
comp.compile(source_paths="commons/mods/ebner2019 commons/mods/4p_ach_da_syns commons/mods/neuron_commons", target_path=os.getcwd())


if __name__ == '__main__':
    # define cell
    cell = Ebner2019AChDACell(name="cell")
    cell.load_morpho(filepath='commons/morphologies/swc/my.swc', seg_per_L_um=1, make_const_segs=11)
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
    syn_ach = cell.make_sypanses(source=stim1, weight=WEIGHT, mod_name="SynACh", sec=heads, delay=1, **cell.params_ach)
    syn_da = cell.make_sypanses(source=stim2, weight=WEIGHT, mod_name="SynDa", sec=heads, delay=1, **cell.params_da)
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
