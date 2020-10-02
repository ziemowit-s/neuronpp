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

    def tearDown(self):
        self.soma.remove_immediate_from_neuron()
        self.apic1.remove_immediate_from_neuron()
        self.cell.remove_immediate_from_neuron()

        l = len(list(h.allsec()))
        if len(list(h.allsec())) != 0:
            raise RuntimeError("Not all section have been removed after teardown. "
                               "Sections left: %s" % l)

    def test_empty_method(self):
        sim = Simulation()
        self.assertFalse(sim.is_neuron_empty())

        self.soma.remove_immediate_from_neuron()
        self.apic1.remove_immediate_from_neuron()
        self.cell.remove_immediate_from_neuron()

        self.assertTrue(sim.is_neuron_empty())

    def test_size_method(self):
        sim = Simulation()
        self.assertEqual(198, sim.size)

        self.soma.remove_immediate_from_neuron()
        self.apic1.remove_immediate_from_neuron()
        self.cell.remove_immediate_from_neuron()

        self.assertEqual(0, sim.size)

    def test_dt(self):
        rec = Record(self.soma(0.5))

        sim = Simulation(dt=10)
        sim.run(100)
        r1 = rec.as_numpy('v')

        sim = Simulation(dt=0.01)
        sim.run(100)
        r2 = rec.as_numpy('v')

        sim.remove_immediate_from_neuron()
        rec.remove_immediate_from_neuron()

        self.assertEqual(11, r1.size)
        self.assertEqual(10001, r2.size)

    def test_init_v(self):
        rec = Record(self.soma(0.5))

        sim = Simulation(init_v=-100)
        sim.run(100)
        r1 = rec.as_numpy('v')

        sim = Simulation(init_v=100)
        sim.run(100)
        r2 = rec.as_numpy('v')

        sim.remove_immediate_from_neuron()
        rec.remove_immediate_from_neuron()

        self.assertEqual(-100, r1.records[0])
        self.assertEqual(100, r2.records[0])

    def test_timestep_constant(self):
        rec = Record(self.soma(0.5))

        sim = Simulation(constant_timestep=True, dt=1)
        sim.run(100)
        r1 = rec.as_numpy('v')

        sim = Simulation(constant_timestep=False, dt=1)
        sim.run(100)
        r2 = rec.as_numpy('v')

        sim = Simulation(constant_timestep=False, dt=10)
        sim.run(100)
        r3 = rec.as_numpy('v')

        sim = Simulation(constant_timestep=False, dt=0.0001)
        sim.run(100)
        r4 = rec.as_numpy('v')

        sim.remove_immediate_from_neuron()
        rec.remove_immediate_from_neuron()

        self.assertEqual(101, r1.size)
        self.assertEqual(188, r2.size)
        self.assertEqual(180, r3.size)
        self.assertEqual(189, r4.size)

    def test_warmup(self):
        rec = Record(self.soma(0.5))

        value_error = False
        try:
            sim = Simulation(warmup=-100)
            sim.run(100)
            r1 = rec.as_numpy('v')
        except ValueError:
            value_error = True
        self.assertTrue(value_error)

        sim = Simulation(warmup=100, dt=1)
        sim.run(100)
        r2 = rec.as_numpy('v')

        sim = Simulation(warmup=100, dt=1, warmup_dt=1)
        sim.run(100)
        r3 = rec.as_numpy('v')

        sim.remove_immediate_from_neuron()
        rec.remove_immediate_from_neuron()

        self.assertEqual(111, r2.size)
        self.assertEqual(201, r3.size)

    def test_netstim_before_sim(self):
        """
        NetStim run in a regular way before Simulation run, in this cale (netcon weight=1.0)
        we have spike of the soma.

        However NetStim start is in the absolute time.
        """
        # Netstim to synapse
        stim = NetStimCell("stim").add_netstim(start=25, number=10, interval=2)
        self.cell.add_synapse(source=stim, netcon_weight=1.0, mod_name="ExpSyn", delay=1,
                              seg=self.apic1(0.5))
        # Record
        rec = Record(self.soma(0.5))
        # Run
        sim = Simulation(init_v=-70, warmup=20)
        sim.run(1)

        sim.run(100)
        r = rec.as_numpy(variable="v")

        stim.remove_immediate_from_neuron()
        sim.remove_immediate_from_neuron()
        rec.remove_immediate_from_neuron()

        # Make assertions
        self.assertEqual(4051, r.size)
        self.assertEqual(34.5205, round(r.records.max(), 4))
        self.assertEqual(-75.3053, round(r.records.min(), 4))

        self.assertEqual(319, r.records.argmax())
        # time in ms of max mV value
        self.assertEqual(27.725, round(r.time[r.records.argmax()], 4))

    def test_netcon_event_before_sim(self):
        """
        Netcon created before sim init or start is not effective and should return error
        """
        sim = Simulation()
        sim.reinit()
        syn = self.cell.add_synapse(source=None, netcon_weight=1.0, mod_name="ExpSyn", delay=1,
                                    seg=self.apic1(0.5))
        error = False
        try:
            syn.make_event(50)
        except ConnectionRefusedError:
            error = True

        self.assertTrue(error)

    def test_netcon_event_after_sim(self):
        syn = self.cell.add_synapse(source=None, netcon_weight=1.0, mod_name="ExpSyn", delay=1,
                                    seg=self.apic1(0.5))
        # Record
        rec = Record(self.soma(0.5))
        # Run
        sim = Simulation(init_v=-70, warmup=20)
        sim.run(1)

        syn.make_event(50)

        sim.run(100)
        r = rec.as_numpy(variable="v")

        syn.remove_immediate_from_neuron()
        sim.remove_immediate_from_neuron()
        rec.remove_immediate_from_neuron()

        # Make assertions
        self.assertEqual(4051, r.size)
        self.assertEqual(34.4582, round(r.records.max(), 4))
        self.assertEqual(-75.3478, round(r.records.min(), 4))

        self.assertEqual(2159, r.records.argmax())
        # time in ms of max mV value
        self.assertEqual(73.725, round(r.time[r.records.argmax()], 4))

    def test_netstim_after_sim(self):
        """
        NetStim created after simulation run has no effect, it won't go on this simulation at all.

        However NetStim start is in the absolute time.
        """
        # Record
        rec = Record(self.soma(0.5))
        # Run
        sim = Simulation(init_v=-70, warmup=20)
        sim.run(1)

        # Netstim to synapse
        stim = NetStimCell("stim").add_netstim(start=25, number=10, interval=2)
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
        self.assertEqual(6, r.time[r.records.argmax()])

        stim.remove_immediate_from_neuron()
        sim.remove_immediate_from_neuron()
        rec.remove_immediate_from_neuron()

    def test_iclamp_before_sim(self):
        """
        IClamp works in a regular way before simulation run. in this case (amplitude 3 pA)
        we have spike at the soma.

        However IClamp delay is in the absolute time.
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

        sim.remove_immediate_from_neuron()
        rec.remove_immediate_from_neuron()
        iclamp.remove_immediate_from_neuron()

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

        sim.remove_immediate_from_neuron()
        rec.remove_immediate_from_neuron()
        iclamp.remove_immediate_from_neuron()

        # Make assertions
        self.assertEqual(4051, r.size)
        self.assertEqual(34.3815, round(r.records.max(), 4))
        self.assertEqual(-75.3247, round(r.records.min(), 4))

        self.assertEqual(330, r.records.argmax())
        # time in ms of max mV value
        self.assertEqual(28, round(r.time[r.records.argmax()], 4))

    def test_2_runs(self):
        """
        Test setup for 2 cells and their records which should be the same.

        After each creation of the Simulation object, the Record object is cleaned up
        (inside vector is empty) however on other Hoc object is removed eg. Sections.
        That means - each new sections and cell are retained in the current NEURON run.
        """

        def run_and_get_rec():
            rec = Record(self.soma(0.5))
            iclamp = IClamp(segment=self.soma(0.5))
            iclamp.stim(delay=25, dur=3, amp=3)
            sim = Simulation(init_v=-70, warmup=20)
            sim.run(100)
            return rec

        rec1 = run_and_get_rec()
        r1 = rec1.as_numpy('v').records

        self.tearDown()
        self.setUp()

        rec2 = run_and_get_rec()
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
