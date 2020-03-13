from math import ceil

import numpy as np
from neuron import h
from typing import List
import matplotlib.pyplot as plt

from neuronpp.core.cells.netcon_cell import NetConCell


class HitmapGraph:
    def __init__(self, cells: List[NetConCell], shape, sec="soma", loc=0.5):
        self.cells = cells
        self.shape = shape
        self.last_t = 0

        for c in self.cells:
            if c._spike_detector is None:
                c.make_spike_detector(c.filter_secs(sec)(loc))

        self.fig, self.ax = plt.subplots()
        self.fig.canvas.draw()
        self.fig.show()

    def plot(self):
        xs = []
        ys = []
        data = self._get_zero_size()
        for i, c in enumerate(self.cells):
            spikes = [ms for ms in c.get_spikes() if ms > self.last_t]
            data[i] = len(spikes)

        data = data.reshape(self.shape).T
        heatmap = self.ax.pcolor(data, cmap=plt.cm.Blues)

        self.ax.draw_artist(self.ax.patch)
        self.ax.draw_artist(heatmap)
        self.fig.canvas.blit(self.ax.bbox)
        self.fig.canvas.flush_events()

        self.last_t = h.t
        plt.pause(1e-9)

    def _get_zero_size(self):
        size = self.shape if len(self.shape) == 1 else self.shape[0] * self.shape[1]
        return np.zeros(size)
