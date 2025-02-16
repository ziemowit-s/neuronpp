from neuronpp.core.cells.core_cell import CoreCell

from neuronpp.core.decorators import non_removable_fields
from neuronpp.core.cells.synaptic_spine_cell import SynapticSpineCell


@non_removable_fields("population")
class Cell(SynapticSpineCell):
    def __init__(self, name=None, compile_paths=None, population=None,
                 override=True, wait_in_sec=2, compile_mods_with_random_subfolder=True):
        """
        :param name:
            Name of the cell
        :param compile_paths:
            paths to folders containing mods. Can be list or string separated by spaces.
        :param population:
            reference to the population (if the cell is a part of such). Default is None
        :param override:
           If True, the function will override existing compiled MOD files in the target folder.
           If False and the target path exists, the function will skip the compilation step.
           Default is True.
        :param wait_in_sec:
           The number of seconds to wait between retries if loading the mechanisms fails.
           Default is 2 seconds.
        :param compile_mods_with_random_subfolder:
            if True it will create a random subfolder in the target folder as compiled/random_string/modsNUM.
            if False it will create folder compiled/modsNUM
        """
        CoreCell.__init__(self, name=name, compile_paths=compile_paths,
                          override=override, wait_in_sec=wait_in_sec, compile_mods_with_random_subfolder=compile_mods_with_random_subfolder)
        SynapticSpineCell.__init__(self, name)
        self.population = population
