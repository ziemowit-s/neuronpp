import os

from neuronpp.cells.cell import Cell
from neuronpp.core.cells.netstim_cell import NetStimCell
from neuronpp.core.populations.population import Population
from neuronpp.utils.graphs.network_status_graph import NetworkStatusGraph

from neuronpp.utils.simulation import Simulation

path = os.path.dirname(os.path.abspath(__file__))

class ExcitatoryPopulation(Population):
    def cell_definition(self, **kwargs) -> Cell:
        cell = Cell(name="cell")
        morpho_path = os.path.join(path, "..",
                          "commons/morphologies/swc/my.swc")
        cell.load_morpho(filepath=morpho_path)
        cell.insert("pas")
        cell.insert("hh")
        return cell

    def syn_definition(self, cell, source, weight=1, **kwargs) -> list:
        secs = cell.filter_secs("dend")
        syns, heads = cell.add_synapses_with_spine(source=source, secs=secs, mod_name="Exp2Syn", netcon_weight=weight)
        return syns


if __name__ == '__main__':
    # Create NetStim
    stim = NetStimCell("stim").make_netstim(start=21, number=1000, interval=2)

    # Create population 1
    pop1 = ExcitatoryPopulation("pop_0")
    pop1.create(4)
    pop1.connect(source=stim, rule='all', weight=0.01)
    pop1.record()

    # Create population 2
    pop2 = ExcitatoryPopulation("pop_1")
    pop2.create(4)
    pop2.connect(source=pop1, rule='all', weight=0.01)
    pop2.record()

    # Create population 3
    pop3 = ExcitatoryPopulation("pop_2")
    pop3.create(4)
    pop3.connect(source=pop2, rule='all', weight=0.01)
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
        pop1.plot(animate=True)
        pop2.plot(animate=True)
        pop3.plot(animate=True)
