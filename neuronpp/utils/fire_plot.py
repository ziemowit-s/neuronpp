from math import ceil

import numpy as np
from typing import List
import matplotlib.pyplot as plt

from neuronpp.core.cells.netcon_cell import NetConCell


class FirePlot:
    def __init__(self, cells: List[NetConCell], cols_num, sec="soma", loc=0.5):
        self.cells = cells
        self.cols_num = cols_num
        self.row_num = ceil(len(self.cells)/cols_num)

        for c in self.cells:
            if c._spike_detector is None:
                c.make_spike_detector(c.filter_secs(sec)(loc))

        self.fig, self.ax = plt.subplots()
        self.scatter = self.ax.scatter([], [])

        plt.xlim(-1, self.cols_num)
        plt.ylim(-1, self.row_num)
        plt.draw()

    def plot(self):
        xs = []
        ys = []

        row = -1
        for i, c in enumerate(self.cells):
            x = i % self.cols_num
            if x == 0:
                row += 1
            y = row
            if len(c.get_spikes()) > 0:
                xs.append(x)
                ys.append(y)

        self.scatter.set_offsets(np.c_[xs, ys])
        self.fig.canvas.draw_idle()

        plt.pause(1e-9)
