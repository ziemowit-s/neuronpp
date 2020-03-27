import numpy as np
import seaborn as sb
from neuron import h
from typing import List
import matplotlib.pyplot as plt

from neuronpp.core.cells.netcon_cell import NetConCell


class SpikesHeatmapGraph:
    def __init__(self, name, cells: List[NetConCell], shape=None, sec="soma", loc=0.5):
        self.name = name
        if shape is None:
            shape = [len(cells), 1]
        if len(shape) == 1:
            shape = [shape, 1]
        if len(shape) > 2 or len(shape) == 0:
            raise LookupError("Param shape must be a tuple of size 1 or 2.")

        self.shape = shape
        self.cells = cells

        self.last_t = 0

        print("Heatmap %s - number -> cell_name mapping:" % self.name)
        for i, c in enumerate(self.cells):
            print("%s:" % i, c.name)
            if c._spike_detector is None:
                c.make_spike_detector(c.filter_secs(sec)(loc))

        self.fig, self.ax = plt.subplots()
        self.ax.set_title(self.name)
        self.fig.canvas.draw()
        self.fig.show()

    def plot(self):
        data = []
        for i, c in enumerate(self.cells):
            spikes = [ms for ms in c.get_spikes() if ms > self.last_t]
            data.append(len(spikes))

        nums = [i for i in range(len(data))]
        nums = np.array(nums).reshape(self.shape)
        data = np.array(data).reshape(self.shape)

        sb.heatmap(data, annot=nums, fmt='', cmap=plt.cm.Blues, xticklabels=False, yticklabels=False, cbar=False, ax=self.ax)
        self.fig.canvas.blit(self.ax.bbox)
        self.fig.canvas.flush_events()

        self.last_t = h.t
        plt.pause(1e-9)

    def _get_zero_size(self):
        size = self.shape if len(self.shape) == 1 else self.shape[0] * self.shape[1]
        return np.zeros(size)
