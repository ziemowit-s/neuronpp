import numpy as np
import seaborn as sb
from neuron import h
import matplotlib.pyplot as plt


class HeatmapGraph:
    def __init__(self, name, elements, extract_func=lambda x: x, shape=None):
        """

        :param name:
        :param elements:
            list or np.array
        :param shape:
            if None:
                for list - assume it's 1D vector
                for np.array - take its shape
        """
        self.name = name
        # last time of NEURON simulation; maybe helpful but it's just a hack
        # if you want to use this class outside the NEURON context - just ignore self.last_sim_time
        self.last_sim_time = 0

        self.shape = None
        self.elements = None
        self.update(elements, shape=shape)

        self.extract_func = extract_func
        self.fig, self.ax = plt.subplots()
        self.ax.set_title(self.name)
        self.fig.canvas.draw()
        self.fig.show()

    def plot(self, vmin=None, vmax=None, update_elements=None):
        """
        :param vmin:
            min value on the colormap. None means that it will assume min based on the data provided.
        :param vmax:
            default max value on the colormap. None means that it will assume min based on the data provided.
        :param update_elements:
            if you want to update elements collection
        :return:
        """
        self.update(elements=update_elements)
        data = []
        for i, e in enumerate(self.elements):
            data.append(self.extract_func(e))

        annots = np.round(np.array(data).reshape(self.shape), 4)
        data = np.array(data).reshape(self.shape)

        self.ax.texts = []
        sb.heatmap(data, annot=annots, fmt='', cmap=plt.cm.Blues, vmin=vmin, vmax=vmax,
                   xticklabels=False, yticklabels=False, cbar=False, ax=self.ax)
        self.fig.canvas.blit(self.ax.bbox)
        self.fig.canvas.flush_events()

        # last time of NEURON simulation; maybe helpful but it's just a hack
        # if you want to use this class outside the NEURON context - just ignore self.last_sim_time
        self.last_sim_time = h.t
        plt.pause(1e-3)

    def update(self, elements, shape=None):
        """
        if you want to update elements collection as a new collection
        :param elements:
            elements to update. Shape must be the same af initial elements
        :param shape:
            if None:
                for list - assume it's 1D vector
                for np.array - take its shape
        :return:
        """
        if shape is None and self.shape is None:
            if isinstance(elements, np.ndarray):
                shape = elements.shape
            elif isinstance(elements, list):
                shape = [len(elements), 1]
            else:
                raise TypeError("Allowed types are list or numpy.array.")

            if len(shape) == 1:
                shape = [shape, 1]
            if len(shape) > 2 or len(shape) == 0:
                raise LookupError("Param shape must be a tuple of size 1 or 2.")
            self.shape = shape
        self.elements = elements

    def _get_zero_size(self):
        size = self.shape if len(self.shape) == 1 else self.shape[0] * self.shape[1]
        return np.zeros(size)
