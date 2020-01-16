from neuronpp.core.cells.synaptic_spine_cell import SynapticSpineCell


class Cell(SynapticSpineCell):
    def __init__(self, name=None):
        SynapticSpineCell.__init__(self, name)
