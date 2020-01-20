import os
import time

from neuronpp.utils.compile_mod import CompileMOD

from neuronpp.core.cells.hoc_cell import HocCell

from neuronpp.cells.cell import Cell


class Graham2014Cell(Cell, HocCell):
    def __init__(self, name=None, model_folder="commons/hocmodels/graham2014", compile=True):
        Cell.__init__(self, name)
        HocCell.__init__(self, name)

        if compile:
            comp = CompileMOD()
            comp.compile(source_paths=model_folder, target_path=os.getcwd())

        self.make_hoc("commons/hocmodels/graham2014/run_PC.hoc", cell_template_name="PyramidalCell")

