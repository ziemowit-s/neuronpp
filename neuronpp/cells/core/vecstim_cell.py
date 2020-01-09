from neuronpp.cells.core.cell import Cell
from neuronpp.cells.core.utils import get_vecstim


class VecStimCell(Cell):
    def __init__(self, name):
        Cell.__init__(self, name)
        self.vecstims = {}
        self.vectors = {}
        self.vecstim_num = 0

    def filter_vecstims(self, stim_names, as_list=False):
        """
        :param stim_names:
            List of string names as list or separated by space.
            Filter will look for obj_dict keys which contains each sec_name.
            None or 'all' will return all stims.
        :param as_list:
        :return:
        """
        return self._filter_obj_dict("vecstims", names=stim_names, as_list=as_list)

    def filter_vectors(self, stim_names, as_list=False):
        """
        :param stim_names:
            List of string names as list or separated by space.
            Filter will look for obj_dict keys which contains each sec_name.
            None or 'all' will return all stims.
        :param as_list:
        :return:
        """
        return self._filter_obj_dict("vectors", names=stim_names, as_list=as_list)

    def add_vecstim(self, name, ping_array):
        """

        :param name:
        :param ping_array
            numpy array when ping must start
        :return:
            Created vecstim
        """
        vs, vec = get_vecstim(ping_array)
        name = "%s[%s]" % (name, self.vecstim_num)
        self.vecstims[name] = vs
        self.vectors[name] = vec
        self.vecstim_num += 1
        return vs
