import unittest
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

        syns, heads = cls.cell.add_synapses_with_spine(source=None, secs=soma, mod_name="Exp2Syn")
        cls.syns.extend(syns)
        cls.heads.extend(heads)

        syns, heads = cls.cell.add_synapses_with_spine(source=None, secs=apic1, mod_name="Exp2Syn")
        cls.syns.extend(syns)
        cls.heads.extend(heads)

        syns, heads = cls.cell.add_synapses_with_spine(source=None, secs=apic2, mod_name="Exp2Syn")
        cls.syns.extend(syns)
        cls.heads.extend(heads)
        cls.apic2_syn, cls.apic2_head = syns, heads

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
