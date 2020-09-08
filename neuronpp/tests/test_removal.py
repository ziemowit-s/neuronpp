import unittest
from neuron import h

from neuronpp.cells.cell import Cell


def _get_secs():
    return len(list(h.allsec()))


class TestSection(unittest.TestCase):
    def setUp(self):
        self.cell = Cell(name="cell")
        self.soma = self.cell.add_sec("soma", diam=10, l=10, nseg=10)
        self.dend1 = self.cell.add_sec("dend1", diam=1, l=10, nseg=10)
        self.dend2 = self.cell.add_sec("dend2", diam=1, l=10, nseg=10)
        self.cell.connect_secs(child=self.dend1, parent=self.soma, child_loc=0, parent_loc=0.1)
        self.cell.connect_secs(child=self.dend2, parent=self.soma, child_loc=0, parent_loc=0.9)

    def tearDown(self):
        self.soma.remove_immediate_from_neuron()
        self.dend1.remove_immediate_from_neuron()
        self.dend2.remove_immediate_from_neuron()
        self.cell.remove_immediate_from_neuron()

        all_sec_num = _get_secs()
        if all_sec_num != 0:
            raise RuntimeError("Not all section have been removed after teardown. "
                               "Sections left: %s" % all_sec_num)

    def test_remove_synapse(self):
        """
        Removal of the parent section doesn't remove child sections
        """
        dend3 = self.cell.add_sec("dend3", diam=1, l=10, nseg=10)
        self.cell.connect_secs(child=dend3, parent=self.soma, child_loc=0, parent_loc=0.5)

        syn = self.cell.add_synapse(source=None, mod_name="Exp2Syn", seg=dend3(0.5))

        dend3 = None
        self.assertEqual(4, _get_secs())

        syn.remove_immediate_from_neuron()
        self.assertEqual(4, _get_secs())

    def test_remove_point_process(self):
        """
        Immediate removal of Point Process in outside reference makes
        that Point Process inside synapse also delete
        """
        syn = self.cell.add_synapse(source=None, mod_name="Exp2Syn", seg=self.dend2(0.5))
        syn.point_process.remove_immediate_from_neuron()
        self.assertEqual(0, len(self.cell.syns[0].point_process.__dict__))

    def test_remove_synapse2(self):
        """
        Remove outside reference and inside (Cell's) reference deletes section from NEURON
        """
        dend3 = self.cell.add_sec("dend3", diam=1, l=10, nseg=10)
        self.cell.connect_secs(child=dend3, parent=self.soma, child_loc=0, parent_loc=0.5)

        dend3 = None
        self.assertEqual(4, _get_secs())

        self.cell.secs = self.cell.secs[:3]
        self.assertEqual(3, len(self.cell.secs))
        self.assertEqual(3, _get_secs())

    def test_remove_synapse3(self):
        """
        Remove outside reference and inside (Cell's) reference doesn't delete section if it has
        reference inside the synapse
        """
        dend3 = self.cell.add_sec("dend3", diam=1, l=10, nseg=10)
        self.cell.connect_secs(child=dend3, parent=self.soma, child_loc=0, parent_loc=0.5)

        syn = self.cell.add_synapse(source=None, mod_name="Exp2Syn", seg=dend3(0.5))

        dend3 = None
        self.assertEqual(4, _get_secs())

        self.cell.secs = self.cell.secs[:3]
        self.assertEqual(3, len(self.cell.secs))
        self.assertEqual(4, _get_secs())

        syn.remove_immediate_from_neuron()
        self.assertEqual(3, _get_secs())

    def test_remove_soma(self):
        """
        Removal of the parent section doesn't remove child sections
        """
        self.soma.remove_immediate_from_neuron()
        self.assertEqual(2, _get_secs())

    def test_removal_sec_from_cell_object(self):
        """
        removal section by cell object - removes it from the cell object's self.secs list
        """
        self.cell.add_sec("dend3", diam=10, l=10, nseg=10)
        self.cell.remove_secs("dend3")
        self.assertEqual(3, _get_secs())
        self.assertEqual(3, len(self.cell.secs))

    def test_removal_sec_outside_cell_object(self):
        """
        removal section by itself - removes it from the cell object's self.secs list
        """
        dend3 = self.cell.add_sec("dend3", diam=10, l=10, nseg=10)
        dend3.remove_immediate_from_neuron()
        self.assertEqual(4, len(self.cell.secs))

    def test_removal_sec_outside_cell_object_clear_secs_manual(self):
        """
        removal section from secs clear also the object dend3
        """
        dend3 = self.cell.add_sec("dend3", diam=10, l=10, nseg=10)
        self.cell.secs.remove(dend3)
        self.assertEqual(3, len(self.cell.secs))

    def test_remove_dend1(self):
        """
        Removal of the parent section doesn't remove child sections
        """
        self.dend1.remove_immediate_from_neuron()
        self.assertEqual(2, _get_secs())

    def test_remove_dend1_soma(self):
        """
        Removal of the parent section doesn't remove child sections
        """
        self.soma.remove_immediate_from_neuron()
        self.dend1.remove_immediate_from_neuron()
        self.assertEqual(1, _get_secs())

    def test_remove_cell(self):
        """
        Removal of cell only doesn't remove any sections since their references are valid
        """
        self.cell.remove_immediate_from_neuron()
        self.assertEqual(3, _get_secs())

    def test_remove_sec_with_hoc_ref(self):
        """
        Immediate removal of Section doesn't remove it from NEURON if there is outside reference to
        the HOC object        that Point Process inside synapse also delete
        """
        hoc_soma = self.soma.hoc
        self.soma.remove_immediate_from_neuron()
        self.assertEqual(3, _get_secs())
        
    def test_remove_new_cell_with_no_ref(self):
        """
        deletion of cell, when all its sections have no reference outside - deletes all its
        sections as well
        """
        cell = Cell(name="cell")
        soma = cell.add_sec("soma")
        dend1 = cell.add_sec("dend1")
        dend2 = cell.add_sec("dend2")
        cell.connect_secs(child=dend1, parent=soma, child_loc=0, parent_loc=0.1)
        cell.connect_secs(child=dend2, parent=soma, child_loc=0, parent_loc=0.9)

        soma = None
        dend1 = None
        dend2 = None

        self.assertEqual(6, _get_secs())
        cell.remove_immediate_from_neuron()
        self.assertEqual(3, _get_secs())

    def test_remove_new_cell_with_del_ref(self):
        """
        deletion of cell, when all its outside references are deletes - deletes all its
        sections as well. But deletion of single soma won't delete section soma since its reference
        is still in Cell
        """
        cell = Cell(name="cell")
        soma = cell.add_sec("soma")
        dend1 = cell.add_sec("dend1")
        dend2 = cell.add_sec("dend2")
        cell.connect_secs(child=dend1, parent=soma, child_loc=0, parent_loc=0.1)
        cell.connect_secs(child=dend2, parent=soma, child_loc=0, parent_loc=0.9)

        del soma
        del dend1
        del dend2

        self.assertEqual(6, _get_secs())
        cell.remove_immediate_from_neuron()
        self.assertEqual(3, _get_secs())

    def test_remove_new_cell_with_remove_immediate(self):
        """
        remove immediate removes each section immediate only if there is no reference to the HOC
        object of this section outside the Sec object.
        """
        cell = Cell(name="cell")
        soma = cell.add_sec("soma")
        dend1 = cell.add_sec("dend1")
        dend2 = cell.add_sec("dend2")
        cell.connect_secs(child=dend1, parent=soma, child_loc=0, parent_loc=0.1)
        cell.connect_secs(child=dend2, parent=soma, child_loc=0, parent_loc=0.9)

        self.assertEqual(6, _get_secs())

        soma.remove_immediate_from_neuron()
        dend1.remove_immediate_from_neuron()
        dend2.remove_immediate_from_neuron()

        self.assertEqual(3, _get_secs())
        cell.remove_immediate_from_neuron()

    def test_removal_sec_after_synapse_remove(self):
        """
        Removing synapse allows to remove section as well
        """
        dend3 = self.cell.add_sec("dend3", diam=10, l=10, nseg=10)
        syn = self.cell.add_synapse(source=None, mod_name="Exp2Syn", seg=dend3(0.5))
        syn.remove_immediate_from_neuron()
        self.soma.remove_immediate_from_neuron()
        self.assertEqual(3, _get_secs())

    def test_removal_sec_as_part_of_synapse(self):
        """
        Removal of Sec which is a part of a Synapse won't delete the Section in NEURON as long as
        Synapse exists.
        """
        dend3 = self.cell.add_sec("dend3", diam=10, l=10, nseg=10)
        syn = self.cell.add_synapse(source=None, mod_name="Exp2Syn", seg=dend3(0.5))
        dend3.remove_immediate_from_neuron()
        self.assertEqual(4, _get_secs())

    def test_removal_sec_before_synapse_remove(self):
        """
        Removing section before removing synapse - makes that section is not removed. It is because
        we remove dend3 section, but self.cell still holds the reference to the synapse.
        """
        dend3 = self.cell.add_sec("dend3", diam=10, l=10, nseg=10)
        self.cell.add_synapse(source=None, mod_name="Exp2Syn", seg=dend3(0.5))
        dend3.remove_immediate_from_neuron()
        self.assertEqual(4, _get_secs())

    def test_removal_cell_before_synapse_remove(self):
        """
        Removing whole cell after none of its content's reference is stored out of the cell - makes
        all its content and synapses removal.
        """
        cell2 = Cell(name="cell2")
        dend3 = cell2.add_sec("dend3", diam=10, l=10, nseg=10)
        cell2.add_synapse(source=None, mod_name="Exp2Syn", seg=dend3(0.5))
        dend3 = None

        cell2.remove_immediate_from_neuron()
        self.assertEqual(3, _get_secs())
