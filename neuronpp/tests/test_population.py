import os
import unittest

from neuronpp.core.distributions import Dist, NormalTruncatedDist
from neuronpp.cells.cell_template import CellTemplate
from neuronpp.core.cells.netstim_cell import NetStimCell
from neuronpp.core.populations.population import Population, NormalProba

path = os.path.dirname(os.path.abspath(__file__))


class TestPopulation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cell_template = CellTemplate(name="cell")
        morpho_path = os.path.join(path, "..", "commons/morphologies/swc/my.swc")
        cell_template.load_morpho(filepath=morpho_path)
        cell_template.insert("pas")
        cell_template.insert("hh")

        # Create NetStim
        netstim = NetStimCell("stim1").make_netstim(start=21, number=100, interval=2)

        # Define connection probabilities
        Dist.set_seed(13)
        conn_dist = NormalProba(mean=0.5, std=0.1)
        weight_dist = NormalTruncatedDist(mean=0.01, std=0.02)

        # Create population 1
        cls.pop1 = Population("pop_0")
        cls.pop1.add_cells(template=cell_template, num=3)

        connector = cls.pop1.connect(proba=conn_dist) \
            .source(netstim) \
            .target([c.filter_secs("dend")(0.5) for c in cls.pop1.cells])
        connector.add_synapse("Exp2Syn") \
            .add_netcon(weight=weight_dist)
        connector.build()

        # Create population 2
        cls.pop2 = Population("pop_1")
        cls.pop2.add_cells(template=cell_template, num=4)

        connector = cls.pop2.connect(proba=conn_dist) \
            .source([c.filter_secs("soma")(0.5) for c in cls.pop1.cells]) \
            .target([c.filter_secs("dend")(0.5) for c in cls.pop2.cells])
        connector.add_synapse("Exp2Syn") \
            .add_netcon(weight=weight_dist)
        connector.build()

        # Create population 3
        cls.pop3 = Population("pop_2")
        cls.pop3.add_cells(template=cell_template, num=5)

        connector = cls.pop3.connect(proba=conn_dist) \
            .source([c.filter_secs("soma")(0.5) for c in cls.pop2.cells]) \
            .target([c.filter_secs("dend")(0.5) for c in cls.pop3.cells])
        connector.add_synapse("Exp2Syn") \
            .add_netcon(weight=weight_dist)
        connector.build()

        # Creates inhibitory connections between cls.pop2->cls.pop3
        for c in cls.pop3.cells:
            for p in c.pps:
                p.hoc.e = -90

    def test_cell_number(self):
        self.assertEqual(len(self.pop1.cells), 3)
        self.assertEqual(len(self.pop2.cells), 4)
        self.assertEqual(len(self.pop3.cells), 5)

    def test_connections_pop1(self):
        # for numpy.random.seed(13)
        for i, syn in enumerate(self.pop1.syns):
            netstim_name = syn.sources[0].parent.name
            self.assertEqual(netstim_name, "stim1")

    def test_connections_pop2(self):
        # for numpy.random.seed(13)
        pop2_names = ["pop_0[cell][1]", "pop_0[cell][1]", "pop_0[cell][1]", "pop_0[cell][2]"]
        for i, syn in enumerate(self.pop2.syns):
            cell_name = syn.sources[0].parent.cell.name
            self.assertEqual(cell_name, pop2_names[i])

    def test_connections_pop3(self):
        # for numpy.random.seed(13)
        pop3_names = ["pop_1[cell][0]", "pop_1[cell][0]", "pop_1[cell][1]", "pop_1[cell][1]",
                      "pop_1[cell][2]", "pop_1[cell][2]", "pop_1[cell][3]", "pop_1[cell][3]",
                      "pop_1[cell][3]"]
        for i, syn in enumerate(self.pop3.syns):
            cell_name = syn.sources[0].parent.cell.name
            self.assertEqual(cell_name, pop3_names[i])
            print(cell_name)

    def test_netcon_weight_pop1(self):
        # for numpy.random.seed(13)
        weights = [0.02507532757319406, 0.019036246774915794]
        for i, syn in enumerate(self.pop1.syns):
            netcon_weight = syn.netcons[0].get_weight()
            self.assertEqual(netcon_weight, weights[i])

    def test_netcon_weight_pop2(self):
        # ", ".join([str(syn.netcons[0].get_weight()) for syn in self.pop2.syns])
        # for numpy.random.seed(13)
        weights = [0.005779780499030976, 0.02125693570562063,
                   .028274814097193554, 0.009683215635451629]
        for i, syn in enumerate(self.pop2.syns):
            netcon_weight = syn.netcons[0].get_weight()
            self.assertEqual(netcon_weight, weights[i])

    def test_netcon_weight_pop3(self):
        # for numpy.random.seed(13)
        weights = [0.007095773348279606, 0.0044373096698245105, 0.01981743665019032,
                   0.0009249523751676137, 0.005280679393157255, 0.03276666094984303,
                   0.002597678437904911, 0.009605486370517344, 0.005351482559450754]
        for i, syn in enumerate(self.pop3.syns):
            netcon_weight = syn.netcons[0].get_weight()
            self.assertEqual(netcon_weight, weights[i])


if __name__ == '__main__':
    unittest.main()
