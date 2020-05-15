import os
import unittest

from neuronpp.cells.cell import Cell
from neuronpp.utils.utils import template
from neuronpp.core.cells.netstim_cell import NetStimCell
from neuronpp.core.distributions import Dist, NormalTruncatedDist
from neuronpp.cells.ebner2019_ach_da_cell import Ebner2019AChDACell
from neuronpp.core.populations.population import Population, NormalProba

path = os.path.dirname(os.path.abspath(__file__))


class TestMultiMechPopulation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        morpho_path = os.path.join(path, "..", "commons/morphologies/swc/my.swc")

        TemplateCell = template(Cell)
        template_cell = TemplateCell(name="cell")
        template_cell.load_morpho(filepath=morpho_path)
        template_cell.insert("pas")
        template_cell.insert("hh")

        TemplateEbner2019AChDACell = template(Ebner2019AChDACell)
        template_ebner = TemplateEbner2019AChDACell(name="cell")
        template_ebner.load_morpho(filepath=morpho_path)

        # Create NetStim
        netstim = NetStimCell("stim1").make_netstim(start=21, number=100, interval=2)

        # Define connection probabilities
        Dist.set_seed(13)
        conn_dist = NormalProba(mean=0.5, std=0.1)
        weight_dist = NormalTruncatedDist(mean=0.01, std=0.02)

        # Create population 1
        cls.pop1 = Population("pop_0")
        cls.pop1.add_cells(template=template_cell, num=3)

        connector = cls.pop1.connect(proba=conn_dist)
        connector.set_source(netstim)
        connector.set_target([c.filter_secs("dend")(0.5) for c in cls.pop1.cells])
        mech_adder = connector.add_synapse("Exp2Syn")
        mech_adder.add_netcon(weight=weight_dist)
        connector.build()

        # Create population 2
        cls.pop2 = Population("pop_1")
        cls.pop2.add_cells(template=template_ebner, num=4)

        connector = cls.pop2.connect(proba=conn_dist)
        connector.set_source([c.filter_secs("soma")(0.5) for c in cls.pop1.cells])
        connector.set_target([c.filter_secs("dend")(0.5) for c in cls.pop2.cells])

        del (template_ebner.params_4p_syn['w_pre_init'])
        del (template_ebner.params_4p_syn['w_post_init'])
        mech_adder = connector.add_synapse("Syn4PAChDa")
        mech_adder.add_synaptic_params(w_pre_init=weight_dist, w_post_init=weight_dist,
                                       **template_ebner.params_4p_syn)
        mech_adder.add_netcon(weight=weight_dist)

        mech_adder = connector.add_synapse("SynACh")
        mech_adder.add_netcon(source=None, weight=1)
        mech_adder = connector.add_synapse("SynDa")
        mech_adder.add_netcon(source=None, weight=1)

        connector.set_synaptic_function(
            lambda syns: Ebner2019AChDACell.set_synaptic_pointers(syns[0],
                                                                  syns[1],
                                                                  syns[2]))
        connector.group_synapses()
        connector.build()

        #    self.reward_syns.append(da)
        #    self.punish_syns.append(ach)

        # Create population 3
        cls.pop3 = Population("pop_2")
        cls.pop3.add_cells(template=template_cell, num=5)

        connector = cls.pop3.connect(proba=conn_dist)
        connector.set_source([c.filter_secs("soma")(0.5) for c in cls.pop2.cells])
        connector.set_target([c.filter_secs("dend")(0.5) for c in cls.pop3.cells])
        mech_adder = connector.add_synapse("Exp2Syn")
        mech_adder.add_netcon(weight=weight_dist)
        connector.build()


class TestStandardPopulation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        morpho_path = os.path.join(path, "..", "commons/morphologies/swc/my.swc")

        TemplateCell = template(Cell)
        template_cell = TemplateCell(name="cell")
        template_cell.load_morpho(filepath=morpho_path)
        template_cell.insert("pas")
        template_cell.insert("hh")

        # Create NetStim
        netstim = NetStimCell("stim1").make_netstim(start=21, number=100, interval=2)

        # Define connection probabilities
        Dist.set_seed(13)
        conn_dist = NormalProba(mean=0.5, std=0.1)
        weight_dist = NormalTruncatedDist(mean=0.01, std=0.02)

        # Create population 1
        cls.pop1 = Population("pop_0")
        cls.pop1.add_cells(template=template_cell, num=3)

        connector = cls.pop1.connect(proba=conn_dist)
        connector.set_source(netstim)
        connector.set_target([c.filter_secs("dend")(0.5) for c in cls.pop1.cells])
        mech_adder = connector.add_synapse("Exp2Syn")
        mech_adder.add_netcon(weight=weight_dist)
        connector.build()

        # Create population 2
        cls.pop2 = Population("pop_1")
        cls.pop2.add_cells(template=template_cell, num=4)

        connector = cls.pop2.connect(proba=conn_dist)
        connector.set_source([c.filter_secs("soma")(0.5) for c in cls.pop1.cells])
        connector.set_target([c.filter_secs("dend")(0.5) for c in cls.pop2.cells])
        mech_adder = connector.add_synapse("Exp2Syn")
        mech_adder.add_netcon(weight=weight_dist)
        connector.build()

        # Create population 3
        cls.pop3 = Population("pop_2")
        cls.pop3.add_cells(template=template_cell, num=5)

        connector = cls.pop3.connect(proba=conn_dist)
        connector.set_source([c.filter_secs("soma")(0.5) for c in cls.pop2.cells])
        connector.set_target([c.filter_secs("dend")(0.5) for c in cls.pop3.cells])
        mech_adder = connector.add_synapse("Exp2Syn")
        mech_adder.add_netcon(weight=weight_dist)
        connector.build()

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
            if syn.mod_name == 'Syn4PAChDa':
                cell_name = syn.sources[0].parent.cell.name
                self.assertEqual(cell_name, pop2_names[i])

    def test_connections_pop3(self):
        current_cells = self.get_cells(self.pop3)
        # for numpy.random.seed(13)
        pop3_names = ["pop_1[cell][0]", "pop_1[cell][1]", "pop_1[cell][2]", "pop_1[cell][3]"]
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
        # for numpy.random.seed(13)
        weights = [0.005779780499030976, 0.02125693570562063,
                   .028274814097193554, 0.009683215635451629]
        for i, syn in enumerate(self.pop2.syns):
            if syn.mod_name == 'Syn4PAChDa':
                netcon_weight = syn.netcons[0].get_weight()
                self.assertEqual(netcon_weight, weights[i])

    def test_netcon_weight_pop3(self):
        current_weights_str = self.get_weights(self.pop3)
        # for numpy.random.seed(13)
        weights = [0.005779780499030976, 0.015232118906381384, 0.02125693570562063,
                   0.005133474962288749]
        for i, syn in enumerate(self.pop3.syns):
            netcon_weight = syn.netcons[0].get_weight()
            self.assertEqual(netcon_weight, weights[i])

    @staticmethod
    def get_weights(pop) -> str:
        return "[%s]" % ', '.join([str(syn.netcons[0].get_weight()) for syn in pop.syns])

    @staticmethod
    def get_cells(pop) -> str:
        return '["%s"]' % '", "'.join([syn.sources[0].parent.cell.name for syn in pop.syns])


if __name__ == '__main__':
    unittest.main()
