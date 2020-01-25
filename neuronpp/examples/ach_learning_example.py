import matplotlib.pyplot as plt

from neuronpp.utils.run_sim import RunSim

from neuronpp.utils.record import Record
from neuronpp.cells.ebner2019_ach_da_cell import Ebner2019AChDACell


WEIGHT = 0.01  # 0.07 µS is ~10mV, default threshold pass
WARMUP = 100


def create_cell(syn_4p_source=None, syn_ach_source=None, syn_da_source=None):
    cell = Ebner2019AChDACell("cell", "../commons/mods/ebner2019 ../commons/mods/4p_ach_da_syns")
    cell.make_sec("soma", diam=20, l=20, nseg=10)
    cell.make_sec("dend", diam=8, l=500, nseg=100)
    cell.connect_secs(source="dend", target="soma", source_loc=0, target_loc=1)

    # make synapses with spines
    syn_4p, heads = cell.make_spine_with_synapse(source=syn_4p_source, number=3, weight=WEIGHT,
                                                 mod_name="Syn4PAChDa", delay=1, **cell.params_4p_syn)
    syn_ach = cell.make_sypanses(source=syn_ach_source, weight=WEIGHT, mod_name="SynACh", sec=heads, delay=1)
    syn_da = cell.make_sypanses(source=syn_da_source, weight=WEIGHT, mod_name="SynDa", sec=heads, delay=1)

    for s1, s2, s3 in zip(syn_4p, syn_ach, syn_da):
        cell.set_synaptic_pointers(syn_4p, syn_ach, syn_da)
        cell.group_complex_sypanses("input_syn", s1, s2, s3)

    # add mechanisms
    cell.make_soma_mechanisms()
    cell.make_apical_mechanisms(sections='dend head neck')
    return cell


if __name__ == '__main__':
    cell = create_cell()
    syns = cell.filter_complex_synapses()
    soma = cell.filter_secs("soma")[0]

    syn4p = syns[0]['Syn4PAChDa']
    synach = syns[0]['SynACh']

    rec_w = Record(syn4p, variables="w")
    rec1 = Record(syn4p, variables="stdp_ach")
    rec2 = Record(syn4p, variables="ach_stdp")
    rec3 = Record(syn4p, variables="ACh")
    rec4 = Record(syn4p, variables="ACh_w")
    rec5 = Record(soma, locs=0.5, variables="v")

    sim = RunSim(init_v=-83, warmup=WARMUP)

    #syn['SynACh'].make_event(10)

    event = 0
    inter = 5
    for i in range(100):
        for syn in syns:
            syn['Syn4PAChDa'].make_event(event)
            event += inter

    sim.run(runtime=500)

    # plot
    rec_w.plot()
    rec1.plot()
    rec2.plot()
    rec3.plot()
    rec4.plot()
    rec5.plot()

    plt.show()
