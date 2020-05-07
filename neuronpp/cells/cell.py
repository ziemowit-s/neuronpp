from neuronpp.core.cells.core_cell import CoreCell

from neuronpp.core.cells.synaptic_spine_cell import SynapticSpineCell


class Cell(SynapticSpineCell):
    def __init__(self, name=None, compile_paths=None, build_on_the_fly=True):
        """
        :param name:
            Name of the cell
        :param compile_paths:
            paths to folders containing mods. Can be list or string separated by spaces.
        """
        CoreCell.__init__(self, name=name, compile_paths=compile_paths,
                          build_on_the_fly=build_on_the_fly)
        SynapticSpineCell.__init__(self, name)
