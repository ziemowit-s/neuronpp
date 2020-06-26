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

    def test_cai_records(self):
        arr = self.cai_head0_rec.as_numpy()[:, 0, 0]
        self.assertEqual(arr.size, 915)

        self.assertEqual(np.argmax(arr), 336)
        self.assertEqual(round(np.max(arr), 4), 0.0061)

        self.assertEqual(np.argmin(arr), 0)
        self.assertEqual(np.min(arr), 0.0001)

        self.assertEqual(arr[0], 0.0001)
        self.assertEqual(round(arr[500], 4), 0.0054)
        self.assertEqual(round(arr[-1], 3), 0.001)

    def test_v_records(self):
        arr = self.v_soma_rec.as_numpy()[:, 0, 0]
        self.assertEqual(arr.size, 915)

        self.assertEqual(np.argmax(arr), 395)
        self.assertEqual(round(np.max(arr), 4), 36.4358)

        self.assertEqual(np.argmin(arr), 903)
        self.assertEqual(round(np.min(arr), 4), -76.9668)

        self.assertEqual(arr[0], -70)
        self.assertEqual(round(arr[500], 4), -15.8164)
        self.assertEqual(round(arr[-1], 4), -76.6513)


if __name__ == '__main__':
    unittest.main()
