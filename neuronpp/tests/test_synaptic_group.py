import unittest
from neuron import h

from neuronpp.utils.record import Record
from neuronpp.utils.simulation import Simulation
from neuronpp.core.cells.synaptic_group_cell import SynapticGroupCell


class TestSynapticGroup(unittest.TestCase):
    def setUp(self):
        self.cell = SynapticGroupCell(name="cell")
        self.soma = self.cell.add_sec("soma")
        self.apic1 = self.cell.add_sec("apic1")
        self.cell.connect_secs(self.apic1, self.soma)
        self.cell.insert("pas")
        self.cell.insert("hh")

        self.syn1 = self.cell.add_synapse(source=None, mod_name="Exp2Syn",
                                          seg=self.apic1(0.5), tag="syn1")
        self.syn2 = self.cell.add_synapse(source=None, mod_name="ExpSyn",
                                          seg=self.apic1(0.5), tag="syn2")
        self.cell.group_synapses(name="apic_group", tag="aa", synapses=[self.syn1, self.syn2])

        self.syn3 = self.cell.add_synapse(source=None, mod_name="Exp2Syn",
                                          seg=self.soma(0.5), tag="syn3")
        self.syn4 = self.cell.add_synapse(source=None, mod_name="ExpSyn",
                                          seg=self.soma(0.5), tag="syn4")
        self.cell.group_synapses(name="soma_group", tag="ss", synapses=[self.syn3, self.syn4])

    def tearDown(self):
        self.syn1.remove_immediate_from_neuron()
        self.syn2.remove_immediate_from_neuron()
        self.syn3.remove_immediate_from_neuron()
        self.syn4.remove_immediate_from_neuron()

        self.apic1.remove_immediate_from_neuron()
        self.soma.remove_immediate_from_neuron()
        self.cell.remove_immediate_from_neuron()

        l = len(list(h.allsec()))
        if len(list(h.allsec())) != 0:
            raise RuntimeError("Not all section have been removed after teardown. "
                               "Sections left: %s" % l)

    def test_name_and_tag_filter(self):
        g1 = self.cell.filter_synaptic_group(name="apic")
        g2 = self.cell.filter_synaptic_group(tag="aa")
        self.assertTrue(g1 == g2)
        self.assertTrue(g1 is not None)

        # Remove variables and clear NEURON
        g1.remove_immediate_from_neuron()
        g2.remove_immediate_from_neuron()

    def test_mod_name_filter(self):
        g1 = self.cell.filter_synaptic_group(mod_name="Exp2Syn", tag="aa")
        g2 = self.cell.filter_synaptic_group(mod_name="ExpSyn", name="apic")
        self.assertTrue(g1 == g2)
        self.assertTrue(g1 is not None)

        # Remove variables and clear NEURON
        g1.remove_immediate_from_neuron()
        g2.remove_immediate_from_neuron()

    def test_mod_filter(self):
        gs = self.cell.filter_synaptic_group(mod_name="Exp2Syn")
        self.assertEqual("aa", gs[0].tag)
        self.assertEqual("ss", gs[1].tag)

        # Remove variables and clear NEURON
        gs[0].remove_immediate_from_neuron()
        gs[1].remove_immediate_from_neuron()

    def test_add_netcon_and_make_event_separately(self):
        g1 = self.cell.filter_synaptic_group(mod_name="Exp2Syn", tag="aa")
        nc = g1.add_netcon(source=None)

        exp2syn_rec = Record(g1['Exp2Syn'][0], variables='i')
        expsyn_rec = Record(g1['ExpSyn'][0], variables='i')

        sim = Simulation()
        sim.run(1)
        nc['Exp2Syn'][0].make_event(10)
        nc['ExpSyn'][0].make_event(20)
        sim.run(100)

        exp2syn_np = exp2syn_rec.as_numpy('i')
        stim_time_exp2syn = exp2syn_np.time[(exp2syn_np.records != 0).argmax()]
        expsyn_np = expsyn_rec.as_numpy('i')
        stim_time_expsyn = expsyn_np.time[(expsyn_np.records != 0).argmax()]

        self.assertEqual(12.05, round(stim_time_exp2syn, 4))
        self.assertEqual(22.025, round(stim_time_expsyn, 4))

        # Remove variables and clear NEURON
        nc['Exp2Syn'][0].remove_immediate_from_neuron()
        nc['ExpSyn'][0].remove_immediate_from_neuron()
        nc = {}
        g1.remove_immediate_from_neuron()
        exp2syn_rec.remove_immediate_from_neuron()
        expsyn_rec.remove_immediate_from_neuron()
        sim.remove_immediate_from_neuron()

    def test_stim_syns(self):
        gs = self.cell.filter_synaptic_group()

        gs0_exp2syn_rec = Record(gs[0]['Exp2Syn'][0], variables='i')
        gs0_expsyn_rec = Record(gs[0]['ExpSyn'][0], variables='i')

        gs1_exp2syn_rec = Record(gs[1]['Exp2Syn'][0], variables='i')
        gs1_expsyn_rec = Record(gs[1]['ExpSyn'][0], variables='i')

        sim = Simulation()
        sim.run(1)

        gs[0].make_event(10)
        gs[1].make_event(20)

        sim.run(100)

        # Test stim time of synaptic group 1
        gs0_exp2syn_np = gs0_exp2syn_rec.as_numpy('i')
        stim_time_gs0_exp2syn = gs0_exp2syn_np.time[(gs0_exp2syn_np.records != 0).argmax()]

        gs0_expsyn_np = gs0_expsyn_rec.as_numpy('i')
        stim_time_gs0_expsyn = gs0_expsyn_np.time[(gs0_expsyn_np.records != 0).argmax()]

        self.assertEqual(round(stim_time_gs0_exp2syn, 1), round(stim_time_gs0_expsyn, 1))

        # Test stim time of synaptic group 2
        gs1_exp2syn_np = gs1_exp2syn_rec.as_numpy('i')
        stim_time_gs1_exp2syn = gs1_exp2syn_np.time[(gs1_exp2syn_np.records != 0).argmax()]

        gs1_expsyn_np = gs1_expsyn_rec.as_numpy('i')
        stim_time_gs1_expsyn = gs1_expsyn_np.time[(gs1_expsyn_np.records != 0).argmax()]

        self.assertEqual(round(stim_time_gs1_exp2syn, 1), round(stim_time_gs1_expsyn, 1))

        # Test values of mV in soma
        self.assertEqual(31.3285, round(gs0_exp2syn_np.records.max(), 4))
        self.assertEqual(-61.309, round(gs0_exp2syn_np.records.min(), 4))

        # Remove variables and clear NEURON
        gs0_exp2syn_rec.remove_immediate_from_neuron()
        gs0_expsyn_rec.remove_immediate_from_neuron()
        gs1_exp2syn_rec.remove_immediate_from_neuron()
        gs1_expsyn_rec.remove_immediate_from_neuron()
        gs[0].remove_immediate_from_neuron()
        gs[1].remove_immediate_from_neuron()
        sim.remove_immediate_from_neuron()
