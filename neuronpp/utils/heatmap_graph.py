import numpy as np
import seaborn as sb
from neuron import h
from typing import List
import matplotlib.pyplot as plt

from neuronpp.core.cells.netcon_cell import NetConCell


class HeatmapGraph:
    def __init__(self, cells: List[NetConCell], shape=None, sec="soma", loc=0.5):
        if shape is None:
            shape = [len(cells), 1]
        if len(shape) == 1:
            shape = [shape, 1]
        if len(shape) > 2 or len(shape) == 0:
            raise LookupError("Param shape must be a tuple of size 1 or 2.")

        self.shape = shape
        self.cells = cells

        self.last_t = 0

        for c in self.cells:
            if c._spike_detector is None:
                c.make_spike_detector(c.filter_secs(sec)(loc))

        self.fig, self.ax = plt.subplots()
        self.fig.canvas.draw()
        self.fig.show()

    def plot(self, with_names=False):
        names = []
        data = self._get_zero_size()
        for i, c in enumerate(self.cells):
            if with_names:
                try:
                    cell_num = c.name.split("[")[-1].replace(']', '')
                    names.append(cell_num)
                except Exception:
                    raise ValueError("Currently hitmap names assume that each cell ends with: '[NUM]' which is a unique number of the cell "
                                     "within cells you are plotting on the heatmap, but provided cell name was: %s" % c.name)
            spikes = [ms for ms in c.get_spikes() if ms > self.last_t]
            data[i] = len(spikes)

        data = data.reshape(self.shape).T

        if with_names:
            names = np.array(names).reshape(self.shape).T
        else:
            names = None

        sb.heatmap(data, annot=names, fmt='', cmap=plt.cm.Blues, xticklabels=False, yticklabels=False, cbar=False, ax=self.ax)
        self.fig.canvas.blit(self.ax.bbox)
        self.fig.canvas.flush_events()

        self.last_t = h.t
        plt.pause(1e-9)

    def _get_zero_size(self):
        size = self.shape if len(self.shape) == 1 else self.shape[0] * self.shape[1]
        return np.zeros(size)
