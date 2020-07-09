import os
import unittest
import numpy as np

from neuron import h
from neuronpp.cells.cell import Cell
from neuronpp.utils.iclamp import IClamp
from neuronpp.utils.record import Record
from neuronpp.utils.simulation import Simulation
from neuronpp.core.cells.netstim_cell import NetStimCell

path = os.path.dirname(os.path.abspath(__file__))


class TestSimulation(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.first_rec = None

    def setUp(self):
        """
        Setup call after each test, however from the NEURON point of view - all created HOC
        objects exist, so each new call of setUp() creates a separated new cell on which tests are
        performed
        """
        morpho_path = os.path.join(path, "..", "commons/morphologies/asc/cell2.asc")
        self.cell = Cell(name="cell")
        self.cell.load_morpho(filepath=morpho_path)
        self.cell.insert("pas")
        self.cell.insert("hh")

        self.soma = self.cell.filter_secs("soma")
        self.apic1 = self.cell.filter_secs('apic[1]')

    def test_netstim_before_sim(self):
        """
        NetStim run in a regular way before Simulation run, in this cale (netcon weight=1.0)
        we have spike of the soma.

        However NetStim start is in the absolute time.
        4 error
        """
        # Netstim to synapse
        stim = NetStimCell("stim").make_netstim(start=25, number=10, interval=2)
        self.cell.add_synapse(source=stim, netcon_weight=1.0, mod_name="ExpSyn", delay=1,
                              seg=self.apic1(0.5))
        # Record
        rec = Record(self.soma(0.5))
        # Run
        sim = Simulation(init_v=-70, warmup=20)
        sim.run(1)

        sim.run(100)
        r = rec.as_numpy(variable="v")

        # Make assertions
        self.assertEqual(4051, r.size)
        self.assertEqual(34.5205, round(r.records.max(), 4))
        self.assertEqual(-75.3053, round(r.records.min(), 4))

        self.assertEqual(319, r.records.argmax())
        # time in ms of max mV value
        self.assertEqual(27.725, round(r.time[r.records.argmax()], 4))

    def test_netstim_after_sim(self):
        """
        NetStim created after simulation run has no effect, it won't go on this simulation at all.

        However NetStim start is in the absolute time.
        3
        """
        # Record
        rec = Record(self.soma(0.5))
        # Run
        sim = Simulation(init_v=-70, warmup=20)
        sim.run(1)

        # Netstim to synapse
        stim = NetStimCell("stim").make_netstim(start=25, number=10, interval=2)
        self.cell.add_synapse(source=stim, netcon_weight=0.5, mod_name="ExpSyn", delay=1,
                              seg=self.apic1(0.5))
        sim.run(100)
        r = rec.as_numpy(variable="v")

        # Make assertions
        self.assertEqual(4051, r.size)
        self.assertEqual(-67.1917, round(r.records.max(), 4))
        self.assertEqual(-70.0, round(r.records.min(), 4))

        self.assertEqual(3, r.records.argmax())
        # time in ms of max mV value
        self.assertEqual(6, round(r.time[r.records.argmax()], 4))

    def test_iclamp_before_sim(self):
        """
        IClamp works in a regular way before simulation run. in this case (amplitude 3 pA)
        we have spike at the soma.

        However IClamp delay is in the absolute time.
        2
        """
        # Record
        rec = Record(self.soma(0.5))

        # IClamp to soma
        iclamp = IClamp(segment=self.soma(0.5))
        iclamp.stim(delay=25, dur=3, amp=3)

        # Run
        sim = Simulation(init_v=-70, warmup=20)
        sim.run(1)

        sim.run(100)
        r = rec.as_numpy(variable="v")

        # Make assertions
        self.assertEqual(4051, r.size)
        self.assertEqual(34.3815, round(r.records.max(), 4))
        self.assertEqual(-75.3247, round(r.records.min(), 4))

        self.assertEqual(330, r.records.argmax())
        # time in ms of max mV value
        self.assertEqual(28, round(r.time[r.records.argmax()], 4))

    def test_iclamp_after_sim(self):
        """
        IClamp works in a regular way after simulation run. in this case (amplitude 3 pA)
        we have spike at the soma.

        However IClamp delay is in the absolute time.
        1
        """
        # Record
        rec = Record(self.soma(0.5))

        # Run
        sim = Simulation(init_v=-70, warmup=20)
        sim.run(1)

        # IClamp to soma
        iclamp = IClamp(segment=self.soma(0.5))
        iclamp.stim(delay=25, dur=3, amp=3)

        sim.run(100)
        r = rec.as_numpy(variable="v")

        # Make assertions
        self.assertEqual(4051, r.size)
        self.assertEqual(34.3815, round(r.records.max(), 4))
        self.assertEqual(-75.3247, round(r.records.min(), 4))

        self.assertEqual(330, r.records.argmax())
        # time in ms of max mV value
        self.assertEqual(28, round(r.time[r.records.argmax()], 4))

    def test_2_cells(self):
        """
        Test setup for 2 cells and their records which should be the same.

        After each creation of the Simulation object, the Record object is cleaned up
        (inside vector is empty) however on other Hoc object is removed eg. Sections.
        That means - each new sections and cell are retained in the current NEURON run.
        """

        def get_rec():
            rec = Record(self.soma(0.5))
            iclamp = IClamp(segment=self.soma(0.5))
            iclamp.stim(delay=25, dur=3, amp=3)
            sim = Simulation(init_v=-70, warmup=20)
            sim.run(100)
            return rec

        rec1 = get_rec()
        r1 = rec1.as_numpy('v').records

        self.setUp()

        rec2 = get_rec()
        r2 = rec2.as_numpy('v').records

        sim = Simulation(init_v=-70, warmup=20)
        sim.run(100)

        # Make assertions
        self.assertEqual(4011, r1.size)
        self.assertEqual(4011, r2.size)
        self.assertTrue(np.alltrue(r1 == r2))

    def test_record_before_sim(self):
        """
        Record created before simulation run is full of data
        6 error
        """
        # Record
        rec = Record(self.soma(0.5))

        # IClamp to soma
        iclamp = IClamp(segment=self.soma(0.5))
        iclamp.stim(delay=25, dur=3, amp=3)

        # Run
        sim = Simulation(init_v=-70, warmup=20)
        sim.run(1)
        print(h.t)

        sim.run(100)
        r = rec.as_numpy(variable="v")

        # Make assertions
        self.assertEqual(4051, r.size)
        self.assertEqual(34.3815, round(r.records.max(), 4))
        self.assertEqual(-75.3247, round(r.records.min(), 4))

        self.assertEqual(330, r.records.argmax())
        # time in ms of max mV value
        self.assertEqual(28, round(r.time[r.records.argmax()], 4))

    def test_record_after_sim(self):
        """
        record created after simulation run is empty
        5
        """
        # IClamp to soma
        iclamp = IClamp(segment=self.soma(0.5))
        iclamp.stim(delay=25, dur=3, amp=3)

        # Run
        sim = Simulation(init_v=-70, warmup=20)
        sim.run(1)
        print(h.t)

        # Record
        rec = Record(self.soma(0.5))

        sim.run(100)
        r = rec.as_numpy(variable="v")

        # Make assertion
        self.assertEqual(0, r.size)


if __name__ == '__main__':
    unittest.main()