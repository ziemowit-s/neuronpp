from neuronpp.cells.cell import Cell

from neuronpp.core.cells.core_cell import CoreCell
from neuronpp.core.cells.core_hoc_cell import CoreHocCell


class HocCell(CoreHocCell, Cell):
    def __init__(self, name=None, compile_paths=None):
        """
        :param name:
            Name of the cell
        :param compile_paths:
            paths to folders containing mods. Can be list or string separated by spaces.
        """
        CoreCell.__init__(self, name=name, compile_paths=compile_paths)
        Cell.__init__(self, name)
        CoreHocCell.__init__(self, name)
