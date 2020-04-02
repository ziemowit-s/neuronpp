from neuronpp.utils.simulation import Simulation

from neuronpp.utils.record import Record
from neuronpp.cells.ebner2019_ach_da_cell import Ebner2019AChDACell

WARMUP = 100


if __name__ == '__main__':
    cell = Ebner2019AChDACell("cell")
    cell.add_sec("soma", diam=20, l=20, nseg=10)
    cell.add_sec("dend", diam=8, l=500, nseg=100)
    cell.connect_secs(source="dend", target="soma", source_loc=0, target_loc=1)

    # make synapses with spines
    syns_4p, heads = cell.add_synapses_with_spine(source=None, secs=cell.secs, mod_name="Syn4PAChDa",
                                                  number=3, netcon_weight=1, delay=1, **cell.params_4p_syn)

    for s, h in zip(syns_4p, heads):
        syn_ach = cell.add_synapse(source=None, mod_name="SynACh", seg=h(1.0), netcon_weight=0.1, delay=1)
        syn_da = cell.add_synapse(source=None, mod_name="SynDa", seg=h(1.0), netcon_weight=0.1, delay=1)
        cell.set_synaptic_pointers(s, syn_ach, syn_da)
        cell.group_complex_synapses("input_syn", s, syn_ach, syn_da)

    # add mechanisms
    cell.make_default_mechanisms()
    cell.make_apical_mechanisms(sections='dend head neck')

    soma = cell.filter_secs("soma")

    syns = cell.filter_complex_synapses()
    syn4p = syns[0]['Syn4PAChDa']
    synach = syns[0]['SynACh']

    rec_syn = Record(syn4p, variables="w stdp_ach ach_stdp ACh ACh_w")
    rec_soma = Record(soma(0.5), variables="v")

    sim = Simulation(init_v=-80, warmup=WARMUP)

    event = 0
    inter = 5
    for i in range(10):
        for syn in syns:
            syn['Syn4PAChDa'].make_event(event)
            syn['SynACh'].make_event(event)
            event += inter

    sim.run(runtime=150)

    # plot
    rec_soma.plot()
    rec_syn.plot()
