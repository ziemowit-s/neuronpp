import os
import unittest
import numpy as np
from neuronpp.core.cells.spine_cell import SpineCell, SPINE_DIMENSIONS


class TestCellAddSpineToSection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cell = SpineCell(name="cell")
        cls.soma = cell.add_sec("soma", add_pas=True, nseg=10)
        cell._add_spines_to_section(cls.soma, "new", 0.5, 1, 1, 0.5, 0.5,
                                    None, None, None, None,
                                    add_pas=False)
        cls.head = cell.heads[0]
        cls.neck = cell.necks[0]
        cell2 = SpineCell(name="cell2")
        cls.soma2 = cell2.add_sec("soma", nseg=10, add_pas=True)
        cell2._add_spines_to_section(cls.soma2, "new", 0.3, .5, .5, 0.3, 0.3,
                                     None, None, None, None,
                                     add_pas=True)
        cls.head2 = cell2.heads[0]
        cls.neck2 = cell2.necks[0]

        cell3 = SpineCell(name="cell3")
        cls.soma3 = cell3.add_sec("soma", add_pas=True)
        cell3._add_spines_to_section(cls.soma3, "new", 0.3, .5, .5, 0.3, 0.3,
                                     -80, 1 / 30000, 100, 2)
        cls.head3 = cell3.heads[0]
        cls.neck3 = cell3.necks[0]

        cls.cell4 = SpineCell(name="cell4")
        cls.soma4 = cls.cell4.add_sec("soma", add_pas=True)
        cls.cell4._add_spines_to_section(cls.soma4, "new",
                                         [0.1, 0.2, 0.4, 0.8],
                                         .5, .5, 0.4, 0.4,
                                         -80, 1 / 40000, 100, 2)
        cls.head4 = cls.cell4.heads
        cls.neck4 = cls.cell4.necks

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
        parent = self.neck.parent
        self.assertEqual(parent, self.soma)

    def test_neck_parent_location(self):
        par = str(self.neck.hoc.psection()["morphology"]["parent"])
        neck_parent_loc = float(par.split("(")[1].split(")")[0])
        self.assertEqual(neck_parent_loc, 0.5)

    def test_head_parent1(self):
        self.assertEqual(self.head.parent, self.neck)

    def test_head_parent2(self):
        par = str(self.head.hoc.psection()["morphology"]["parent"])
        head_parent_loc = float(par.split("(")[1].split(")")[0])
        self.assertEqual(head_parent_loc, 1.0)

    def test2_head_parent3(self):
        par = str(self.head2.hoc.psection()["morphology"]["parent"])
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
        self.assertEqual(self.neck2.parent, self.soma2)

    def test2_head_parent(self):
        self.assertEqual(self.head2.parent, self.neck2)

    def test2_neck_parent_location(self):
        par = str(self.neck2.hoc.psection()["morphology"]["parent"])
        neck_parent_loc = float(par.split("(")[1].split(")")[0])
        self.assertEqual(neck_parent_loc, 0.3)

    def test3_head_e_pas(self):
        self.assertEqual(self.head3.hoc.e_pas, -80)

    def test3_neck_e_pas(self):
        self.assertEqual(self.neck3.hoc.e_pas, -80)

    def test3_head_g_pas(self):
        out = np.isclose(self.head3.hoc.g_pas, 1 / 30000)
        self.assertTrue(out)

    def test3_neck_g_pas(self):
        out = np.isclose(self.neck3.hoc.g_pas, 1 / 30000)
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
        self.assertEqual(head.parent, self.neck4[0])

    def test4_head_parents_1(self):
        head = self.head4[1]
        self.assertEqual(head.parent, self.neck4[1])

    def test4_head_parents_2(self):
        head = self.head4[2]
        self.assertEqual(head.parent, self.neck4[2])

    def test4_head_parents_3(self):
        head = self.head4[3]
        self.assertEqual(head.parent, self.neck4[3])

    def test4_neck_parents_0(self):
        neck = self.neck4[0]
        self.assertEqual(neck.parent, self.soma4)

    def test4_neck_parents_1(self):
        neck = self.neck4[1]
        self.assertEqual(neck.parent, self.soma4)

    def test4_neck_parents_2(self):
        neck = self.neck4[2]
        self.assertEqual(neck.parent, self.soma4)

    def test4_neck_parents_3(self):
        neck = self.neck4[3]
        self.assertEqual(neck.parent, self.soma4)

    def test3_neck0_parent_location(self):
        par = str(self.neck4[0].hoc.psection()["morphology"]["parent"])
        neck_parent_loc = float(par.split("(")[1].split(")")[0])
        self.assertEqual(neck_parent_loc, 0.1)

    def test3_neck1_parent_location(self):
        par = str(self.neck4[1].hoc.psection()["morphology"]["parent"])
        neck_parent_loc = float(par.split("(")[1].split(")")[0])
        self.assertEqual(neck_parent_loc, 0.2)

    def test3_neck0_parent_location1(self):
        par = str(self.neck4[2].hoc.psection()["morphology"]["parent"])
        neck_parent_loc = float(par.split("(")[1].split(")")[0])
        self.assertEqual(neck_parent_loc, 0.4)

    def test3_neck0_parent_location2(self):
        par = str(self.neck4[3].hoc.psection()["morphology"]["parent"])
        neck_parent_loc = float(par.split("(")[1].split(")")[0])
        self.assertEqual(neck_parent_loc, 0.8)

    def test_adding_heads_to_list(self):
        self.assertEqual(self.head4, self.cell4.heads)

    def test_adding_necks_to_list(self):
        self.assertEqual(self.neck4, self.cell4.necks)


