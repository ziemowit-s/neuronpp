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
        cls.v_soma_rec = Record([cls.soma(0.5), cls.syns[0].parent], variables='v')
        cls.cai_head0_rec = Record(cls.syns[0].parent, variables='cai')

        # Run
        sim = Simulation(init_v=-70, warmup=20, with_neuron_gui=False, constant_timestep=False)
        sim.run(runtime=100)

        cls.cai_records = cls.cai_head0_rec.as_numpy()[:, 0, 0]
        cls.v_records = cls.v_soma_rec.as_numpy()[:, 0, 0]

    def test_cai_record_size(self):
        self.assertEqual(self.cai_records.size, 912)

    def test_cai_max_record(self):
        self.assertEqual(np.argmax(self.cai_records), 336)
        self.assertEqual(round(np.max(self.cai_records), 4), 0.0061)

    def test_cai_min_record(self):
        self.assertEqual(np.argmin(self.cai_records), 0)
        self.assertEqual(np.min(self.cai_records), 0.0001)

    def test_cai_first_record(self):
        self.assertEqual(self.cai_records[0], 0.0001)

    def test_cai_last_record(self):
        self.assertEqual(round(self.cai_records[-1], 3), 0.001)

    def test_cai_500ms_record(self):
        self.assertEqual(round(self.cai_records[500], 4), 0.0054)

    def test_v_record_size(self):
        self.assertEqual(self.v_records.size, 912)

    def test_v_max_record(self):
        self.assertEqual(np.argmax(self.v_records), 395)
        self.assertEqual(round(np.max(self.v_records), 4), 36.4358)

    def test_v_min_record(self):
        self.assertEqual(np.argmin(self.v_records), 900)
        self.assertEqual(round(np.min(self.v_records), 4), -76.9668)

    def test_v_first_record(self):
        self.assertEqual(self.v_records[0], -70)

    def test_v_last_record(self):
        self.assertEqual(-76.6498, round(self.v_records[-1], 4))

    def test_v_500ms_record(self):
        self.assertEqual(-15.8324, round(self.v_records[500], 4))


if __name__ == '__main__':
    unittest.main()
