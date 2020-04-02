from collections import defaultdict

import numpy as np
import pandas as pd
from neuron import h
import matplotlib.pyplot as plt

from neuronpp.core.hocwrappers.sec import Sec
from neuronpp.core.hocwrappers.seg import Seg
from neuronpp.core.hocwrappers.point_process import PointProcess


class Record:
    def __init__(self, elements, variables='v'):
        """
        :param elements:
            elements can any object from HocWrappers which implements hoc param
        :param variables:
            str or list_of_str of variable names to track
        """
        if h.t > 0:
            raise ConnectionRefusedError("Record cannot be created after simulation have been initiated. "
                                         "You need to specify Record before creation of SimRun object.")
        if not isinstance(elements, (list, set, tuple)):
            elements = [elements]

        if isinstance(variables, str):
            variables = variables.split(' ')

        if len(elements) == 0:
            raise IndexError("The list of provided elements to record is empty.")

        self.recs = dict([(v, []) for v in variables])
        self.figs = {}
        self.axs = defaultdict(list)

        for elem in elements:
            for var in variables:
                if isinstance(elem, Seg):
                    cell_name = elem.parent.parent.name
                    name = "%s_%s" % (cell_name, elem.name)
                elif isinstance(elem, PointProcess):
                    cell_name = elem.cell.name
                    name = "%s_%s" % (cell_name, elem.name)
                elif isinstance(elem, Sec):
                    raise TypeError("Record element cannot be of type Sec, however you can specify Seg eg. soma(0.5) and pass as element.")
                else:
                    name = elem.name

                try:
                    s = getattr(elem.hoc, "_ref_%s" % var)
                except AttributeError:
                    raise AttributeError("there is no attribute of %s. Maybe you forgot to append loc param for sections?" % var)

                rec = h.Vector().record(s)
                self.recs[var].append((name, rec))

        self.time = h.Vector().record(h._ref_t)

    def plot(self, animate=False, **kwargs):
        """
        :param animate:
            if true, it will redraw the plot on the same figure each time this function is called
        :param steps:
            [used only if animate=True] how many timesteps to see on the graph
        :param y_lim:
            [used only if animate=True] tuple of limits for y axis. Default is (-80, 50)
        :param position:
            position of all subplots ON EACH figure (each figure is created for each variable separately).
            * position=(3,3) -> if you have 9 neurons and want to display 'v' on 3x3 matrix
            * position='merge' -> it will display all figures on the same graph.
            * position=None -> Default, each neuron has separated  axis (row) on the figure.
        :return:
        """
        if animate:
            self._plot_animate(**kwargs)
        else:
            self._plot_static(**kwargs)

    def _plot_static(self, position=None):
        """
        :param position:
            position of all subplots ON EACH figure (each figure is created for each variable separately).
            * position=(3,3) -> if you have 9 neurons and want to display 'v' on 3x3 matrix
            * position='merge' -> it will display all figures on the same graph.
            * position=None -> Default, each neuron has separated  axis (row) on the figure.
        :return:
        """
        for i, (var_name, section_recs) in enumerate(self.recs.items()):
            fig = plt.figure()

            if position is "merge":
                ax = fig.add_subplot(1, 1, 1)

            for i, (name, rec) in enumerate(section_recs):
                rec_np = rec.as_numpy()
                if np.max(np.isnan(rec_np)):
                    raise ValueError("Vector recorded for variable: '%s' and segment: '%s' contains nan values." % (var_name, name))

                if position is not "merge":
                    ax = self._get_subplot(fig=fig, var_name=var_name, position=position, row_len=len(section_recs), index=i + 1)
                ax.set_title("Variable: %s" % var_name)
                ax.plot(self.time, rec, label=name)
                ax.set(xlabel='t (ms)', ylabel=var_name)
                ax.legend()

    def _plot_animate(self, steps=10000, y_lim=None, position=None):
        """
        Call each time you want to redraw plot.

        :param steps:
            how many timesteps to see on the graph
        :param y_lim:
            tuple of limits for y axis. Default is None
        :param position:
            position of all subplots ON EACH figure (each figure is created for each variable separately).
            * position=(3,3) -> if you have 9 neurons and want to display 'v' on 3x3 matrix
            * position='merge' -> it will display all figures on the same graph.
            * position=None -> Default, each neuron has separated  axis (row) on the figure.
        :return:
        """
        create_fig = False
        for var_name, section_recs in self.recs.items():
            if var_name not in self.figs:
                self.figs[var_name] = None

            fig = self.figs[var_name]
            if fig is None:
                create_fig = True
                fig = plt.figure(figsize=(16.5, 5.5))
                fig.canvas.draw()
                self.figs[var_name] = fig

            records = np.array([rec.as_numpy()[-steps:] for name, rec in section_recs])
            names = [name for name, rec in section_recs]
            if position == "merge" and y_lim is None:
                y_lim = records.min(), records.max()
            current_time = self.time.as_numpy()[-steps:]

            for i, name in enumerate(names):
                rec = records[i]
                if create_fig:
                    if position == 'merge':
                        ax = fig.add_subplot(1, 1, 1)
                    else:
                        ax = self._get_subplot(fig=fig, var_name=var_name, position=position, row_len=len(section_recs), index=i + 1)

                    if y_lim:
                        ax.set_ylim(y_lim[0], y_lim[1])
                    line, = ax.plot([], lw=1, label=name)
                    ax.set_ylabel(var_name)
                    ax.set_xlabel("time (ms)")
                    ax.legend()

                    self.axs[var_name].append((ax, line))

                ax, line = self.axs[var_name][i]
                ax.set_xlim(current_time.min(), current_time.max())

                if y_lim is None and position != "merge":
                    ax.set_ylim(rec.min()-(np.abs(rec.min()*0.05)), rec.max()+(np.abs(rec.max()*0.05)))

                # update data
                line.set_data(current_time, rec)

            fig.subplots_adjust(left=0.09, bottom=0.075, right=0.99, top=0.98, wspace=None, hspace=0.00)
            fig.canvas.draw()
            fig.canvas.flush_events()

        if create_fig:
            plt.show(block=False)

    def to_csv(self, filename):
        cols = ['time']
        data = [self.time.as_numpy().tolist()]

        for var_name, rec_data in self.recs.items():
            for sec_name, vec in rec_data:
                cols.append(sec_name)
                data.append(vec.as_numpy().tolist())

        df = pd.DataFrame(list(zip(*data)), columns=cols)
        df.to_csv(filename, index=False)

    @staticmethod
    def _get_subplot(fig, var_name, position, row_len=1, index=1):
        if position is None:
            ax = fig.add_subplot(row_len, 1, index)
        elif position == 'grid':
            n = np.sqrt(row_len)
            if n % int(n) != 0:
                n += 1
            ax = fig.add_subplot(n, n, index)
        else:
            size = position[0] * position[1]
            if position[0] * position[1] < row_len:
                raise IndexError("Provided position %s declared %s graphs on the figure, "
                                 "however you have %s records on the variable '%s'." %
                                 (position, size, row_len, var_name))
            ax = fig.add_subplot(position[0], position[1], index)

        return ax
