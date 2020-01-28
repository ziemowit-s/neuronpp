from collections import defaultdict

import numpy as np
from neuron import h
import pandas as pd
from math import ceil
import matplotlib.pyplot as plt


class Record:
    def __init__(self, elements, variables='v', loc=None):
        """
        :param elements:
            elements can any object from HocWrappers which implements hoc param
        :param loc:
            float (if loc for all sections is the same), or list of floats (in that case len must be the same as len(sections).
            Default None. If None - loc will be skipped (eg. for point process)
        :param variables:
            str or list_of_str of variable names to track
        """
        if not isinstance(elements, (list, set, tuple)):
            elements = [elements]

        if isinstance(variables, str):
            variables = variables.split(' ')

        if isinstance(loc, float) or isinstance(loc, int) or loc is None:
            loc = [loc for _ in range(len(elements))]

        if len(loc) != len(elements):
            raise IndexError("loc can be single float (eg. 0.5) or a list where len(loc) must be the same as len(sections).")

        self.recs = dict([(v, []) for v in variables])
        self.figs = {}
        self.axs = defaultdict(list)

        for sec, loc in zip(elements, loc):
            for var in variables:
                s = sec.hoc if loc is None else sec.hoc(loc)
                try:
                    s = getattr(s, "_ref_%s" % var)
                except AttributeError:
                    raise AttributeError("there is no attribute of %s. Maybe you forgot to append loc param for sections?" % var)

                rec = h.Vector().record(s)
                name = "%s(%s)" % (sec.name, loc)
                self.recs[var].append((name, rec))

        self.t = h.Vector().record(h._ref_t)

    def plot(self, animate=False, **kwargs):
        if animate:
            self.plot_animate(**kwargs)
        else:
            self.plot_static()

    def plot_static(self):
        for var_name, section_recs in self.recs.items():
            fig, axs = plt.subplots(len(section_recs))
            axs = axs.flat if isinstance(axs, np.ndarray) else [axs]

            for ax, (name, rec) in zip(axs, section_recs):
                ax.set_title("%s.%s" % (name, var_name))
                ax.plot(self.t, rec)
                ax.set(xlabel='t (ms)', ylabel=var_name)

    def plot_animate(self, steps=10000, y_lim=None, position=None):
        """
        Call each time you want to redraw plot.

        :param steps:
            how many timesteps to see on the graph
        :param y_lim:
            tuple of limits for y axis. Default is (-80, 50)
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
                fig = plt.figure()
                fig.canvas.draw()
                self.figs[var_name] = fig

            for i, (name, rec) in enumerate(section_recs):
                if create_fig:
                    if position is None:
                        ax = fig.add_subplot(len(section_recs), 1, i + 1)
                    elif position == 'merge':
                        ax = fig.add_subplot(1, 1, 1)
                    else:
                        size = position[0] * position[1]
                        if position[0] * position[1] < len(section_recs):
                            raise IndexError("Provided position %s declared %s graphs on the figure, "
                                             "however you have %s records on the variable '%s'." %
                                             (position, size, len(section_recs), var_name))
                        ax = fig.add_subplot(position[0], position[1], i + 1)

                    if y_lim:
                        ax.set_ylim(y_lim[0], y_lim[1])
                    line, = ax.plot([], lw=1)
                    ax.set_title(name)
                    ax.set_ylabel(var_name)
                    ax.set_xlabel("t (ms)")
                    self.axs[var_name].append((ax, line))

                ax, line = self.axs[var_name][i]
                t = self.t.as_numpy()[-steps:]
                r = rec.as_numpy()[-steps:]

                ax.set_xlim(t.min(), t.max())
                if y_lim is None:
                    ax.set_ylim(r.min()-(np.abs(r.min()*0.05)), r.max()+(np.abs(r.max()*0.05)))

                # update data
                line.set_data(t, r)

            fig.canvas.draw()
            fig.canvas.flush_events()

        if create_fig:
            plt.show(block=False)

    def to_csv(self, filename):
        cols = ['time']
        data = [self.t.as_numpy().tolist()]

        for var_name, rec_data in self.recs.items():
            for sec_name, vec in rec_data:
                cols.append(sec_name)
                data.append(vec.as_numpy().tolist())

        df = pd.DataFrame(list(zip(*data)), columns=cols)
        df.to_csv(filename, index=False)
