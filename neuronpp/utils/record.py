from collections import defaultdict

import numpy as np
from neuron import h
import pandas as pd
from math import ceil
import matplotlib.pyplot as plt


class Record:
    def __init__(self, elements, variables, locs=None):
        """

        :param elements:
            elements can any object from HocWrappers which implements hoc param
        :param locs:
            float (if loc for all sections is the same), or list of floats (in that case len must be the same as len(sections).
            Default None. If None - loc will be skipped (eg. for point process)
        :param variables:
            str or list_of_str of variable names to track
        """
        if not isinstance(elements, (list, set, tuple)):
            elements = [elements]

        if isinstance(variables, str):
            variables = variables.split(' ')

        if isinstance(locs, float) or isinstance(locs, int) or locs is None:
            locs = [locs for _ in range(len(elements))]

        if len(locs) != len(elements):
            raise IndexError("locs can be single float (eg. 0.5) or a list where len(locs) must be the same as len(sections).")

        self.recs = dict([(v, []) for v in variables])
        self.figs = {}
        self.axs = defaultdict(list)

        for sec, loc in zip(elements, locs):
            for var in variables:
                s = sec.hoc if loc is None else sec.hoc(loc)
                try:
                    s = getattr(s, "_ref_%s" % var)
                except AttributeError:
                    raise AttributeError("there is no attribute of %s. Maybe you forgot to append locs param for sections?" % var)

                rec = h.Vector().record(s)
                name = "%s(%s)" % (sec.name, loc)
                self.recs[var].append((name, rec))

        self.t = h.Vector().record(h._ref_t)

    def plot(self):
        for var_name, section_recs in self.recs.items():
            if var_name not in self.figs:
                self.figs[var_name] = None

            fig = self.figs[var_name]
            create_fig = False
            if fig is None:
                create_fig = True
                fig = plt.figure()
                fig.canvas.draw()
                self.figs[var_name] = fig

            for i, (name, rec) in enumerate(section_recs):
                if create_fig:
                    ax = fig.add_subplot(len(section_recs), 1, 1)
                    line, = ax.plot([], lw=3)
                    self.axs[var_name].append((ax, line))

                ax, line = self.axs[var_name][i]
                fig = self.figs[var_name]

                # update data
                line.set_data(self.t, rec)

                fig.canvas.draw()
                fig.canvas.flush_events()

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
