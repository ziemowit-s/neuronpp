import os

from neuronpp.utils.simulation import Simulation
from neuronpp.utils.record import Record
from neuronpp.cells.ebner2019_cell import Ebner2019Cell
from neuronpp.core.cells.netstim_cell import NetStimCell

path = os.path.dirname(os.path.abspath(__file__))
WEIGHT = 0.0035  # µS, conductance of (single) synaptic potentials
WARMUP = 200


if __name__ == '__main__':
    # define cell
    cell = Ebner2019Cell(name="cell")
    filepath = os.path.join(path, "..",
                            "commons/morphologies/swc/my.swc")
    cell.load_morpho(filepath=filepath)

    # stimulation
    stim = NetStimCell("stim_cell").make_netstim(start=WARMUP + 1, number=300, interval=1)
    cell.add_synapses_with_spine(source=stim, secs=cell.secs, mod_name="Syn4P", netcon_weight=WEIGHT, delay=1,
                                 head_nseg=10, neck_nseg=10, number=10, **cell.params_4p_syn)

    # add mechanisms
    cell.make_default_mechanisms()
    cell.make_apical_mechanisms(sections='dend head neck')

    # make plots
    rec_w = Record(cell.filter_point_processes(mod_name="Syn4P", name="head[0]"), variables="w")
    rec_v = Record(cell.filter_secs(name="head[0]")(1.0), variables="v")

    # init and run
    sim = Simulation(init_v=-70, warmup=WARMUP)
    sim.run(runtime=500)

    # plot
    rec_w.plot()
    rec_v.plot()
