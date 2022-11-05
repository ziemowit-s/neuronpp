import os

import numpy as np

from neuronpp.cells.cell import Cell
from neuronpp.utils.simulation import Simulation
from neuronpp.core.cells.netstim_cell import NetStimCell
from neuronpp.utils.graphs.network_graph import NetworkGraph
from neuronpp.core.populations.population import Population, NormalConnectionProba
from neuronpp.core.dists.distributions import Dist, NormalTruncatedDist, NormalTruncatedSegDist
from neuronpp.utils.utils import show_connectivity_graph

path = os.path.dirname(os.path.abspath(__file__))


def cell_function():
    cell = Cell(name="cell")
    morpho_path = os.path.join(path, "..", "commons/morphologies/swc/c91662.swc")
    cell.load_morpho(filepath=morpho_path)
    cell.insert("pas")
    cell.insert("hh")
    cell.make_spike_detector(seg=cell.filter_secs("soma")(0.5))
    return cell


if __name__ == '__main__':
    # Create NetStim
    netstim = NetStimCell("stim").add_netstim(start=21, number=200, interval=10)

    # Define weight distribution for both: NetStim->population1 and population1->population2
    weight_dist = NormalTruncatedDist(mean=0.1, std=0.2)

    # Create population 1
    pop1 = Population("pop_1")
    pop1.add_cells(num=3, cell_function=cell_function)

    # create 10 synapses on population 2 per NetStim object (single NetStim here)
    connector = pop1.connect(syn_num_per_cell_source=10)
    connector.set_source(netstim)

    # choose all dendrites as potential targets for synaptic choice
    targets = [d(0.5) for c in pop1.cells for d in c.filter_secs("dend")]
    connector.set_target(targets)

    # Make synapse
    syn_adder = connector.add_synapse("Exp2Syn")
    syn_adder.add_netcon(weight=weight_dist)
    # change tau1 and tau2 for Exp2Syn synapses
    syn_adder.add_point_process_params(tau1=0.1, tau2=2)

    connector.build()
    pop1.record()

    # Create population 2
    pop2 = Population("pop_2")
    pop2.add_cells(num=3, cell_function=cell_function)

    # create 5 synapses per single cell in population 1
    connector = pop2.connect(syn_num_per_cell_source=5)

    source = [c.filter_secs("soma")(0.5) for c in pop1.cells]
    connector.set_source(source)

    # choose all dendrites as potential targets for synaptic choice
    targets = [d(0.5) for c in pop2.cells for d in c.filter_secs("dend")]
    connector.set_target(targets)

    # Make synapse
    syn_adder = connector.add_synapse("Exp2Syn")
    syn_adder.add_netcon(weight=weight_dist)
    # change tau1 and tau2 for Exp2Syn synapses
    syn_adder.add_point_process_params(tau1=0.1, tau2=2)

    connector.build()
    pop2.record()

    show_connectivity_graph(pop1.cells + pop2.cells)

    # Run
    sim = Simulation(init_v=-70, warmup=20)
    for i in range(1000):
        sim.run(runtime=1)
        pop1.plot(animate=True)
        pop2.plot(animate=True)
