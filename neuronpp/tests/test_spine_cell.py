import os
import unittest
import numpy as np
from neuron import h
from neuronpp.core.cells.spine_cell import SpineCell, SPINE_DIMENSIONS

class TestCellAddSpineToSection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cell = SpineCell(name="cell")
        cls.soma = cell.add_sec("soma", add_leak=True, nseg=10)
        cell._add_spines_to_section(cls.soma, 0.5, 1, 1, 0.5, 0.5,
                                    None, None, None, None,
                                    add_leak=False)
        cls.head = cell.filter_secs("head")
        cls.neck = cell.filter_secs("neck")
        cell2 = SpineCell(name="cell2")
        cls.soma2 = cell2.add_sec("soma", nseg=10, add_leak=True)
        cell2._add_spines_to_section(cls.soma2, 0.3, .5, .5, 0.3, 0.3,
                                     None, None, None, None,
                                     add_leak=True)
        cls.head2 = cell2.filter_secs("head")
        cls.neck2 = cell2.filter_secs("neck")

        cell3 = SpineCell(name="cell3")
        cls.soma3 = cell3.add_sec("soma", add_leak=True)
        cell3._add_spines_to_section(cls.soma3, 0.3, .5, .5, 0.3, 0.3,
                                     -80, 1/30000, 100, 2)
        cls.head3 = cell3.filter_secs("head")
        cls.neck3 = cell3.filter_secs("neck")

        cls.cell4 = SpineCell(name="cell4")
        cls.soma4 = cls.cell4.add_sec("soma", add_leak=True)
        cls.cell4._add_spines_to_section(cls.soma4, [0.1, 0.2, 0.4, 0.8],
                                     .5, .5, 0.4, 0.4,
                                     -80, 1/40000, 100, 2)
        cls.head4 = cls.cell4.filter_secs("head")
        cls.neck4 = cls.cell4.filter_secs("neck")

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

    def test3_head_e_pas(self):
        self.assertEqual(self.head3.hoc.e_pas, -80)

    def test3_neck_e_pas(self):
        self.assertEqual(self.neck3.hoc.e_pas, -80)

    def test3_head_g_pas(self):
        out = np.isclose(self.head3.hoc.g_pas, 1/30000)
        self.assertTrue(out)

    def test3_neck_g_pas(self):
        out = np.isclose(self.neck3.hoc.g_pas, 1/30000)
        self.assertTrue(out)

    def test3_head_ra(self):
        self.assertEqual(self.head3.hoc.Ra, 100)

    def test3_neck_ra(self):
        self.assertEqual(self.neck3.hoc.Ra, 100)

    def test3_head_cm(self):
        self.assertEqual(self.head3.hoc.cm, 2)

    def test3_neck_cm(self):
        self.assertEqual(self.neck3.hoc.cm, 2)

    def test4_no_of_heads(self):
        self.assertEqual(len(self.head4), 4)

    def test4_no_of_necks(self):
        self.assertEqual(len(self.neck4), 4)

    def test4_head_parents_0(self):
        head = self.head4[0]
        head_parent = h.SectionRef(sec=head.hoc).parent.name()
        self.assertEqual(head_parent, self.neck4[0].hoc.name())

    def test4_head_parents_1(self):
        head = self.head4[1]
        head_parent = h.SectionRef(sec=head.hoc).parent.name()
        self.assertEqual(head_parent, self.neck4[1].hoc.name())

    def test4_head_parents_2(self):
        head = self.head4[2]
        head_parent = h.SectionRef(sec=head.hoc).parent.name()
        self.assertEqual(head_parent, self.neck4[2].hoc.name())

    def test4_head_parents_3(self):
        head = self.head4[3]
        head_parent = h.SectionRef(sec=head.hoc).parent.name()
        self.assertEqual(head_parent, self.neck4[3].hoc.name())

    def test4_neck_parents_0(self):
        neck_parent = h.SectionRef(sec=self.neck4[0].hoc).parent.name()
        self.assertEqual(neck_parent, self.soma4.hoc.name())

    def test4_neck_parents_1(self):
        neck_parent = h.SectionRef(sec=self.neck4[1].hoc).parent.name()
        self.assertEqual(neck_parent, self.soma4.hoc.name())

    def test4_neck_parents_2(self):
        neck_parent = h.SectionRef(sec=self.neck4[2].hoc).parent.name()
        self.assertEqual(neck_parent, self.soma4.hoc.name())

    def test4_neck_parents_3(self):
        neck_parent = h.SectionRef(sec=self.neck4[3].hoc).parent.name()
        self.assertEqual(neck_parent, self.soma4.hoc.name())

    def test3_neck0_parent_location(self):
        par = str(self.neck4[0].hoc.psection()["morphology"]["parent"])
        neck_parent_loc = float(par.split("(")[1].split(")")[0])
        self.assertEqual(neck_parent_loc, 0.1)
        
    def test3_neck1_parent_location(self):
        par = str(self.neck4[1].hoc.psection()["morphology"]["parent"])
        neck_parent_loc = float(par.split("(")[1].split(")")[0])
        self.assertEqual(neck_parent_loc, 0.2)

    def test3_neck0_parent_location(self):
        par = str(self.neck4[2].hoc.psection()["morphology"]["parent"])
        neck_parent_loc = float(par.split("(")[1].split(")")[0])
        self.assertEqual(neck_parent_loc, 0.4)

    def test3_neck0_parent_location(self):
        par = str(self.neck4[3].hoc.psection()["morphology"]["parent"])
        neck_parent_loc = float(par.split("(")[1].split(")")[0])
        self.assertEqual(neck_parent_loc, 0.8)

    def test_adding_heads_to_list(self):
        self.assertEqual(self.head4, self.cell4.heads)

    def test_adding_necks_to_list(self):
        self.assertEqual(self.neck4, self.cell4.necks)




