import re
import unittest

import numpy as np
from neuron import h

from neuronpp.core.cells.synaptic_cell import SynapticCell
from neuronpp.core.dists.distributions import UniformDist


class TestAddSynapsesRandomUniformByLenght(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cell = SynapticCell(name="cell")
        soma = cls.cell.add_sec("soma", nseg=1000)
        apic1 = cls.cell.add_sec("apic1", nseg=1000)
        apic2 = cls.cell.add_sec("apic2", nseg=1000)

        cls.cell.connect_secs(child=apic1, parent=soma)
        cls.cell.connect_secs(child=apic2, parent=soma)

        cls.syns = []
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
                                                    mod_name="Exp2Syn", number=cls.N,
                                                    netcon_weight=UniformDist(low=1, high=2))
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

    def test_syns_len(self):
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

    def test_uniform_weight_dist(self):
        ws = [s.netcons[0].get_weight() for s in self.syns]
        self.assertEqual(1.5, round(np.average(ws), 1))


class TestAddSynapsesRandomUniformBySec(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cell = SynapticCell(name="cell")
        soma = cls.cell.add_sec("soma", nseg=1000)
        apic1 = cls.cell.add_sec("apic1", nseg=1000)
        apic2 = cls.cell.add_sec("apic2", nseg=1000)
        apic3 = cls.cell.add_sec("apic3", nseg=1000)
        apic4 = cls.cell.add_sec("apic4", nseg=1000)

        cls.cell.connect_secs(child=apic1, parent=soma)
        cls.cell.connect_secs(child=apic2, parent=soma)
        cls.cell.connect_secs(child=apic3, parent=soma)
        cls.cell.connect_secs(child=apic4, parent=soma)

        cls.N = 10000

        secs = [soma, apic1, apic2, apic3, apic4]
        cls.syns = cls.cell.add_random_uniform_synapses(source=None, secs=secs,
                                                    mod_name="Exp2Syn", number=cls.N,
                                                    netcon_weight=UniformDist(low=1, high=2),
                                                    uniform_by='sec')

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

    def test_syns_len(self):
        self.assertEqual(len(self.syns), self.N)

    def test_uniform_secs_distribution(self):
        secs = [s.parent.name.split('.')[1].split('(')[0] for s in self.syns]

        counts = []
        for s in set(secs):
            counts.append(secs.count(s))
        props = np.round(np.array(counts)/sum(counts), 1)
        self.assertTrue(np.all(props == 0.2))

    def test_uniform_locs_distribution(self):
        dd = {}
        for k, v in [(s.parent.name.split('.')[1].split('(')[0], s.parent.x) for s in self.syns]:
            if k not in dd:
                dd[k] = []
            dd[k].append(v)

        locs_uniform = np.round([np.mean(v) for v in dd.values()], 1)
        self.assertTrue(np.all(locs_uniform == 0.5))


    def test_uniform_weight_dist(self):
        ws = [s.netcons[0].get_weight() for s in self.syns]
        self.assertEqual(1.5, round(np.average(ws), 1))


class TestAddRandomCentroidNormalDistSynapses(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cell = SynapticCell(name="cell")
        soma = cls.cell.add_sec("soma", nseg=1000, l=10, diam=10)
        apic1 = cls.cell.add_sec("apic1", nseg=1000, l=50, diam=2)
        apic2 = cls.cell.add_sec("apic2", nseg=1000, l=50, diam=2)

        apic3 = cls.cell.add_sec("apic3", nseg=1000, l=50, diam=2)
        apic4 = cls.cell.add_sec("apic4", nseg=1000, l=50, diam=2)

        cls.cell.connect_secs(child=apic1, parent=soma)
        cls.cell.connect_secs(child=apic2, parent=soma)
        cls.cell.connect_secs(child=apic3, parent=apic2, parent_loc=0.5)
        cls.cell.connect_secs(child=apic4, parent=apic2, parent_loc=0.5)

        cls.centroid = apic2(0.5)
        cls.std = 30

        cls.syns = []
        cls.N = 100
        cls.RAND_SEED = 31

        cls.secs_max_len = int(sum([s.hoc.L for s in [soma, apic1, apic2]]))

        # set random seed
        np.random.seed(cls.RAND_SEED)

        secs = [soma, apic1, apic2]
        dist = UniformDist(low=1, high=2)
        syns = cls.cell.add_random_centroid_normal_dist_synapses(source=None, secs=secs,
                                                                 centroid=cls.centroid, std=cls.std,
                                                                 mod_name="Exp2Syn", number=cls.N,
                                                                 netcon_weight=dist)
        cls.syns.extend(syns)

    @classmethod
    def tearDownClass(cls):
        del cls.centroid
        for sy in cls.syns:
            sy.remove_immediate_from_neuron()
        cls.cell.remove_immediate_from_neuron()

        l = len(list(h.allsec()))
        if len(list(h.allsec())) != 0:
            raise RuntimeError("Not all section have been removed after teardown. "
                               "Sections left: %s" % l)

        # reset random seed
        np.random.seed(None)

    def test_syns_len(self):
        self.assertEqual(len(self.syns), self.N)

    def test_truncated_normal_dist_of_centroid(self):
        """
        distribution is truncated to only positive values (absolute) and between min-max
        distance from the centroid of all segments
        """
        np.random.seed(self.RAND_SEED)

        dists_to_centroid = [h.distance(self.centroid.hoc, s.parent.hoc) for s in self.syns]
        mean = np.mean(dists_to_centroid)
        std = np.std(dists_to_centroid)

        norm = np.abs(np.random.normal(loc=0, scale=self.std, size=self.N * 100))

        segs = [seg for sec in self.cell.secs for seg in sec.segs if seg.area > 0]
        dists_seg_ids = []
        for segi, seg in enumerate(segs):
            dists_seg_ids.append((h.distance(self.centroid.hoc, seg.hoc), segi))

        dists = [d[0] for d in dists_seg_ids]
        normal_locs = np.array([l for l in norm if min(dists) <= l <= max(dists)])[:self.N]
        norm_mean = np.mean(normal_locs)
        norm_std = np.std(normal_locs)
        print("a")

        self.assertEqual(round(norm_mean, 3), round(mean, 3))
        self.assertEqual(round(norm_std, 3), round(std, 3))
