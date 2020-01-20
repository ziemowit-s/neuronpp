import os
import time

from neuronpp.core.hocwrappers.sec import Sec

from neuronpp.utils.compile_mod import CompileMOD

from neuronpp.core.cells.hoc_cell import HocCell

from neuronpp.cells.cell import Cell


class Combe2018Cell(Cell, HocCell):
    def __init__(self, name=None, model_folder="commons/hocmodels/combe2018", spine_number=0, spine_sec="apic",
                 spine_seed: int = None, compile=True):
        """
        
        :param name:
            The name of the cell
        :param model_folder:
            The folder where the main folder of Combe et al. 2018 model is located
        :param spine_number:
            The number of spines added to the model with random_uniform distribution to the sections specified by 'spine_sec' param.
        :param spine_sec:
            The section or sections where to put spines. It can be:
              * a string - as a filter name, so you can set "apic" to add spies to all apical dendrites

              * a regex, which need to be prefixed with 'regex:' string before eg. 'regex:(apic)|(basal)'
              will return all sections wich have a name containing 'apic' or 'basal' string

              * a list of existing sections in the cell
        :param spine_seed:
            Seed value for the random_uniform spike distribution. Default is None, meaning - there is no seed
        :param compile:
            If you want to compile model's MOD files. Default is True.
        """
        Cell.__init__(self, name)
        HocCell.__init__(self, name)

        if compile:
            comp = CompileMOD()
            comp.compile(source_paths=model_folder, target_path=os.getcwd())

        main_file = "%s/load_cell.hoc" % model_folder
        self.make_hoc(main_file)

        # Add spines with AMPA and NMDA synapses
        self.combe_syns = []
        if spine_number > 0:

            heads, necks = self.make_spines(sec=spine_sec, spine_number=spine_number, head_nseg=10, neck_nseg=10, seed=spine_seed)

            self.copy_mechanisms_from_segment(secs_to_copy=heads, sec_from=self.secs[0])

            # Create AMPA synapses
            ampa_weight = 1.2 * 0.00156
            ampa_syns = self.make_sypanses(source=None, sec=heads, weight=ampa_weight, mod_name="Exp2Syn")
            for syn in ampa_syns:
                syn.point_process.hoc.e = 0
                syn.point_process.hoc.tau1 = .5
                syn.point_process.hoc.tau2 = 1.0

            # Create NMDA synapses
            nmda_weight = 1.2 * 0.000882
            nmda_syns = self.make_sypanses(source=None, sec=heads, weight=nmda_weight, mod_name="nmdanet")
            for syn in nmda_syns:
                syn.point_process.hoc.Alpha = 0.35
                syn.point_process.hoc.Beta = 0.035

            for syns in zip(ampa_syns, nmda_syns):
                comp_syn = self.group_complex_sypanses(syns, tag="combe_type")
                self.combe_syns.append(comp_syn)
