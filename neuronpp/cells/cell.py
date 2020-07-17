from neuronpp.core.cells.core_cell import CoreCell

from neuronpp.core.decorators import non_removable_fields
from neuronpp.core.cells.synaptic_spine_cell import SynapticSpineCell


@non_removable_fields("population")
class Cell(SynapticSpineCell):
    def __init__(self, name=None, compile_paths=None, population=None):
        """
        :param name:
            Name of the cell
        :param compile_paths:
            paths to folders containing mods. Can be list or string separated by spaces.
        :param population:
            reference to the population (if the cell is a part of such). Default is None
        """
        CoreCell.__init__(self, name=name, compile_paths=compile_paths)
        SynapticSpineCell.__init__(self, name)
        self.population = population
