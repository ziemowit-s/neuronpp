from neuronpp.core.cells.cell import Cell
from neuronpp.core.wrappers.hoc import Hoc
from neuronpp.core.wrappers.netconn import NetConn
from neuronpp.core.wrappers.point_process import PointProcess


class Synapse:
    def __init__(self, source, point_process: PointProcess, netconn: NetConn, parent_cell: Cell, name):
        self.parent = str(parent_cell)
        self.name = name

        self.source = source
        self.point_process = point_process
        self.netconn = netconn

    def __repr__(self):
        return "{}[{}]{}_{}".format(self.parent, self.__class__.__name__, self.netconn, self.name)
