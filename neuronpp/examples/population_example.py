import os
import numpy as np

from neuronpp.cells.cell_template import CellTemplate
from neuronpp.core.cells.netstim_cell import NetStimCell
from neuronpp.core.distributions import NormalDist, Dist, NormalTruncatedDist
from neuronpp.core.populations.population import Population, NormalProba
from neuronpp.utils.graphs.network_status_graph import NetworkStatusGraph

from neuronpp.utils.simulation import Simulation

path = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    cell_template = CellTemplate(name="cell")
    morpho_path = os.path.join(path, "..", "commons/morphologies/swc/my.swc")
    cell_template.load_morpho(filepath=morpho_path)
    cell_template.insert("pas")
    cell_template.insert("hh")

    # Create NetStim
    netstim = NetStimCell("stim").make_netstim(start=21, number=100, interval=2)

    # Define connection probabilities
    Dist.set_seed(13)
    connection_proba = NormalProba(mean=0.45, std=0.1)
    weight_dist = NormalTruncatedDist(mean=0.01, std=0.02)

    # Create population 1
    pop1 = Population("pop_0")
    pop1.add_cells(template=cell_template, num=4)

    connector = pop1.connect(proba=connection_proba) \
        .source(netstim) \
        .target([c.filter_secs("dend")(0.5) for c in pop1.cells])
    connector.add_synapse("Exp2Syn") \
        .add_netcon(weight=weight_dist)

    connector.build()
    pop1.record()

    # Create population 2
    pop2 = Population("pop_1")
    pop2.add_cells(template=cell_template, num=4)

    connector = pop2.connect(proba=connection_proba) \
        .source([c.filter_secs("soma")(0.5) for c in pop1.cells]) \
        .target([c.filter_secs("dend")(0.5) for c in pop2.cells])
    connector.add_synapse("Exp2Syn") \
        .add_netcon(weight=weight_dist)

    connector.build()
    pop2.record()

    # Create population 3
    pop3 = Population("pop_2")
    pop3.add_cells(template=cell_template, num=4)

    connector = pop3.connect(proba=connection_proba) \
        .source([c.filter_secs("soma")(0.5) for c in pop2.cells]) \
        .target([c.filter_secs("dend")(0.5) for c in pop3.cells])
    connector.add_synapse("Exp2Syn") \
        .add_netcon(weight=weight_dist)

    connector.build()
    pop3.record()

    # Creates inhibitory connections between pop2->pop3
    for c in pop3.cells:
        for p in c.pps:
            p.hoc.e = -90

    # Create connectivity graph grouped by populations, with weighs and spike rates updated
    graph = NetworkStatusGraph(cells=pop1.cells + pop2.cells + pop3.cells)
    graph.plot()

    # Run
    sim = Simulation(init_v=-70, warmup=20)
    for i in range(1000):
        sim.run(runtime=1)
        # pop1.plot(animate=True)
        # pop2.plot(animate=True)
        # pop3.plot(animate=True)
