import matplotlib.pyplot as plt

from neuronpp.utils.run_sim import RunSim

from neuronpp.utils.record import Record
from neuronpp.core.cells.netstim_cell import NetStimCell
from neuronpp.cells.ebner2019_ach_da_cell import Ebner2019AChDACell


WEIGHT = 0.07  # 0.07 µS is ~10mV, default threshold pass
WARMUP = 500


def create_cell(syn_4p_source=None, syn_ach_source=None, syn_da_source=None):
    cell = Ebner2019AChDACell("cell", "commons/mods/ebner2019 commons/mods/4p_ach_da_syns")
    cell.make_sec("soma", diam=20, l=20, nseg=10)
    cell.make_sec("dend", diam=8, l=500, nseg=100)
    cell.connect_secs(source="dend", target="soma", source_loc=0, target_loc=1)

    # make synapses with spines
    syn_4p, heads = cell.make_spine_with_synapse(source=syn_4p_source, number=1, weight=WEIGHT,
                                                 mod_name="Syn4PAChDa", delay=1, **cell.params_4p_syn)
    syn_ach = cell.make_sypanses(source=syn_ach_source, weight=WEIGHT, mod_name="SynACh", sec=heads, delay=1)
    syn_da = cell.make_sypanses(source=syn_da_source, weight=WEIGHT, mod_name="SynDa", sec=heads, delay=1)
    cell.set_synaptic_pointers(syn_4p, syn_ach, syn_da)

    cell.group_complex_sypanses("input_syn", syn_4p, syn_ach, syn_da)

    # add mechanisms
    cell.make_soma_mechanisms()
    cell.make_apical_mechanisms(sections='dend head neck')
    return cell


if __name__ == '__main__':
    ns_cell = NetStimCell("netstim_cell")
    stim1 = ns_cell.make_netstim(start=WARMUP + 1, number=1)

    cell = create_cell()
    syn = cell.filter_complex_synapses()[0]

    syn4p = syn['Syn4PAChDa']
    synach = syn['SynACh']
    print('ACh tau', synach.hoc.tau)
    rec_v = Record(syn.parent, locs=0.5, variables="v")
    rec_w = Record(syn4p, variables="w")
    rec_ach = Record(syn4p, variables="ACh")

    sim = RunSim(init_v=-83, warmup=WARMUP)
    #syn.make_event(10)
    syn['Syn4PAChDa'].make_event(10)
    #syn['SynACh'].make_event(20)
    sim.run(runtime=5000)

    # plot
    rec_w.plot()
    rec_ach.plot()
    rec_v.plot()
    plt.show()
