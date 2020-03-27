from typing import List

import numpy as np
import seaborn as sb
from neuron import h
import matplotlib.pyplot as plt
from neuronpp.core.hocwrappers.composed.synapse import Synapse


class HeatmapGraph:
    def __init__(self, name, elements: list, extract_func=lambda x: x, shape=None):
        """

        :param name:
        :param elements:
        :param shape:
        """
        self.name = name
        self.last_sim_time = 0

        if shape is None:
            shape = [len(elements), 1]
        if len(shape) == 1:
            shape = [shape, 1]
        if len(shape) > 2 or len(shape) == 0:
            raise LookupError("Param shape must be a tuple of size 1 or 2.")

        self.shape = shape
        self.elements = elements
        self.extract_func = extract_func

        self.fig, self.ax = plt.subplots()
        self.ax.set_title(self.name)
        self.fig.canvas.draw()
        self.fig.show()

    def plot(self, vmin=None, vmax=None):
        """
        :param vmin:
            min value on the colormap. None means that it will assume min based on the data provided.
        :param vmax:
            default max value on the colormap. None means that it will assume min based on the data provided.
        :return:
        """
        data = []
        for i, e in enumerate(self.elements):
            data.append(self.extract_func(e))

        annots = np.array([round(d, 4) for d in data]).reshape(self.shape)
        data = np.array(data).reshape(self.shape)

        self.ax.texts = []
        sb.heatmap(data, annot=annots, fmt='', cmap=plt.cm.Blues, vmin=vmin, vmax=vmax,
                   xticklabels=False, yticklabels=False, cbar=False, ax=self.ax)
        self.fig.canvas.blit(self.ax.bbox)
        self.fig.canvas.flush_events()

        self.last_sim_time = h.t
        plt.pause(1e-9)

    def _get_zero_size(self):
        size = self.shape if len(self.shape) == 1 else self.shape[0] * self.shape[1]
        return np.zeros(size)
