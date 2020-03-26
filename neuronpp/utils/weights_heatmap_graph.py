from typing import List

import numpy as np
import seaborn as sb
from neuron import h
import matplotlib.pyplot as plt
from neuronpp.core.hocwrappers.composed.synapse import Synapse


class WeightsHeatmapGraph:
    def __init__(self, name, syns: List[Synapse], shape=None):
        self.name = name
        if shape is None:
            shape = [len(syns), 1]
        if len(shape) == 1:
            shape = [shape, 1]
        if len(shape) > 2 or len(shape) == 0:
            raise LookupError("Param shape must be a tuple of size 1 or 2.")

        self.shape = shape
        self.syns = syns

        self.last_t = 0

        self.fig, self.ax = plt.subplots()
        self.ax.set_title(self.name)
        self.fig.canvas.draw()
        self.fig.show()

    def plot(self):
        data = []
        for i, s in enumerate(self.syns):
            data.append(s.hoc.w)

        data = np.array(data).reshape(self.shape)

        sb.heatmap(data, fmt='', cmap=plt.cm.Blues, xticklabels=False, yticklabels=False, cbar=False, ax=self.ax)
        self.fig.canvas.blit(self.ax.bbox)
        self.fig.canvas.flush_events()

        self.last_t = h.t
        plt.pause(1e-9)

    def _get_zero_size(self):
        size = self.shape if len(self.shape) == 1 else self.shape[0] * self.shape[1]
        return np.zeros(size)
