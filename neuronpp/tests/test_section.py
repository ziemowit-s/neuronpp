import re
import unittest
from neuron import h

from neuronpp.cells.cell import Cell


class TestSection(unittest.TestCase):
    def setUp(self):
        self.cell = Cell(name="cell")

    def tearDown(self):
        self.cell.remove_immediate_from_neuron()

        l = len(list(h.allsec()))
        if len(list(h.allsec())) != 0:
            raise RuntimeError("Not all section have been removed after teardown. "
                               "Sections left: %s" % l)

    def test_default_name(self):
        """
        If the name exists it will add a number starting from 2 to the proposed name.
        """
        pat = re.compile("[1-9]")

        for i in range(10):
            self.cell.add_sec("dend")

        for i, dend in enumerate(self.cell.filter_secs(name="dend")):
            res = pat.search(dend.name)
            if i == 0:
                self.assertIsNone(res)
            else:
                self.assertEqual(i + 1, int(dend.name.replace("dend", "")))
            dend.remove_immediate_from_neuron()

    def test_regex_search(self):
        for i in range(10):
            self.cell.add_sec("dend")

        for i, dend in enumerate(self.cell.filter_secs("regex:dend[1-9]")):
            self.assertEqual(i + 2, int(dend.name.replace("dend", "")))

        for d in self.cell.secs:
            d.remove_immediate_from_neuron()

    def test_connections(self):
        soma = self.cell.add_sec(name="soma", l=10, nseg=10)
        dend = self.cell.add_sec(name="dend", l=100, nseg=10)
        self.cell.connect_secs(child=dend, parent=soma, child_loc=0, parent_loc=0.7)

        self.assertEqual(0, dend.orientation)
        self.assertEqual(0.7, dend.parent_loc)
        self.assertIsNone(soma.parent_loc)

    def test_allseg(self):
        soma = self.cell.add_sec(name="soma", diam=1, l=10, nseg=20)
        dend = self.cell.add_sec(name="dend", diam=1, l=100, nseg=200)
        self.assertEqual(22, len(soma.segs))
        self.assertEqual(202, len(dend.segs))

    def test_area1(self):
        soma = self.cell.add_sec(name="soma", diam=1, l=10, nseg=20)
        dend = self.cell.add_sec(name="dend", diam=1, l=100, nseg=200)

        self.assertEqual(0, soma.segs[0].area)
        self.assertEqual(0, soma.segs[-1].area)
        self.assertEqual(0, dend.segs[0].area)
        self.assertEqual(0, dend.segs[-1].area)

        for s in soma.segs[1:-1]:
            self.assertEqual(1.5708, round(s.area, 4))
        for s in dend.segs[1:-1]:
            self.assertEqual(1.5708, round(s.area, 4))

    def test_area2(self):
        apic = self.cell.add_sec(name="apic", diam=10, l=10, nseg=4)
        for s in apic.segs[1:-1]:
            self.assertEqual(78.5398, round(s.area, 4))


if __name__ == '__main__':
    unittest.main()

