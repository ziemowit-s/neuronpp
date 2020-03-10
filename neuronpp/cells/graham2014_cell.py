import os

from neuronpp.core.cells.core_hoc_cell import CoreHocCell

from neuronpp.cells.cell import Cell

path =  os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(path, "..",
                          "commons/hocmodels/graham2014")

class Graham2014Cell(Cell, CoreHocCell):
    def __init__(self, name=None, model_folder=model_path):
        Cell.__init__(self, name, model_folder)
        CoreHocCell.__init__(self, name)

        main_file = os.path.join(model_folder, "run_PC.hoc")
        self.load_hoc(main_file, cell_template_name="PyramidalCell")

