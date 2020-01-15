from neuronpp.cells.core.cell import Cell
from neuronpp.cells.core.utils import get_netstim
from neuronpp.hocs.netstim import NetStim


class NetStimCell(Cell):
    def __init__(self, name):
        Cell.__init__(self, name)
        self.nss = []

    def filter_netstim(self, name:str):
        """
        :param name:
            start with 'regex:any pattern' to use regular expression. If without 'regex:' - will look which Hoc objects contain the str
        :return:
        """
        return self.filter(searchable=self.nss, name=name)

    def add_netstim(self, name:str, start, number, interval=1, noise=0):
        """
        :param name:
        :param start:
        :param number:
        :param interval:
        :param noise:
        :return:
            Created NetStim
        """
        ns_hoc = get_netstim(start=start, number=number, interval=interval, noise=noise)
        name = "%s[%s]" % (name, len(self.nss))

        ns = NetStim(ns_hoc, parent=self, name=name)
        self.nss.append(ns)
        return ns
