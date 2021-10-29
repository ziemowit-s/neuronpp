import unittest
import numpy as np
from neuron import h
from neuronpp.core.cells.synaptic_spine_cell import SynapticSpineCell


class TestAddSynapsesWithSpine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cell = SynapticSpineCell(name="cell")
        soma = cls.cell.add_sec("soma")
        apic1 = cls.cell.add_sec("apic1")
        apic2 = cls.cell.add_sec("apic2")

        cls.syns = []
        cls.heads = []

        syns, heads = cls.cell.add_random_synapses_with_spine(source=None, secs=soma,
                                                              mod_name="Exp2Syn")
        cls.syns.extend(syns)
        cls.heads.extend(heads)

        syns, heads = cls.cell.add_random_synapses_with_spine(source=None, secs=apic1,
                                                              mod_name="Exp2Syn")
        cls.syns.extend(syns)
        cls.heads.extend(heads)

        syns, heads = cls.cell.add_random_synapses_with_spine(source=None, secs=apic2,
                                                              mod_name="Exp2Syn")
        cls.syns.extend(syns)
        cls.heads.extend(heads)
        cls.apic2_syn, cls.apic2_head = syns, heads

    @classmethod
    def tearDownClass(cls):
        for sy in cls.syns:
            sy.remove_immediate_from_neuron()
        for he in cls.heads:
            he.remove_immediate_from_neuron()
        cls.cell.remove_immediate_from_neuron()

        l = len(list(h.allsec()))
        if len(list(h.allsec())) != 0:
            raise RuntimeError("Not all section have been removed after teardown. "
                               "Sections left: %s" % l)

    def test_secs_heads_lens(self):
        secs = self.cell.filter_secs("soma,apic")
        heads = self.cell.heads
        self.assertEqual(len(secs), len(heads))

    def test_last_added_syns_heads_lens(self):
        self.assertEqual(len(self.apic2_syn), len(self.apic2_head))

    def test_all_returned_syns_heads_lens(self):
        self.assertEqual(len(self.syns), len(self.heads))

    def test_parents(self):
        for syn, head in zip(self.syns, self.heads):
            segment = syn.parent
            sec = segment.parent
            self.assertEqual(sec, head)


class TestAddRandomSynapsesWithSpine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cell = SynapticSpineCell(name="cell")
        soma = cls.cell.add_sec("soma")
        apic1 = cls.cell.add_sec("apic1")
        apic2 = cls.cell.add_sec("apic2")

        cls.syns = []
        cls.heads = []
        cls.N = 10

        # set random seed
        np.random.seed(31)

        secs = [soma, apic1, apic2]
        syns, heads = cls.cell.add_random_synapses_with_spine(source=None, secs=secs,
                                                              mod_name="Exp2Syn", number=cls.N)
        cls.syns.extend(syns)
        cls.heads.extend(heads)

    @classmethod
    def tearDownClass(cls):
        for sy in cls.syns:
            sy.remove_immediate_from_neuron()
        for he in cls.heads:
            he.remove_immediate_from_neuron()
        cls.cell.remove_immediate_from_neuron()

        l = len(list(h.allsec()))
        if len(list(h.allsec())) != 0:
            raise RuntimeError("Not all section have been removed after teardown. "
                               "Sections left: %s" % l)

        # reset random seed
        np.random.seed(None)

    def test_all_returned_syns_heads_lens(self):
        self.assertEqual(len(self.syns), len(self.heads))

    def test_parents(self):
        for syn, head in zip(self.syns, self.heads):
            segment = syn.parent
            sec = segment.parent
            self.assertEqual(sec, head)

    def test_random_number(self):
        self.assertEqual(len(self.syns), self.N)

    def test_loc(self):
        neck = self.heads[0].parent
        neck_loc = neck.parent_loc
        # the location of the first neck based on random seed
        self.assertEqual(neck_loc, 0.858161464981547)
