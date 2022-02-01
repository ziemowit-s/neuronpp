import re
import unittest

import numpy as np
from neuron import h

from neuronpp.core.cells.synaptic_cell import SynapticCell


class TestAddRandomSynapses(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cell = SynapticCell(name="cell")
        soma = cls.cell.add_sec("soma", nseg=1000)
        apic1 = cls.cell.add_sec("apic1", nseg=1000)
        apic2 = cls.cell.add_sec("apic2", nseg=1000)

        cls.syns = []
        cls.heads = []
        cls.N = 100
        cls.RAND_SEED = 31

        # the location of the first synapse based on random seed
        cls.FIRST_SYN_RAND_NUM = 0.28605382166051563
        cls.LAST_SYN_RAND_NUM = 0.7714921151583348

        cls.secs_max_len = int(sum([s.hoc.L for s in [soma, apic1, apic2]]))

        # set random seed
        np.random.seed(cls.RAND_SEED)

        secs = [soma, apic1, apic2]
        syns = cls.cell.add_random_uniform_synapses(source=None, secs=secs,
                                                    mod_name="Exp2Syn", number=cls.N)
        cls.syns.extend(syns)

    @classmethod
    def tearDownClass(cls):
        for sy in cls.syns:
            sy.remove_immediate_from_neuron()
        cls.cell.remove_immediate_from_neuron()

        l = len(list(h.allsec()))
        if len(list(h.allsec())) != 0:
            raise RuntimeError("Not all section have been removed after teardown. "
                               "Sections left: %s" % l)

        # reset random seed
        np.random.seed(None)

    def test_rand_seed_for_secs(self):
        np.random.seed(self.RAND_SEED)
        rands = np.random.rand(self.N)
        self.assertEqual(self.FIRST_SYN_RAND_NUM, rands[0])
        self.assertEqual(self.LAST_SYN_RAND_NUM, rands[-1])

    def test_all_returned_syns_heads_lens(self):
        self.assertEqual(len(self.syns), self.N)

    def test_parents(self):
        for syn, head in zip(self.syns, self.heads):
            segment = syn.parent
            sec = segment.parent
            self.assertEqual(sec, head)

    def test_random_number(self):
        self.assertEqual(len(self.syns), self.N)

    def test_first_syn_loc(self):
        syn = self.syns[0]
        syn_sec = syn.parent.parent
        syn_sec_L = syn_sec.hoc.L

        point_process_name = syn.point_process.name
        all_nums = re.findall("\d+\.\d+", point_process_name)

        loc = float(all_nums[0])
        first_sec_loc = (self.FIRST_SYN_RAND_NUM * self.secs_max_len) / syn_sec_L

        self.assertEqual(len(all_nums), 1)
        self.assertEqual(loc, first_sec_loc)
        self.assertEqual(round(syn.parent.x, 2), round(first_sec_loc, 2))

    def test_last_syn_loc(self):
        syn = self.syns[-1]
        syn_sec = syn.parent.parent
        syn_sec_L = syn_sec.hoc.L

        point_process_name = syn.point_process.name
        all_nums = re.findall("\d+\.\d+", point_process_name)

        loc = float(all_nums[0])
        last_loc_all = self.LAST_SYN_RAND_NUM * self.secs_max_len
        last_sec_loc = (last_loc_all - self.secs_max_len + syn_sec_L) / syn_sec_L

        self.assertEqual(len(all_nums), 1)
        self.assertEqual(loc, last_sec_loc)
        self.assertEqual(round(syn.parent.x, 2), round(last_sec_loc, 2))

    def test_soma_syn_locs(self):
        for s in self.syns:
            point_process_name = s.point_process.name
            all_nums = re.findall("\d+\.\d+", point_process_name)
            loc = float(all_nums[0])
            self.assertEqual(len(all_nums), 1)
            self.assertEqual(round(s.parent.x, 2), round(loc, 2))
