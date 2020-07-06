import os

from neuronpp.cells.cell import Cell
from neuronpp.utils.simulation import Simulation
from neuronpp.core.cells.netstim_cell import NetStimCell
from neuronpp.utils.graphs.network_graph import NetworkGraph
from neuronpp.core.populations.population import Population, NormalProba
from neuronpp.core.distributions import Dist, NormalTruncatedDist, NormalTruncatedSegDist

path = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    def cell_function():
        cell = Cell(name="cell")
        morpho_path = os.path.join(path, "..", "commons/morphologies/swc/my.swc")
        cell.load_morpho(filepath=morpho_path)
        cell.insert("pas")
        cell.insert("hh")
        cell.make_spike_detector(seg=cell.filter_secs("soma")(0.5))
        return cell

    # Create NetStim
    netstim = NetStimCell("stim").make_netstim(start=21, number=100, interval=2)

    # Define connection probabilities
    Dist.set_seed(13)
    connection_proba = NormalProba(mean=0.8, std=0.1)
    weight_dist = NormalTruncatedDist(mean=0.1, std=0.2)

    # Create population 1
    pop1 = Population("pop_1")
    pop1.add_cells(num=4, cell_function=cell_function)

    connector = pop1.connect(cell_proba=connection_proba)
    connector.set_source(netstim)
    connector.set_target([c.filter_secs("dend")(0.5) for c in pop1.cells])
    syn_adder = connector.add_synapse("Exp2Syn")
    syn_adder.add_netcon(weight=weight_dist)

    connector.build()
    pop1.record()

    # Create population 2
    pop2 = Population("pop_2")
    pop2.add_cells(num=4, cell_function=cell_function)

    connector = pop2.connect(cell_proba=connection_proba, seg_dist=NormalTruncatedSegDist(0.5, 0.1))
    connector.set_source([c.filter_secs("soma")(0.5) for c in pop1.cells])
    connector.set_target([c.filter_secs("dend")(0.5) for c in pop2.cells])
    syn_adder = connector.add_synapse("Exp2Syn")
    syn_adder.add_netcon(weight=weight_dist)

    connector.build()
    pop2.record()

    # Create connectivity graph grouped by populations, with weighs and spike rates updated
    graph = NetworkGraph(populations=[pop1, pop2])
    graph.plot()

    # Run
    sim = Simulation(init_v=-70, warmup=20)
    for i in range(1000):
        sim.run(runtime=1)
        pop1.plot(animate=True)
        pop2.plot(animate=True)

        graph.update_weights()
        graph.update_spikes()
