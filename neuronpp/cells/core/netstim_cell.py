from neuronpp.cells.core.cell import Cell
from neuronpp.cells.core.utils import get_netstim


class NetStimCell(Cell):
    def __init__(self, name):
        Cell.__init__(self, name)
        self.netstims = {}
        self.netstim_num = 0

    def filter_netstims(self, stim_names, as_list=False):
        """
        :param stim_names:
            List of string names as list or separated by space.
            Filter will look for obj_dict keys which contains each sec_name.
            None or 'all' will return all stims.
        :param as_list:
        :return:
        """
        return self._filter_obj_dict("netstims", names=stim_names, as_list=as_list)

    def add_netstim(self, name, start, number, interval=0, noise=0):
        """

        :param name:
        :param start:
        :param number:
        :param interval:
        :param noise:
        :return:
            Created NetStim
        """
        ns = get_netstim(start=start, number=number, interval=interval, noise=noise)
        self.netstims["%s[%s]" % (name, self.netstim_num)] = ns
        self.netstim_num += 1
        return ns
