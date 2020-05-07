import os

from neuronpp.cells.cell_template import CellTemplate
from neuronpp.core.cells.netstim_cell import NetStimCell
from neuronpp.core.distributions import NormalDist
from neuronpp.core.population import Population, NormalProba, NetconParams, ConnParams
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
    stim = NetStimCell("stim").make_netstim(start=21, number=100, interval=2)

    # Create population 1
    conn_dist = NormalProba(expected=0.5, mean=0.5, std=0.1)
    weight_dist = NormalDist(mean=0.01, std=0.02)

    pop1 = Population("pop_0")
    pop1.add_cells(template=cell_template, num=4)
    pop1.connect(source=stim,
                 target=[c.filter_secs("dend")(0.5) for c in pop1.cells],
                 mod_name="Exp2Syn",
                 netcon_params=NetconParams(weight=weight_dist),
                 conn_params=ConnParams(proba=conn_dist))
    pop1.record()

    # Create population 2
    pop2 = Population("pop_1")
    pop2.add_cells(template=cell_template, num=4)
    pop2.connect(source=[c.filter_secs("soma")(0.5) for c in pop1.cells],
                 target=[c.filter_secs("dend")(0.5) for c in pop2.cells],
                 mod_name="Exp2Syn",
                 netcon_params=NetconParams(weight=weight_dist),
                 conn_params=ConnParams(proba=conn_dist))
    pop2.record()

    # Create population 3
    pop3 = Population("pop_2")
    pop3.add_cells(template=cell_template, num=4)
    pop3.connect(source=[c.filter_secs("soma")(0.5) for c in pop2.cells],
                 target=[c.filter_secs("dend")(0.5) for c in pop3.cells],
                 mod_name="Exp2Syn",
                 netcon_params=NetconParams(weight=weight_dist),
                 conn_params=ConnParams(proba=conn_dist))
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
        #pop1.plot(animate=True)
        #pop2.plot(animate=True)
        #pop3.plot(animate=True)
