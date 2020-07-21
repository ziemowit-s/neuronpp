import os
import unittest
import numpy as np
from neuron import h

from neuronpp.cells.cell import Cell
from neuronpp.core.cells.netstim_cell import NetStimCell
from neuronpp.core.populations.population import Population
from neuronpp.core.distributions import Dist, NormalTruncatedDist, NormalDist

path = os.path.dirname(os.path.abspath(__file__))


def get_netcon_weights(pop):
    return [syn.netcons[0].get_weight() for syn in pop.syns]


def get_source_cells(pop):
    return [(syn.sources[0].parent.cell, syn.target.parent.parent.cell) for syn in pop.syns]


class TestStandardPopulation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        morpho_path = os.path.join(path, "..", "commons/morphologies/swc/my.swc")

        def cell_template():
            cell = Cell(name="cell")
            cell.load_morpho(filepath=morpho_path)
            cell.insert("pas")
            cell.insert("hh")
            return cell

        # Create NetStim
        cls.netstim = NetStimCell("stim1").make_netstim(start=21, number=100, interval=2)

        # Define connection probabilities
        Dist.set_seed(13)
        weight_dist = NormalDist(mean=0.01, std=0.024)

        # Create population 1
        cls.pop1 = Population("pop_0")
        cls.pop1.add_cells(num=30, cell_function=cell_template)

        connector = cls.pop1.connect(cell_connection_proba=0.6)
        connector.set_source(cls.netstim)
        connector.set_target([c.filter_secs("dend") for c in cls.pop1.cells])
        syn_adder = connector.add_synapse("Exp2Syn")
        syn_adder.add_netcon(weight=weight_dist)
        connector.build()

        # Create population 2
        cls.pop2 = Population("pop_1")
        cls.pop2.add_cells(num=40, cell_function=cell_template)

        connector = cls.pop2.connect(cell_connection_proba=0.8)
        connector.set_source([c.filter_secs("soma")(0.5) for c in cls.pop1.cells])
        connector.set_target([c.filter_secs("dend") for c in cls.pop2.cells])
        syn_adder = connector.add_synapse("Exp2Syn")
        syn_adder.add_netcon(weight=weight_dist)
        connector.build()

        # Create population 3
        cls.pop3 = Population("pop_2")
        cls.pop3.add_cells(num=50, cell_function=cell_template)

        connector = cls.pop3.connect(cell_connection_proba=0.3)
        connector.set_source([c.filter_secs("soma")(0.5) for c in cls.pop2.cells])
        connector.set_target([c.filter_secs("dend") for c in cls.pop3.cells])
        syn_adder = connector.add_synapse("Exp2Syn")
        syn_adder.add_netcon(weight=weight_dist)
        connector.build()

    @classmethod
    def tearDownClass(cls):
        cls.netstim.remove_immediate_from_neuron()
        cls.pop1.remove_immediate_from_neuron()
        cls.pop2.remove_immediate_from_neuron()
        cls.pop3.remove_immediate_from_neuron()

        l = len(list(h.allsec()))
        if len(list(h.allsec())) != 0:
            raise RuntimeError("Not all section have been removed after teardown. "
                               "Sections left: %s" % l)

    def test_cell_number(self):
        self.assertEqual(len(self.pop1.cells), 30)
        self.assertEqual(len(self.pop2.cells), 40)
        self.assertEqual(len(self.pop3.cells), 50)

    def test_connections_pop1(self):
        for i, syn in enumerate(self.pop1.syns):
            stim_cell_name = syn.sources[0].parent.name
            self.assertEqual(stim_cell_name, "stim1")

    def test_netcon_weight_pop1(self):
        pops = self.pop1.syns + self.pop2.syns + self.pop3.syns
        weights = [s.netcons[0].get_weight() for s in pops]
        avg = np.average(weights)
        std = np.std(weights)
        self.assertEqual(0.01, round(avg, 2))
        self.assertEqual(0.02, np.round(std, 2))


