import os
import unittest

from neuronpp.cells.cell import Cell

class TestCellAddSectionDefault(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cell = Cell(name="cell")
        cls.soma = cls.cell.add_sec("soma", add_leak=True)
        
    def test_add_soma_L_default(self):
        self.assertEqual(self.soma.hoc.L, 100.)

    def test_add_soma_diam_default(self):
        self.assertEqual(self.soma.hoc.diam, 500.)

    def test_add_soma_cm_default(self):
        self.assertEqual(self.soma.hoc.cm, 1.)
        
    def test_add_soma_ra_default(self):
        self.assertEqual(self.soma.hoc.Ra, 35.4)

    def test_add_soma_g_pas_default(self):
        self.assertEqual(self.soma.hoc.g_pas, 0.001)

    def test_add_soma_e_pas_default(self):
        self.assertEqual(self.soma.hoc.e_pas, -70.0)

if __name__ == '__main__':
    unittest.main()
# # Create cell
# cell = Cell(name="cell")
# path = os.path.dirname(os.path.abspath(__file__))
# morpho_path = os.path.join(path, "..",
#                            "commons/morphologies/asc/cell2.asc")
# cell.load_morpho(filepath=morpho_path)
# cell.insert("hh")

# # Create stim and synapses
# ns_cell = NetStimCell("stim_cell")
# ns = ns_cell.make_netstim(start=30, number=5, interval=10)

# syns = cell.add_synapses_with_spine(source=ns, secs=cell.filter_secs("apic"), mod_name="ExpSyn", netcon_weight=0.01, delay=1,
#                                     number=100)
# soma = cell.filter_secs("soma")

# # Create IClamp
# ic = IClamp(segment=soma(0.5))
# ic.stim(delay=100, dur=10, amp=0.1)

# # prepare plots and spike detector
# rec_v = Record(soma(0.5), variables="v")
# cell.make_spike_detector(soma(0.5))

# # run
# sim = RunSim(init_v=-65, warmup=20, init_sleep=2, with_neuron_gui=True, shape_plots=[make_shape_plot()])
# sim.run(runtime=200, stepsize=1, delay_between_steps=500)

# # plot
# cell.plot_spikes()
# rec_v.plot()
# plt.show()


