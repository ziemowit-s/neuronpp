import os

from neuronpp.cells.cell import Cell
from neuronpp.core.cells.core_hoc_cell import CoreHocCell

path = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(path, "..",
                          "commons/hocmodels/combe2018")

class Combe2018Cell(Cell, CoreHocCell):
    def __init__(self, name=None, model_folder=model_path, spine_number=0,
                 spine_secs_names="apic",
                 spine_seed: int = None):
        """
        :param name:
            The name of the cell
        :param model_folder:
            The folder where the main folder of Combe et al. 2018 model is located
        :param spine_number:
            The number of spines added to the model with random_uniform distribution to the sections specified by 'spine_sec' param.
        :param spine_secs_names:
            The section or sections where to put spines. It can be:
              * a string - as a filter name, so you can set "apic" to add spies to all apical dendrites

              * a regex, which need to be prefixed with 'regex:' string before eg. 'regex:(apic)|(basal)'
              will return all sections wich have a name containing 'apic' or 'basal' string

              * a list of existing sections in the cell
        :param spine_seed:
            Seed value for the random_uniform spike distribution. Default is None, meaning - there is no seed
        """
        Cell.__init__(self, name, model_folder)
        CoreHocCell.__init__(self, name)

        main_file = os.path.join(model_folder, "load_cell.hoc")
        self.load_hoc(main_file)

        secs = self.filter_secs(name=spine_secs_names)

        # Add spines with AMPA and NMDA synapses
        self.combe_syns = []
        if spine_number > 0:

            heads, necks = self.make_spines(secs=secs, spine_number=spine_number, head_nseg=10, neck_nseg=10, seed=spine_seed)

            # Copy mechanisms from parent sec of the neck and from the nec to the head
            self.copy_mechanisms(secs_to=necks, sec_from='parent')
            self.copy_mechanisms(secs_to=heads, sec_from='parent')

            ampa_syns = []
            nmda_syns = []

            # Create AMPA synapses
            ampa_weight = 1.2 * 0.00156
            for h in heads:
                syn = self.add_synapse(source=None, seg=h(1.0), mod_name="Exp2Syn", netcon_weight=ampa_weight)
                syn.point_process.hoc.e = 0
                syn.point_process.hoc.tau1 = .5
                syn.point_process.hoc.tau2 = 1.0
                ampa_syns.append(syn)

            # Create NMDA synapses
            nmda_weight = 1.2 * 0.000882
            for h in heads:
                syn = self.add_synapse(source=None, seg=h(1.0), mod_name="nmdanet", netcon_weight=nmda_weight)
                syn.point_process.hoc.Alpha = 0.35
                syn.point_process.hoc.Beta = 0.035
                nmda_syns.append(syn)

            for syns in zip(ampa_syns, nmda_syns):
                comp_syn = self.group_complex_synapses("combe_type", syns)
                self.combe_syns.append(comp_syn)
