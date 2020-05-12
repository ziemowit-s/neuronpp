from neuronpp.cells.cell import Cell
from neuronpp.core.template import Template


class TemplateCell(Template, Cell):
    def __init__(self, name=None, compile_paths=None):
        """
        Class used to create Cell template object which maybe used to create cells in Population.
        :param name:
            Name of the cell
        :param compile_paths:
            paths to folders containing mods. Can be list or string separated by spaces.
        """
        Template.__init__(self, name=name, compile_paths=compile_paths)
        Cell.__init__(self, name=name, compile_paths=compile_paths)
