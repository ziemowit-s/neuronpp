from neuronpp.cells.cell import Cell
from neuronpp.core.cells.netstim_cell import NetStimCell
from neuronpp.core.populations.population import Population
from neuronpp.utils.utils import show_conectivity_graph

from neuronpp.utils.run_sim import RunSim


class ExcitatoryPopulation(Population):
    def cell_definition(self, **kwargs) -> Cell:
        cell = Cell(name="cell")
        cell.load_morpho(filepath='../commons/morphologies/swc/my.swc')
        cell.insert("pas")
        cell.insert("hh")
        return cell

    def syn_definition(self, cell, source, weight=1, **kwargs) -> list:
        secs = cell.filter_secs("dend")
        syns, heads = cell.add_synapses_with_spine(source=source, secs=secs, mod_name="Exp2Syn", weight=weight)
        return syns


if __name__ == '__main__':
    # Create NetStim
    stim = NetStimCell("stim").make_netstim(start=21, number=10, interval=10)

    # Create population 1
    pop1 = ExcitatoryPopulation("pop1")
    pop1.create(4)
    pop1.connect(source=stim, rule='all', weight=0.01)
    pop1.record()

    # Create population 2
    pop2 = ExcitatoryPopulation("pop2")
    pop2.create(4)
    pop2.connect(source=pop1, rule='all', weight=0.01)
    pop2.record()

    # Create population 3
    pop3 = ExcitatoryPopulation("pop3")
    pop3.create(4)
    pop3.connect(source=pop2, rule='all', weight=0.01)
    pop3.record()

    show_conectivity_graph(pop1.cells + pop2.cells + pop3.cells)

    # Run
    sim = RunSim(init_v=-70, warmup=20)
    for i in range(1000):
        sim.run(runtime=1)
        pop1.plot(animate=True)
        pop2.plot(animate=True)
        pop3.plot(animate=True)
