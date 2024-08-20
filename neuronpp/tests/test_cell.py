import os
import time
import unittest
import numpy as np
from neuron import h
from neuronpp.cells.cell import Cell
import shutil
from neuronpp.utils.compile_mod import compile_and_load_mods


class TestCellAddSectionDefault(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cell = Cell(name="cell")
        cls.cell_name = "my_simple_cell"
        cls.cell = Cell(name=cls.cell_name)
        cls.soma = cls.cell.add_sec("soma", add_pas=True)

        cls.dend1 = cls.cell.add_sec("dend1", add_pas=True)
        cls.dend2 = cls.cell.add_sec("dend2", add_pas=True)
        cls.cell.connect_secs(cls.dend1, cls.soma)
        cls.cell.connect_secs(cls.dend2, cls.soma)

    @classmethod
    def tearDownClass(cls):
        cls.soma.remove_immediate_from_neuron()
        cls.dend1.remove_immediate_from_neuron()
        cls.dend2.remove_immediate_from_neuron()
        cls.cell.remove_immediate_from_neuron()

        l = len(list(h.allsec()))
        if len(list(h.allsec())) != 0:
            raise RuntimeError("Not all section have been removed after teardown. "
                               "Sections left: %s" % l)

    def test_add_soma_L_default(self):
        self.assertEqual(self.soma.hoc.L, 100.)

    def test_add_soma_diam_default(self):
        self.assertEqual(self.soma.hoc.diam, 500.)

    def test_add_soma_cm_default(self):
        self.assertEqual(self.soma.hoc.cm, 1.)

    def test_add_soma_ra_default(self):
        self.assertEqual(self.soma.hoc.Ra, 35.4)

    def test_add_soma_g_pas_default(self):
        self.assertEqual(self.soma.hoc.g_pas, 0.001)

    def test_add_soma_e_pas_default(self):
        self.assertEqual(self.soma.hoc.e_pas, -70.0)

    def test_soma_name(self):
        self.assertEqual(self.soma.name, self.soma.hoc.name())

    def test_cell_parent(self):
        self.assertEqual(self.dend1.parent, self.soma)

    def test_cell_filter_obj(self):
        self.assertEqual(self.cell.filter_secs("soma"), self.soma)

    def test_cell_filter_list(self):
        self.assertEqual(len(self.cell.filter_secs("dend")), 2)


class TestCellAddSectionLeak(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cell1 = Cell(name="cell1")
        cls.soma1 = cell1.add_sec("soma", add_pas=True)
        cell2 = Cell(name="cell2")
        cls.soma2 = cell2.add_sec("soma", g_pas=0.002)
        cell3 = Cell(name="cell3")
        cls.soma3 = cell3.add_sec("soma", rm=1 / 0.003)

        cell4 = Cell(name="cell4")
        cls.soma4 = cell4.add_sec("soma", E_rest=-80)
        # no pas but add pas
        cls.cell5 = Cell(name="cell5")
        cls.soma5 = cls.cell5.add_sec("soma", add_pas=True)

        cls.dend = h.Section(name="dend", cell=cls.cell5)
        cls.dend.insert("pas")

        cell6 = Cell(name="cell6")
        cls.soma6 = cell6.add_sec("soma", add_pas=True)
        cls.soma6.hoc.insert("pas")
        cell6.set_pas("soma", Rm=1000, E_rest=-77, g_pas=0.002)

    @classmethod
    def tearDownClass(cls):
        cls.soma1.remove_immediate_from_neuron()
        cls.soma2.remove_immediate_from_neuron()
        cls.soma3.remove_immediate_from_neuron()
        cls.soma4.remove_immediate_from_neuron()
        cls.soma5.remove_immediate_from_neuron()
        cls.soma6.remove_immediate_from_neuron()
        cls.dend = None

        l = len(list(h.allsec()))
        if len(list(h.allsec())) != 0:
            raise RuntimeError("Not all section have been removed after teardown. "
                               "Sections left: %s" % l)

    def test_cell1_g_pas(self):
        self.assertEqual(self.soma1.hoc.g_pas, 0.001)

    def test_cell1_E_pas(self):
        self.assertEqual(self.soma1.hoc.e_pas, -70.0)

    def test_cell2_g_pas(self):
        self.assertEqual(self.soma2.hoc.g_pas, 0.002)

    def test_cell2_E_pas(self):
        self.assertEqual(self.soma2.hoc.e_pas, -70.0)

    def test_cell3_g_pas(self):
        self.assertTrue(np.isclose(self.soma3.hoc.g_pas, 0.003))

    def test_cell3_E_pas(self):
        self.assertEqual(self.soma3.hoc.e_pas, -70.0)

    def test_cell4_g_pas(self):
        self.assertEqual(self.soma4.hoc.g_pas, 0.001)

    def test_cell4_E_pas(self):
        self.assertEqual(self.soma4.hoc.e_pas, -80.0)

    def test_cell5(self):
        self.cell5.set_pas("soma", E_rest=-80)
        self.assertEqual(self.soma5.hoc.e_pas, -80)

    def test_cell5_dend(self):
        self.cell5.set_pas(self.dend, E_rest=-80)
        self.assertEqual(self.dend.e_pas, -80)

    def test_cell5_dend_rm(self):
        self.cell5.set_pas(self.dend, Rm=10000)
        self.assertEqual(self.dend.g_pas, 1 / 10000)

    def test_cell5_dend_g_pas(self):
        self.cell5.set_pas(self.dend, g_pas=0.02)
        self.assertEqual(self.dend.g_pas, 0.02)

    def test_cell6_soma_e_pas(self):
        self.assertEqual(self.soma6.hoc.g_pas, 0.002)

    def test_cell6_soma_g_pas(self):
        self.assertEqual(self.soma6.hoc.e_pas, -77)


class TestFiltering(unittest.TestCase):
    def test_distance(self):
        path = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(path, "..",
                                "commons/morphologies/asc/cell1.asc")
        cell = Cell("cell")
        cell.load_morpho(filepath=filepath)
        soma = cell.filter_secs("soma")

        # Filter sections by distance to the soma (return only those distance > 1000 um)
        far_secs = cell.filter_secs(
            obj_filter=lambda s: h.distance(soma.hoc(0.5), s.hoc(0.5)) > 1000)
        self.assertEqual(len(far_secs), 32)

        soma.remove_immediate_from_neuron()
        for s in far_secs:
            s.remove_immediate_from_neuron()
        cell.remove_immediate_from_neuron()

        self.assertEqual(0, len(list(h.allsec())))



class TestMODCompile(unittest.TestCase):

    def test_mod_override(self):
        path = os.path.dirname(os.path.abspath(__file__))
        f_path = os.path.join(path, "..", "commons/mods/combe2018")

        # first remove compile path
        shutil.rmtree(f_path, ignore_errors=True, onerror=None)

        # compile first
        target_path = compile_and_load_mods(f_path, override=True, wait_in_sec=2)

        cat_path = os.path.join(target_path, "cad.mod")
        first_mod_time = os.path.getmtime(cat_path)

        time.sleep(2)

        # compile second
        compile_and_load_mods(f_path, override=True, wait_in_sec=2)
        second_mod_time = os.path.getmtime(cat_path)

        # Check if the file modification time has changed
        self.assertNotEqual(first_mod_time, second_mod_time,
                            "The file cad.mod did not change after the second compilation.")


if __name__ == '__main__':
    unittest.main()