class TestAddSpinesToSectionList(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cell1 = SpineCell(name="cell1")
        cls.dend1 = cls.cell1.add_sec("dend1", add_pas=True)
        cls.dend2 = cls.cell1.add_sec("dend2", add_pas=True)
        cls.cell1.connect_secs(cls.dend2, cls.dend1)
        cls.spine_density = 2 / 100
        cls.n_spines = 2
        cls.head_diam = cls.head_len = 1
        cls.neck_diam = cls.neck_len = 0.5
        cls.E_pas = -80
        cls.g_pas = 1 / 20000
        cls.ra = 100
        cls.cm = 1.1
        cls.out_1 = cls.cell1.add_spines_to_section_list([cls.dend1,
                                                          cls.dend2],
                                                         cls.spine_density,
                                                         spine_type="mushroom",
                                                         spine_E_pas=cls.E_pas,
                                                         spine_g_pas=cls.g_pas,
                                                         spine_ra=cls.ra,
                                                         spine_cm=cls.cm,
                                                         u_random=None,
                                                         area_density=False,
                                                         add_pas=True)

        cls.cell2 = SpineCell(name="cell2")
        cls.dend21 = cls.cell2.add_sec("dend1", add_pas=True)
        cls.dend22 = cls.cell2.add_sec("dend2", add_pas=True)
        cls.cell2.connect_secs(cls.dend21, cls.dend22)
        cls.out_2 = cls.cell2.add_spines_to_section_list([cls.dend21,
                                                          cls.dend22],
                                                         cls.spine_density,
                                                         spine_type="mushroom",
                                                         head_diam=cls.head_diam,
                                                         head_len=cls.head_len,
                                                         neck_diam=cls.neck_diam,
                                                         neck_len=cls.neck_len,
                                                         add_pas=False,
                                                         u_random=1,
                                                         area_density=False)
        cls.cell3 = SpineCell(name="cell3")
        cls.soma3 = cls.cell3.add_sec("soma", add_pas=False)
        cls.cell3.add_spines_to_section_list([cls.soma3],
                                             cls.spine_density,
                                             spine_type="weird",
                                             add_pas=False)

    def test_number_of_heads(self):
        self.assertEqual(len(self.cell1.heads), 4)

    def test_number_of_necks(self):
        self.assertEqual(len(self.cell1.necks), 4)

    def test_neck_parents(self):
        parents = []
        for neck in self.cell1.necks:
            parents.append(neck.parent)

        out = [self.dend1, self.dend1,
               self.dend2, self.dend2]
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

    def test_E_pas_1(self):
        e_pass = set([x.hoc.e_pas for x in self.cell1.necks])
        self.assertEqual(e_pass, set([self.E_pas]))

    def test_g_pas_1(self):
        g_pass = set([x.hoc.g_pas for x in self.cell1.necks])
        self.assertEqual(g_pass, set([self.g_pas]))

    def test_E_pas_2(self):
        e_pass = set([x.hoc.e_pas for x in self.cell1.heads])
        self.assertEqual(e_pass, set([self.E_pas]))

    def test_g_pas_2(self):
        g_pass = set([x.hoc.g_pas for x in self.cell1.heads])
        self.assertEqual(g_pass, set([self.g_pas]))

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

    def test_unknown_spine_head_diam(self):
        diams = set([x.hoc.diam for x in self.cell3.heads])
        head_diam = SPINE_DIMENSIONS["generic"]["head_diam"]
        self.assertEqual(diams, set([head_diam]))

    def test_unknown_spine_head_len(self):
        lens = set([x.hoc.L for x in self.cell3.heads])
        head_len = SPINE_DIMENSIONS["generic"]["head_len"]
        self.assertEqual(lens, set([head_len]))

    def test_unknown_spine_neck_diam(self):
        diams = set([x.hoc.diam for x in self.cell3.necks])
        neck_diam = SPINE_DIMENSIONS["generic"]["neck_diam"]
        self.assertEqual(diams, set([neck_diam]))

    def test_unknown_spine_neck_len(self):
        lens = set([x.hoc.L for x in self.cell3.necks])
        neck_len = SPINE_DIMENSIONS["generic"]["neck_len"]
        self.assertEqual(lens, set([neck_len]))

    def test_no_pas_1(self):
        out = []
        for head in self.cell3.heads:
            out.append("pas" in head.hoc.psection()["density_mechs"])
        self.assertEqual(set(out), set([False]))

    def test_head_name(self):
        outs = set(["mushroom" in x.hoc.name() for x in self.cell1.heads])
        self.assertEqual(outs, set([True]))

    def test_neck_name(self):
        outs = set(["mushroom" in x.hoc.name() for x in self.cell1.necks])
        self.assertEqual(outs, set([True]))

    def test_head_name(self):
        outs = set(["weird" in x.hoc.name() for x in self.cell3.heads])
        self.assertEqual(outs, set([True]))

    def test_neck_name(self):
        outs = set(["weird" in x.hoc.name() for x in self.cell3.necks])
        self.assertEqual(outs, set([True]))

    def test_equal(self):
        self.assertEqual(self.out_1, [np.linspace(0., .99, 2).tolist(),
                                      np.linspace(0., .99, 2).tolist()])

    def test_random(self):
        self.assertNotEqual(self.out_2[0],
                            np.linspace(0., .99, 2).tolist())


class TestFindingSectionsWithMechs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = os.path.dirname(os.path.abspath(__file__))
        f_path = os.path.join(path, "..", "commons/mods/combe2018")
        cls.cell = SpineCell("cell", compile_paths=f_path)
        cls.soma = cls.cell.add_sec("soma", add_pas=True, nseg=10)
        cls.soma.hoc.insert("hh")
        diam = 5
        lengths = np.linspace(100, 50, 10)
        cls.dends = []
        for i, length in enumerate(lengths):
            dend = cls.cell.add_sec("dend%d" % i, add_pas=True,
                                    nseg=int(length / 10), l=length)
            cls.dends.append(dend)
            if i == 0:
                cls.cell.connect_secs(dend, cls.soma)
            else:
                cls.cell.connect_secs(dend, cls.dends[i - 1])
        cls.cell.insert("calH", "dend", gcalbar=0.0002)
        cls.cell.insert("kca", "dend", gbar=0.00075)
        regions = cls.cell.filter_secs("dend", as_list=True)
        cls.cell.add_spines_to_section_list(regions, 0.02, "thin", add_pas=True)
        cls.cell.insert("calH", "head", gcalbar=0.0001)
        cls.find_calH = cls.cell.get_spines_by_section_with_mech("calH")
        cls.find_kca = cls.cell.get_spines_by_section_with_mech("kca")
        cls.find_all = cls.cell.get_spines_by_section_with_mech(None)

    def test_if_all_parents_accounted_for(self):
        dends = self.cell.filter_secs(obj_filter=lambda o: "dend" in o.name and
                                                           "head" not in o.name and
                                                           "neck" not in o.name)
        self.assertEqual(len(dends), len(self.find_calH))

    def test_no_found_secs(self):
        self.assertEqual({}, self.find_kca)

    def test_all_dends_with_spines(self):
        dends = self.cell.filter_secs(obj_filter=lambda o: "dend" in o.name and
                                                           "head" not in o.name and
                                                           "neck" not in o.name)
        self.assertEqual(len(self.find_all), len(dends))

    def test_all_dends_len(self):
        children = []
        for key in self.find_all.keys():
            children.extend(self.find_all[key])
        self.assertEqual(len(children), len(self.cell.spines))


class TestSpineFactor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = os.path.dirname(os.path.abspath(__file__))
        f_path = os.path.join(path, "..", "commons/mods/combe2018")
        cls.cell = SpineCell("cell", compile_paths=f_path)
        cls.soma = cls.cell.add_sec("soma", add_pas=True, nseg=10)
        cls.diam = 5
        cls.lengths = np.linspace(100, 50, 5)
        cls.dends = []
        for i, length in enumerate(cls.lengths):
            dend = cls.cell.add_sec("dend%d" % i, add_pas=True,
                                    nseg=int(length / 10), l=length,
                                    diam=cls.diam)
            cls.dends.append(dend)
            if i == 0:
                cls.cell.connect_secs(dend, cls.soma)
            else:
                cls.cell.connect_secs(dend, cls.dends[i - 1])
        regions = cls.cell.filter_secs("dend", as_list=True)
        cls.cell.add_spines_to_section_list(regions, 0.02,
                                            "thin", add_pas=True)
        cls.cell.insert("calH", cls.cell.heads, gcalbar=0.0001)
        cls.out_calH = cls.cell._get_spine_factor(cls.cell.spines[:2],
                                                  "calH", "gcalbar")
        cls.out_cm = cls.cell._get_spine_factor(cls.cell.spines[:2], "cm",
                                                None)

    def test_cm(self):
        out = 0
        for spine in self.cell.spines[:2]:
            for sec in spine.sections:
                out += sec.area
        self.assertEqual(self.out_cm, out)

    def test_calH(self):
        out = 0.2 * 0.5 * 2 * np.pi * 0.0001
        self.assertEqual(self.out_calH, out)


class TestCompensateForMechanism(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = os.path.dirname(os.path.abspath(__file__))
        f_path = os.path.join(path, "..", "commons/mods/combe2018")
        cls.cell = SpineCell("cell",
                             compile_paths=f_path)
        cls.soma = cls.cell.add_sec("soma", add_pas=True, nseg=10)
        cls.soma.hoc.insert("hh")
        diam = 5
        lengths = [10]
        cls.dends = []
        for i, length in enumerate(lengths):
            dend = cls.cell.add_sec("dend%d" % i, add_pas=True,
                                    nseg=int(length / 10), l=length, diam=diam)
            cls.dends.append(dend)
            if i == 0:
                cls.cell.connect_secs(dend, cls.soma)
            else:
                cls.cell.connect_secs(dend, cls.dends[i - 1])
        cls.gbar_dend = 0.0002
        cls.gbar_spine = 0.0001
        cls.gkca = 0.00075
        cls.cell.insert("calH", "dend", gcalbar=cls.gbar_dend)
        cls.cell.insert("kca", "dend", gbar=cls.gkca)
        regions = cls.cell.filter_secs("dend", as_list=True)
        cls.cell.add_spines_to_section_list(regions, 0.02, "thin",
                                            add_pas=True, spine_cm=10)
        cls.cell.insert("calH", "head", gcalbar=cls.gbar_spine)
        cls.cell.compensate(cm_adjustment=False, calH="gcalbar")
        cls.cell.compensate(cm_adjustment=False, kca="gbar")
        cls.cell.compensate(cm_adjustment=True)

    def test_cm(self):
        spine_factor = 0
        for spine in self.cell.spines:
            for sec in spine.sections:
                spine_factor += sec.hoc.cm * sec.area
        dend_area = self.dends[0].area
        new_cm = 1 * (dend_area - spine_factor) / dend_area
        out = np.isclose(new_cm, self.dends[0].hoc.cm)
        self.assertTrue(out)

    def test_kca1(self):
        kca = set(self.dends[0].hoc.psection()["density_mechs"]["kca"]["gbar"])
        self.assertEqual(len(kca), 1)

    def test_kca2(self):
        kca = self.dends[0].hoc.psection()["density_mechs"]["kca"]["gbar"]
        out = np.isclose(kca[0], self.gkca)
        self.assertTrue(out)

    def test_calH1(self):
        spine_factor = len(self.cell.heads) * 0.2 * 0.5 * np.pi * self.gbar_spine
        dend_factor = self.dends[0].hoc.diam * np.pi * self.dends[0].hoc.L * self.gbar_dend
        new_gbar = (dend_factor - spine_factor) / dend_factor
        gca = self.dends[0].hoc.psection()["density_mechs"]["calH"]["gcalbar"]

        self.assertEqual(set(gca), set([new_gbar]))


if __name__ == '__main__':
    unittest.main()