class TestAddSpinesToSectionLocation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cell1 = SpineCell(name="cell1")
        cls.soma1 = cls.cell1.add_sec("soma", add_leak=True)
        cls.cell2 = SpineCell(name="cell2")
        cls.soma2 = cls.cell2.add_sec("soma", add_leak=True)
        cls.n_spines = 10
        cls.head_diam = cls.head_len = 1
        cls.neck_diam = cls.neck_len = 0.5
        cls.E_leak = -70
        cls.g_pas = 1/20000
        cls.ra = None
        cls.cm = None
        cls.out1 = cls.cell1._add_spines_to_section_with_location(cls.soma1,
                                                                  cls.n_spines,
                                                                  cls.head_diam,
                                                                  cls.head_len,
                                                                  cls.neck_diam,
                                                                  cls.neck_len,
                                                                  cls.E_leak,
                                                                  cls.g_pas,
                                                                  cls.ra, cls.cm,
                                                                  u_random=None)
        cls.out2 = cls.cell2._add_spines_to_section_with_location(cls.soma2,
                                                                  cls.n_spines,
                                                                  cls.head_diam,
                                                                  cls.head_len,
                                                                  cls.neck_diam,
                                                                  cls.neck_len,
                                                                  cls.E_leak,
                                                                  cls.g_pas,
                                                                  cls.ra,
                                                                  cls.cm,
                                                                  u_random=1)


    def test_equal(self):
        self.assertEqual(self.out1,
                         np.linspace(0., .99, self.n_spines).tolist())

    def test_random(self):
       self.assertNotEqual(self.out2,
                         np.linspace(0., .99, self.n_spines).tolist())

    def test_how_many_spines(self):
        self.assertEqual(len(self.out2), len(self.out1))

    def test_how_many_spines2(self):
        self.assertEqual(len(self.out2), len(self.cell2.heads))

    def test_how_many_spines3(self):
        self.assertEqual(len(self.out2), len(self.cell2.necks))

    def test_how_many_spines4(self):
        self.assertEqual(len(self.out1), len(self.cell1.heads))

    def test_how_many_spines5(self):
        self.assertEqual(len(self.out1), len(self.cell1.necks))

    def test_heads_diam1(self):
        diams = set([x.hoc.diam for x in self.cell1.heads])
        self.assertEqual(diams, set([self.head_diam]))

    def test_neck_diam1(self):
        diams = set([x.hoc.diam for x in self.cell1.necks])
        self.assertEqual(diams, set([self.neck_diam]))

    def test_heads_len1(self):
        lens = set([x.hoc.L for x in self.cell1.heads])
        self.assertEqual(lens, set([self.head_len]))

    def test_neck_len1(self):
        lens = set([x.hoc.L for x in self.cell1.necks])
        self.assertEqual(lens, set([self.neck_len]))

    def test_neck_g_pas(self):
        lens = set([x.hoc.g_pas for x in self.cell1.necks])
        self.assertEqual(lens, set([self.g_pas]))

    def test_neck_E_leak(self):
        lens = set([x.hoc.e_pas for x in self.cell1.necks])
        self.assertEqual(lens, set([self.E_leak]))

    def test_neck_ra(self):
        lens = set([x.hoc.Ra for x in self.cell1.necks])
        self.assertEqual(lens, set([self.ra]))

    def test_neck_cm(self):
        lens = set([x.hoc.cm for x in self.cell1.necks])
        self.assertEqual(lens, set([self.cm]))

    def test_neck_g_pas(self):
        lens = set([x.hoc.g_pas for x in self.cell1.necks])
        self.assertEqual(lens, set([self.g_pas]))

    def test_neck_E_leak(self):
        lens = set([x.hoc.e_pas for x in self.cell1.necks])
        self.assertEqual(lens, set([self.E_leak]))

    def test_neck_ra(self):
        lens = set([x.hoc.Ra for x in self.cell1.necks])
        self.assertEqual(lens, set([35.4]))

    def test_neck_cm(self):
        lens = set([x.hoc.cm for x in self.cell1.necks])
        self.assertEqual(lens, set([1]))

    def test_head_g_pas(self):
        lens = set([x.hoc.g_pas for x in self.cell1.heads])
        self.assertEqual(lens, set([self.g_pas]))

    def test_head_E_leak(self):
        lens = set([x.hoc.e_pas for x in self.cell1.heads])
        self.assertEqual(lens, set([self.E_leak]))

    def test_head_ra(self):
        lens = set([x.hoc.Ra for x in self.cell1.heads])
        self.assertEqual(lens, set([35.4]))

    def test_head_cm(self):
        lens = set([x.hoc.cm for x in self.cell1.heads])
        self.assertEqual(lens, set([1]))


