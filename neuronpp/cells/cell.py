from neuronpp.core.cells.core_cell import CoreCell

from neuronpp.core.decorators import non_removable_fields
from neuronpp.core.cells.synaptic_spine_cell import SynapticSpineCell


@non_removable_fields("population")
class Cell(SynapticSpineCell):
    def __init__(self, name=None, compile_paths=None, population=None,
                 override=True, wait_in_sec=2):
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
        """
        CoreCell.__init__(self, name=name, compile_paths=compile_paths,
                          override=override, wait_in_sec=wait_in_sec)
        SynapticSpineCell.__init__(self, name)
        self.population = population
