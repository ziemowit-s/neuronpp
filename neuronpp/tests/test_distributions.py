import unittest
import numpy as np
from neuron import h

from neuronpp.cells.cell import Cell
from neuronpp.core.distributions import Dist, UniformDist, NormalTruncatedDist
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
            return Cell(name="cell")
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

    def test_connection_proba(self):
        self.pop2.connect(rule="all", cell_proba=0.5,)


if __name__ == '__main__':
    unittest.main()

