import os

from neuronpp.utils.compile_mod import CompileMOD

from neuronpp.core.cells.core_hoc_cell import CoreHocCell

from neuronpp.cells.cell import Cell


class Graham2014Cell(Cell, CoreHocCell):
    def __init__(self, name=None, model_folder="../commons/hocmodels/graham2014"):
        Cell.__init__(self, name, model_folder)
        CoreHocCell.__init__(self, name)

        if compile:
            comp = CompileMOD()
            comp.compile(source_paths=model_folder, target_path=os.getcwd())

        main_file = "%s/run_PC.hoc" % model_folder
        self.load_hoc(main_file, cell_template_name="PyramidalCell")

