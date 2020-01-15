from neuronpp.cells.core.cell import Cell
from neuronpp.cells.core.utils import get_netstim
from neuronpp.hocs.netstim import NetStim


class NetStimCell(Cell):
    def __init__(self, name):
        Cell.__init__(self, name)
        self.nss = []

    def filter_netstim(self, name_filter:str, regex=False):
        """
        :param name_filters:
            Filter will look for obj_dict keys which contains each name_filter.
        :param regex:
            If True: pattern will be treated as regex expression, if False: pattern str must be in field str
        :return:
        """
        return self.filter(searchable=self.nss, name=name_filter, regex=regex)

    def add_netstim(self, name, start, number, interval=1, noise=0):
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
