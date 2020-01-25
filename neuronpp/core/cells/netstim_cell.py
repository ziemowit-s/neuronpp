from neuron import h

from neuronpp.core.cells.core_cell import CoreCell
from neuronpp.core.cells.utils import get_netstim
from neuronpp.core.hocwrappers.netstim import NetStim


class NetStimCell(CoreCell):
    def __init__(self, name=None):
        CoreCell.__init__(self, name)
        self.nss = []

    def filter_netstim(self, name: str):
        """
        :param name:
            start with 'regex:any pattern' to use regular expression. If without 'regex:' - will look which Hoc objects contain the str
        :return:
        """
        return self.filter(searchable=self.nss, name=name)

    def make_netstim(self, start, number, interval=1, noise=0):
        """
        :param start:
        :param number:
        :param interval:
        :param noise:
        :return:
            created NetStim
        """
        if h.t > 0:
            raise ConnectionRefusedError("NetStim cannot be created after simulation have been initiated. "
                                         "You need to specify NetStim before creation of SimRun object.")

        ns_hoc = get_netstim(start=start, number=number, interval=interval, noise=noise)
        name = str(len(self.nss))

        ns = NetStim(ns_hoc, parent=self, name=name)
        self.nss.append(ns)
        return ns
