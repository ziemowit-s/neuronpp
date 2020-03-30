import os
import unittest
import numpy as np
from neuron import h
from neuronpp.core.cells.spine_cell import SpineCell

class TestCellAddSpineToSectionDefault(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cell = SpineCell(name="cell")
        cls.soma = cell.add_sec("soma", add_leak=True)
        cell._add_spines_to_section(cls.soma, 0.5, 1, 1, 0.5, 0.5,
                                    None, None, None, None,
                                    add_leak=False)
        cls.head = cell.filter_secs("head")
        cls.neck = cell.filter_secs("neck")
        cell2 = SpineCell(name="cell2")
        cls.soma2 = cell2.add_sec("soma", add_leak=True)
        cell2._add_spines_to_section(cls.soma2, 0.3, .5, .5, 0.3, 0.3,
                                     None, None, None, None,
                                     add_leak=True)
        cls.head2 = cell2.filter_secs("head")
        cls.neck2 = cell2.filter_secs("neck")
        
    def test_head_diam(self):
        self.assertEqual(self.head.hoc.diam, 1.)

    def test_head_len(self):
        self.assertEqual(self.head.hoc.L, 1.)

    def test_neck_diam(self):
        self.assertEqual(self.neck.hoc.diam, .5)

    def test_neck_len(self):
        self.assertEqual(self.neck.hoc.L, .5)

    def test_head_no_passive(self):
        mechs = self.head.hoc.psection()
        self.assertEqual(mechs["density_mechs"], {})

    def test_head_ra(self):
        self.assertEqual(self.head.hoc.Ra, 35.4)

    def test_head_cm(self):
        self.assertEqual(self.head.hoc.cm, 1)

    def test_neck_no_passive(self):
        mechs = self.neck.hoc.psection()
        self.assertEqual(mechs["density_mechs"], {})

    def test_neck_parent(self):
        neck_parent = h.SectionRef(sec=self.neck.hoc).parent.name()
        self.assertEqual(neck_parent, self.soma.hoc.name())

    def test_head_parent(self):
        head_parent = h.SectionRef(sec=self.head.hoc).parent.name()
        self.assertEqual(head_parent, self.neck.hoc.name())

    def test_neck_parent_location(self):
        par = str(self.neck.hoc.psection()["morphology"]["parent"])
        neck_parent_loc = float(par.split("(")[1].split(")")[0])
        self.assertEqual(neck_parent_loc, 0.5)

    def test_head_parent(self):
        par = str(self.head.hoc.psection()["morphology"]["parent"])
        head_parent_loc = float(par.split("(")[1].split(")")[0])
        self.assertEqual(head_parent_loc, 1.0)

    def test2_head_diam(self):
        self.assertEqual(self.head2.hoc.diam, .5)

    def test2_head_len(self):
        self.assertEqual(self.head2.hoc.L, .5)

    def test2_neck_diam(self):
        self.assertEqual(self.neck2.hoc.diam, .3)

    def test2_neck_len(self):
        self.assertEqual(self.neck2.hoc.L, .3)

    def test2_head_passive(self):
        mechs = self.head2.hoc.psection()
        self.assertEqual(list(mechs["density_mechs"].keys()),
                         ["pas"])

    def test2_head_E_pas(self):
        self.assertEqual(self.head2.hoc.e_pas, -70.)

    def test2_head_g_pas(self):
        self.assertEqual(self.head2.hoc.g_pas, 0.001)

    def test2_neck_passive(self):
        mechs = self.neck2.hoc.psection()
        self.assertEqual(list(mechs["density_mechs"].keys()),
                         ["pas"])

    def test2_head_ra(self):
        self.assertEqual(self.head2.hoc.Ra, 35.4)

    def test2_head_cm(self):
        self.assertEqual(self.head2.hoc.cm, 1.)

    def test2_neck_parent(self):
        neck_parent = h.SectionRef(sec=self.neck2.hoc).parent.name()
        self.assertEqual(neck_parent, self.soma2.hoc.name())

    def test2_head_parent(self):
        head_parent = h.SectionRef(sec=self.head2.hoc).parent.name()
        self.assertEqual(head_parent, self.neck2.hoc.name())

    def test2_neck_parent_location(self):
        par = str(self.neck2.hoc.psection()["morphology"]["parent"])
        neck_parent_loc = float(par.split("(")[1].split(")")[0])
        self.assertEqual(neck_parent_loc, 0.3)

    def test2_head_parent(self):
        par = str(self.head2.hoc.psection()["morphology"]["parent"])
        head_parent_loc = float(par.split("(")[1].split(")")[0])
        self.assertEqual(head_parent_loc, 1.0)
        
if __name__ == '__main__':
    unittest.main()
