import os
import unittest
import numpy as np
from neuron import h

from neuronpp.cells.cell import Cell
from neuronpp.utils.record import Record
from neuronpp.utils.simulation import Simulation
from neuronpp.utils.experiment import Experiment

path = os.path.dirname(os.path.abspath(__file__))


class TestExperimentAndRecord(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        morpho_path = os.path.join(path, "..", "commons/morphologies/asc/cell2.asc")

        # Create cell
        cell = Cell(name="cell")
        cell.load_morpho(filepath=morpho_path)
        cell.insert("pas")
        cell.insert("hh")

        soma = cell.filter_secs("soma")
        dend = cell.filter_secs("apic[10]")
        syn = cell.add_synapse(source=None, mod_name="ExpSyn", seg=dend(0.5))

        # Prepare EPSP and AP (IClamp) protocols
        experiment = Experiment(iti=40)
        experiment.add_epsp(num=3, synapse=syn, init=20, interval=20, weight=0.02)
        experiment.add_iclamp(num=3, segment=soma(0.5), init=60, interval=20, dur=3, amp=1.6)
        experiment.build()

        # Prepare plots
        rec = Record([soma(0.5), dend(0.5)], variables='v')

        # Run
        sim = Simulation(init_v=-70, warmup=20, with_neuron_gui=False, constant_timestep=True)
        sim.run(runtime=100)

        cls.v_soma = rec.as_numpy('v', segment_name=soma(.5).name)
        cls.v_apic = rec.as_numpy('v', segment_name=dend(.5).name)

        syn.remove_immediate_from_neuron()
        soma.remove_immediate_from_neuron()
        dend.remove_immediate_from_neuron()
        rec.remove_immediate_from_neuron()
        experiment.remove_immediate_from_neuron()
        cell.remove_immediate_from_neuron()
        sim.remove_immediate_from_neuron()

        cls.sections_left = len(list(h.allsec()))

    def removed_section(self):
        self.assertEqual(-1, self.l)

    def test_record_size(self):
        self.assertEqual(4011, self.v_soma.size)

    def test_apical_max_record(self):
        self.assertEqual(1655, np.argmax(self.v_apic.records))
        self.assertEqual(-43.7043, round(np.max(self.v_apic.records), 4))

    def test_apical_min_record(self):
        self.assertEqual(0, np.argmin(self.v_apic.records))
        self.assertEqual(-70.0, np.min(self.v_apic.records))

    def test_apical_first_record(self):
        self.assertEqual(-70.0, self.v_apic.records[0])

    def test_apical_last_record(self):
        self.assertEqual(-67.55, round(self.v_apic.records[-1], 3))

    def test_apical_50ms_record(self):
        v_in_50ms = self.v_apic.get_records_from_time(50)
        self.assertEqual(-67.5712, round(v_in_50ms[0], 4))

    def test_soma_max_record(self):
        self.assertEqual(1713, np.argmax(self.v_soma.records))
        self.assertEqual(-60.0896, round(np.max(self.v_soma.records), 4))

    def test_soma_min_record(self):
        self.assertEqual(0, np.argmin(self.v_soma.records))
        self.assertEqual(-70.0, round(np.min(self.v_soma.records), 4))

    def test_soma_first_record(self):
        self.assertEqual(-70, self.v_soma.records[0])

    def test_soma_last_record(self):
        self.assertEqual(-67.5551, round(self.v_soma.records[-1], 4))

    def test_soma_50ms_record(self):
        v_in_50ms = self.v_soma.get_records_from_time(50)
        self.assertEqual(-67.5403, round(v_in_50ms[0], 4))


if __name__ == '__main__':
    unittest.main()
