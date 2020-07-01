import os
import unittest
import numpy as np

from neuronpp.utils.simulation import Simulation

from neuronpp.cells.combe2018_cell import Combe2018Cell
from neuronpp.utils.experiment import Experiment
from neuronpp.utils.record import Record

path = os.path.dirname(os.path.abspath(__file__))


class TestExperimentAndRecord(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create cell
        cls.cell = Combe2018Cell(name="cell", spine_number=10, spine_secs_names="apic",
                                 spine_seed=13)

        cls.soma = cls.cell.filter_secs("soma")
        cls.syns = cls.cell.filter_complex_synapses(tag="combe")

        # Prepare STDP protocol
        cls.stdp = Experiment()
        cls.stdp.make_protocol("3xEPSP[int=10] 3xAP[int=10,dur=3,amp=1.6]", start=1, isi=10,
                               epsp_synapse=cls.syns[0], i_clamp_section=cls.soma)

        # Prepare plots
        cls.rec = Record([cls.soma(0.5), cls.syns[0].parent], variables='v cai')

        # Run
        sim = Simulation(init_v=-70, warmup=20, with_neuron_gui=False)
        sim.run(runtime=100)

        cls.v_soma = cls.rec.as_numpy('v', segment_name=cls.soma(.5).name)
        cls.cai = cls.rec.as_numpy('cai', segment_name=cls.syns[0].parent.name)

    def test_cai_record_size(self):
        self.assertEqual(4011, self.cai.size)

    def test_cai_max_record(self):
        self.assertEqual(516, np.argmax(self.cai.records))
        self.assertEqual(0.0062, round(np.max(self.cai.records), 4))

    def test_cai_min_record(self):
        self.assertEqual(0, np.argmin(self.cai.records))
        self.assertEqual(0.00005, np.min(self.cai.records))

    def test_cai_first_record(self):
        self.assertEqual(0.00005, self.cai.records[0])

    def test_cai_last_record(self):
        self.assertEqual(0.001, round(self.cai.records[-1], 3))

    def test_cai_50ms_record(self):
        cai = self.cai.get_records_from_time(50)
        self.assertEqual(0.0053, round(cai[0], 4))

    def test_v_record_size(self):
        self.assertEqual(4011, self.v_soma.size)

    def test_v_max_record(self):
        self.assertEqual(914, np.argmax(self.v_soma.records))
        self.assertEqual(36.7521, round(np.max(self.v_soma.records), 4))

    def test_v_min_record(self):
        self.assertEqual(3191, np.argmin(self.v_soma.records))
        self.assertEqual(-76.965, round(np.min(self.v_soma.records), 4))

    def test_v_first_record(self):
        self.assertEqual(-70, self.v_soma.records[0])

    def test_v_last_record(self):
        self.assertEqual(-76.6071, round(self.v_soma.records[-1], 4))

    def test_v_50ms_record(self):
        v = self.v_soma.get_records_from_time(50)
        self.assertEqual(-44.2341, round(v[0], 4))


if __name__ == '__main__':
    unittest.main()
