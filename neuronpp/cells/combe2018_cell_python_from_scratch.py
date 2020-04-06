import os

from neuronpp.cells.cell import Cell

path = os.path.dirname(os.path.abspath(__file__))
f_path = os.path.join(path, "..", "commons/mods/combe2018")

class Combe2018Cell(Cell, SpineCell):
    def __init__(self, name=None, compile_paths=f_path):
        """
        :param name:
            The name of the cell
        :param compile_paths:
            Folder with channels
        """
        Cell.__init__(self, name=name, compile_paths=compile_paths)
        
