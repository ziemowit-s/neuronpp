import unittest
import numpy as np
from neuron import h

from neuronpp.cells.cell import Cell
from neuronpp.core.distributions import Dist, UniformDist, NormalTruncatedDist, NormalConnectionProba
from neuronpp.core.populations.population import Population


class TestSeed(unittest.TestCase):
    def test_seed(self):
        Dist.set_seed(13)
        self.assertEqual(13, np.random.get_state()[1][0])


class TestCellDistparam(unittest.TestCase):
    def setUp(self):
        self.cell = Cell(name="cell")

    def tearDown(self):
        self.cell.remove_immediate_from_neuron()

        l = len(list(h.allsec()))
        if len(list(h.allsec())) != 0:
            raise RuntimeError("Not all section have been removed after teardown. "
                               "Sections left: %s" % l)

    def test_uniform(self):
        num = 100
        Dist.set_seed(13)
        avgs = []
        vars = []
        ls = []
        for i in range(20):
            for i in range(num):
                s = self.cell.add_sec("dend", l=UniformDist(low=1, high=10))
                ls.append(s.hoc.L)
                s.remove_immediate_from_neuron()

            vars.append(np.var(ls))
            avgs.append(np.average(ls))

        self.assertEqual(5.3644, round(np.average(avgs), 4))
        self.assertEqual(7.0346, round(np.average(vars), 4))

    def test_normal(self):
        num = 100
        Dist.set_seed(13)
        avgs = []
        vars = []
        ls = []
        for i in range(20):
            for i in range(num):
                s = self.cell.add_sec("dend", l=NormalTruncatedDist(mean=5, std=2))
                ls.append(s.hoc.L)
                s.remove_immediate_from_neuron()

            vars.append(np.var(ls))
            avgs.append(np.average(ls))

        std = np.sqrt(np.average(vars))
        std_diff = round(abs(std-2), 2)

        avg = np.average(avgs)
        avg_diff = round(abs(avg-5), 2)

        self.assertLess(std_diff, 0.1)
        self.assertLess(avg_diff, 0.05)


class TestPopulationalDistparam(unittest.TestCase):
    def setUp(self):
        def cell():
            c = Cell(name="cell")
            c.add_sec("soma", nseg=10, l=10)
            return c
        self.pop1 = Population("pop1")
        self.pop1.add_cells(num=100, cell_function=cell)

        self.pop2 = Population("pop2")
        self.pop2.add_cells(num=100, cell_function=cell)

    def tearDown(self):
        self.pop1.remove_immediate_from_neuron()
        self.pop2.remove_immediate_from_neuron()

        l = len(list(h.allsec()))
        if len(list(h.allsec())) != 0:
            raise RuntimeError("Not all section have been removed after teardown. "
                               "Sections left: %s" % l)

    def test_con_proba1(self):
        error = True
        try:
            NormalConnectionProba(threshold=1, mean=10, std=2)
            error = False
        except ValueError:
            self.assertTrue(error)

    def test_con_proba2(self):
        error = True
        try:
            NormalConnectionProba(threshold=0.5, mean=0.5, std=10)
            error = False
        except ValueError:
            self.assertTrue(error)

    def test_con_proba3(self):
        error = True
        try:
            NormalConnectionProba(threshold=10, mean=0.5, std=0.5)
            error = False
        except ValueError:
            self.assertTrue(error)

    def test_con_proba4(self):
        error = True
        try:
            NormalConnectionProba(threshold=-1, mean=0.5, std=0.5)
            error = False
        except ValueError:
            self.assertTrue(error)

    def test_con_proba5(self):
        error = True
        try:
            NormalConnectionProba(threshold=0.5, mean=-2, std=0.5)
            error = False
        except ValueError:
            self.assertTrue(error)

    def test_con_proba6(self):
        error = True
        try:
            NormalConnectionProba(threshold=0.5, mean=0.5, std=-2)
            error = False
        except ValueError:
            self.assertTrue(error)

    def test_con_proba7(self):
        error = True
        try:
            NormalConnectionProba(threshold=0.5, mean=0.5, std=0.5)
            error = False
        except ValueError:
            self.assertFalse(error)

    def test_con_proba8(self):
        error = True
        try:
            NormalConnectionProba(threshold=0, mean=0, std=0)
            error = False
        except ValueError:
            self.assertFalse(error)

    def test_uniform_cell_proba_uniform_seg_dist(self):
        Dist.set_seed(13)
        conn = self.pop2.connect(rule="all", cell_proba=0.5, seg_dist="uniform")
        conn.set_source([c.filter_secs("soma")(0.5) for c in self.pop1.cells])
        conn.set_target(self.pop2.cells)
        conn.add_synapse("Exp2Syn").add_netcon(weight=0.5)
        conn.build()

        syns = [c.syns for c in self.pop2.cells]
        print('a')

    def test_normal_cell_proba_uniform_seg_dist(self):
        Dist.set_seed(13)
        conn = self.pop2.connect(rule="all", seg_dist="uniform",
                                 cell_proba=NormalConnectionProba(threshold=0.5, mean=0.1, std=0.01))
        conn.set_source([c.filter_secs("soma")(0.5) for c in self.pop1.cells])
        conn.set_target(self.pop2.cells)
        conn.add_synapse("Exp2Syn").add_netcon(weight=0.5)
        conn.build()

        syns = [c.syns for c in self.pop2.cells]
        print('a')


if __name__ == '__main__':
    unittest.main()

