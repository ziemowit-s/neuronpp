import os
import numpy as np

from neuronpp.utils.record import Record
from neuronpp.utils.simulation import Simulation
from neuronpp.core.cells.netstim_cell import NetStimCell
from neuronpp.core.cells.vecstim_cell import VecStimCell
from neuronpp.cells.ebner2019_ach_da_cell import Ebner2019AChDACell

path = os.path.dirname(os.path.abspath(__file__))


WEIGHT = 0.0035		# µS, conductance of (single) synaptic potentials
WARMUP = 200


if __name__ == '__main__':
    # define cell
    cell = Ebner2019AChDACell(name="cell")
    filepath = os.path.join(path, "..",
                            "commons/morphologies/swc/my.swc")
    cell.load_morpho(filepath=filepath)

    # make NetStim stims
    ns_cell = NetStimCell("netstim_cell")
    stim1 = ns_cell.make_netstim(start=WARMUP + 1, number=1)

    # make VecStim
    vs_cell = VecStimCell("vecstim_cell")
    stim2 = vs_cell.make_vecstim(np.array([WARMUP+50]))

    # make synapses with spines
    syns_4p, heads = cell.add_synapses_with_spine(source=None, secs=cell.secs, number=100, netcon_weight=WEIGHT,
                                                  mod_name="Syn4PAChDa", delay=1, **cell.params_4p_syn)
    for s, h in zip(syns_4p, heads):
        syn_ach = cell.add_synapse(source=stim1, mod_name="SynACh", seg=h(1.0), netcon_weight=0.1, delay=1)
        syn_da = cell.add_synapse(source=stim2, mod_name="SynDa", seg=h(1.0), netcon_weight=0.1, delay=1)
        cell.set_synaptic_pointers(s, syn_ach, syn_da)

    # add mechanisms
    cell.make_default_mechanisms()
    cell.make_apical_mechanisms(sections='head neck')

    # make plots
    rec_4psyn = Record(cell.filter_point_processes(mod_name="Syn4PAChDa", name="head[0]"), variables="w")

    # init and run
    sim = Simulation(init_v=-70, warmup=WARMUP)
    sim.run(runtime=200)

    # Event delivery
    syns_4p[0].make_event(10)

    sim.run(runtime=200)

    # plot
    rec_4psyn.plot()