class TestConnectorAndSynAdder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        morpho_path = os.path.join(path, "..", "commons/morphologies/swc/my.swc")

        def cell_template():
            cell = Cell(name="cell")
            cell.load_morpho(filepath=morpho_path)
            cell.insert("pas")
            cell.insert("hh")
            return cell

        # Define connection probabilities
        Dist.set_seed(13)
        weight_dist1 = NormalTruncatedDist(mean=0.01, std=0.02)
        weight_dist2 = NormalTruncatedDist(mean=0.1, std=0.2)

        # Create population 1
        cls.pop1 = Population("pop_0")
        cls.pop1.add_cells(num=3, cell_function=cell_template)

        # Create population 2
        cls.pop2 = Population("pop_1")
        cls.pop2.add_cells(num=4, cell_function=cell_template)

        connector = cls.pop2.connect(cell_connection_proba=0.5)
        connector.set_source([c.filter_secs("soma")(0.5) for c in cls.pop1.cells])
        connector.set_target([c.filter_secs("dend") for c in cls.pop2.cells])
        connector.add_synapse("ExpSyn").add_netcon(weight=weight_dist1)
        connector.add_synapse("Exp2Syn").add_netcon(weight=1.5)
        connector.group_synapses(name="group1")
        connector.build()

        connector = cls.pop2.connect(cell_connection_proba=0.5)
        connector.set_source([c.filter_secs("soma")(0.5) for c in cls.pop1.cells])
        connector.set_target([c.filter_secs("dend") for c in cls.pop2.cells])
        connector.add_synapse("ExpSyn").add_netcon(weight=weight_dist2)
        connector.add_synapse("Exp2Syn").add_netcon(weight=10.5)
        connector.build()

    @classmethod
    def tearDownClass(cls):
        cls.pop1.remove_immediate_from_neuron()
        cls.pop2.remove_immediate_from_neuron()

        l = len(list(h.allsec()))
        if len(list(h.allsec())) != 0:
            raise RuntimeError("Not all section have been removed after teardown. "
                               "Sections left: %s" % l)

    def test(self):
        get_netcon_weights(self.pop2)
        get_source_cells(self.pop2)


class TestNamingConvention(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        def cell_name_template():
            return Cell(name="my custom name")

        def cell_noname_template():
            return Cell()

        # Create population with name for the cell template
        cls.pop1 = Population("pop_0")
        cls.pop1.add_cells(num=3, cell_function=cell_name_template)

        # Create population without name for the cell template
        cls.pop2 = Population("pop_1")
        cls.pop2.add_cells(num=3, cell_function=cell_noname_template)

    @classmethod
    def tearDownClass(cls):
        cls.pop1.remove_immediate_from_neuron()
        cls.pop2.remove_immediate_from_neuron()

        l = len(list(h.allsec()))
        if len(list(h.allsec())) != 0:
            raise RuntimeError("Not all section have been removed after teardown. "
                               "Sections left: %s" % l)

    def test_cell_with_name(self):
        self.assertEqual("pop_0[my custom name][0]", self.pop1.cells[0].name)
        self.assertEqual("pop_0[my custom name][1]", self.pop1.cells[1].name)
        self.assertEqual("pop_0[my custom name][2]", self.pop1.cells[2].name)

    def test_cell_with_name_string(self):
        self.assertEqual("Cell[pop_0[my custom name][0]]", str(self.pop1.cells[0]))
        self.assertEqual("Cell[pop_0[my custom name][1]]", str(self.pop1.cells[1]))
        self.assertEqual("Cell[pop_0[my custom name][2]]", str(self.pop1.cells[2]))

    def test_cell_without_name(self):
        self.assertEqual("pop_1[cell][0]", self.pop2.cells[0].name)
        self.assertEqual("pop_1[cell][1]", self.pop2.cells[1].name)
        self.assertEqual("pop_1[cell][2]", self.pop2.cells[2].name)

    def test_cell_without_name_string(self):
        self.assertEqual("Cell[pop_1[cell][0]]", str(self.pop2.cells[0]))
        self.assertEqual("Cell[pop_1[cell][1]]", str(self.pop2.cells[1]))
        self.assertEqual("Cell[pop_1[cell][2]]", str(self.pop2.cells[2]))


if __name__ == '__main__':
    unittest.main()