class TestAddSpinesToSectionList(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cell1 = SpineCell(name="cell1")
        cls.dend1 = cls.cell1.add_sec("dend1", add_leak=True)
        cls.dend2 = cls.cell1.add_sec("dend2", add_leak=True)
        cls.cell1.connect_secs(cls.dend2, cls.dend1)
        cls.spine_density = 2/100
        cls.n_spines = 2
        cls.head_diam = cls.head_len = 1
        cls.neck_diam = cls.neck_len = 0.5
        cls.E_leak = -80
        cls.g_pas = 1/20000
        cls.ra = 100
        cls.cm = 1.1
        cls.cell1.add_spines_section_list([cls.dend1, cls.dend2],
                                          cls.spine_density,
                                          spine_type="mushroom",
                                          spine_E_leak=cls.E_leak,
                                          spine_g_pas=cls.g_pas,
                                          spine_ra=cls.ra,
                                          spine_cm=cls.cm,
                                          u_random=None,
                                          area_density=False)

        cls.cell2 = SpineCell(name="cell2")
        cls.dend21 = cls.cell2.add_sec("dend1", add_leak=True)
        cls.dend22 = cls.cell2.add_sec("dend2", add_leak=True)
        cls.cell2.connect_secs(cls.dend21, cls.dend22)
        cls.cell2.add_spines_section_list([cls.dend21, cls.dend22],
                                          cls.spine_density,
                                          spine_type="mushroom",
                                          head_diam=cls.head_diam,
                                          head_len=cls.head_len,
                                          neck_diam=cls.neck_diam,
                                          neck_len=cls.neck_len,
                                          add_leak=False,
                                          u_random=None,
                                          area_density=False)


    def test_number_of_heads(self):
        self.assertEqual(len(self.cell1.heads), 4)

    def test_number_of_necks(self):
        self.assertEqual(len(self.cell1.necks), 4)

    def test_neck_parents(self):
        parents = []
        for neck in self.cell1.necks:
            parents.append(h.SectionRef(sec=neck.hoc).parent.name())

        out = [self.dend1.hoc.name(), self.dend1.hoc.name(),
               self.dend2.hoc.name(), self.dend2.hoc.name()]
        self.assertEqual(out, parents)

    def test_head_diam1(self):
        diams = set([x.hoc.diam for x in self.cell1.heads])
        head_diam = SPINE_DIMENSIONS["mushroom"]["head_diam"]
        self.assertEqual(diams, set([head_diam]))

    def test_head_len1(self):
        lens = set([x.hoc.L for x in self.cell1.heads])
        head_len = SPINE_DIMENSIONS["mushroom"]["head_len"]
        self.assertEqual(lens, set([head_len]))

    def test_neck_diam1(self):
        diams = set([x.hoc.diam for x in self.cell1.necks])
        neck_diam = SPINE_DIMENSIONS["mushroom"]["neck_diam"]
        self.assertEqual(diams, set([neck_diam]))

    def test_neck_len1(self):
        lens = set([x.hoc.L for x in self.cell1.necks])
        neck_len = SPINE_DIMENSIONS["mushroom"]["neck_len"]
        self.assertEqual(lens, set([neck_len]))

    def test_head_diam2(self):
        diams = set([x.hoc.diam for x in self.cell2.heads])
        self.assertEqual(diams, set([self.head_diam]))

    def test_head_len2(self):
        lens = set([x.hoc.L for x in self.cell2.heads])
        self.assertEqual(lens, set([self.head_len]))

    def test_neck_diam2(self):
        diams = set([x.hoc.diam for x in self.cell2.necks])
        self.assertEqual(diams, set([self.neck_diam]))

    def test_neck_len2(self):
        lens = set([x.hoc.L for x in self.cell2.necks])
        self.assertEqual(lens, set([self.neck_len]))

    def test_E_leak_1(self):
        e_leaks = set([x.hoc.e_pas for x in self.cell1.necks])
        self.assertEqual(e_leaks, set([self.E_leak]))

    def test_g_pas_1(self):
        g_leaks = set([x.hoc.g_pas for x in self.cell1.necks])
        self.assertEqual(g_leaks, set([self.g_pas]))

    def test_E_leak_2(self):
        e_leaks = set([x.hoc.e_pas for x in self.cell1.heads])
        self.assertEqual(e_leaks, set([self.E_leak]))

    def test_g_pas_2(self):
        g_leaks = set([x.hoc.g_pas for x in self.cell1.heads])
        self.assertEqual(g_leaks, set([self.g_pas]))

    def test_ra_1(self):
        ras = set([x.hoc.Ra for x in self.cell1.necks])
        self.assertEqual(ras, set([self.ra]))

    def test_ra_2(self):
        ras = set([x.hoc.Ra for x in self.cell1.heads])
        self.assertEqual(ras, set([self.ra]))

    def test_cm_1(self):
        cms = set([x.hoc.cm for x in self.cell1.necks])
        self.assertEqual(cms, set([self.cm]))

    def test_cm_2(self):
        cms = set([x.hoc.cm for x in self.cell1.heads])
        self.assertEqual(cms, set([self.cm]))

if __name__ == '__main__':
    unittest.main()
