from neuronpp.cells.cell import Cell
from neuronpp.core.cells.netstim_cell import NetStimCell
from neuronpp.core.populations.population import Population

from neuronpp.utils.run_sim import RunSim


class ExcitatoryPopulation(Population):
    def make_cell(self, **kwargs) -> Cell:
        cell = Cell(name="cell")
        cell.load_morpho(filepath='../commons/morphologies/swc/my.swc')
        cell.insert("pas")
        cell.insert("hh")
        return cell

    def make_conn(self, cell, source, source_loc=None, weight=1, **kwargs) -> list:
        syns, heads = cell.make_spine_with_synapse(source=source, mod_name="Exp2Syn",
                                                   source_loc=source_loc, weight=weight, target_sec="dend")
        return syns


if __name__ == '__main__':
    # Create NetStim
    stim = NetStimCell("stim").make_netstim(start=21, number=10, interval=10)

    # Create population 1
    pop1 = ExcitatoryPopulation("pop")
    pop1.create(2)
    pop1.connect(source=stim, rule='all', weight=0.01)
    pop1.record()

    # Create population 2
    pop2 = ExcitatoryPopulation("pop2")
    pop2.create(2)
    pop2.connect(source=pop1.cells, rule='all', source_sec_name="soma", source_loc=0.5, weight=0.01)
    pop2.record()

    # Run
    sim = RunSim(init_v=-70, warmup=20)
    for i in range(1000):
        sim.run(runtime=1)
        print('plot')
        pop1.plot(animate=True)
        pop2.plot(animate=True)
