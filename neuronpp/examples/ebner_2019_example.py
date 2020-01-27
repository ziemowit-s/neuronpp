import matplotlib.pyplot as plt

from neuronpp.utils.run_sim import RunSim

from neuronpp.utils.record import Record
from neuronpp.cells.ebner2019_cell import Ebner2019Cell
from neuronpp.core.cells.netstim_cell import NetStimCell


WEIGHT = 0.0035  # µS, conductance of (single) synaptic potentials
WARMUP = 200


if __name__ == '__main__':
    # define cell
    cell = Ebner2019Cell(name="cell", compile_paths="../commons/mods/ebner2019")
    cell.load_morpho(filepath='../commons/morphologies/swc/my.swc', seg_per_L_um=1, make_const_segs=11)

    # stimulation
    stim = NetStimCell("stim_cell").make_netstim(start=WARMUP + 1, number=300, interval=1)
    cell.make_spine_with_synapse(source=stim, weight=WEIGHT, mod_name="Syn4P", delay=1,
                                 number=10, head_nseg=10, neck_nseg=10, target_sec='dend', **cell.params_4p_syn)

    # add mechanisms
    cell.make_soma_mechanisms()
    cell.make_apical_mechanisms(sections='dend head neck')

    # make plots
    rec_w = Record(cell.filter_point_processes(mod_name="Syn4P", name="head[0][0]"), variables="w")
    rec_v = Record(cell.filter_secs(name="head[0]"), locs=1.0, variables="v")

    # init and run
    sim = RunSim(init_v=-70, warmup=WARMUP)
    sim.run(runtime=500)

    # plot
    rec_w.plot()
    rec_v.plot()
