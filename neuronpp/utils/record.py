from math import ceil

import numpy as np

from neuron import h
import matplotlib.pyplot as plt


class Record:
    def __init__(self, sections, variables, locs=None):
        """

        :param sections:
        :param locs:
            float (if loc for all sections is the same), or list of floats (in that case len must be the same as len(sections).
            Default None. If None - loc will be skipped (eg. for point process)
        :param variables:
            str or list_of_str of variable names to track
        """
        if not isinstance(sections, (list, set, tuple)):
            sections = [sections]

        if isinstance(variables, str):
            variables = variables.split(' ')

        if isinstance(locs, float) or isinstance(locs, int) or locs is None:
            locs = [locs for _ in range(len(sections))]

        if len(locs) != len(sections):
            raise IndexError("locs can be single float (eg. 0.5) or a list where len(locs) must be the same as len(sections).")

        self.recs = dict([(v, []) for v in variables])

        for sec, loc in zip(sections, locs):
            for var in variables:
                s = sec.hoc if loc is None else sec.hoc(loc)
                try:
                    s = getattr(s, "_ref_%s" % var)
                except AttributeError:
                    raise AttributeError("there is no attribute of %s. Maybe you forgot to append locs param for sections?" % var)

                rec = h.Vector().record(s)
                self.recs[var].append(("%s(%s)" % (sec.name, loc), rec))

        self.t = h.Vector().record(h._ref_t)

    def plot(self, max_plot_on_fig=4):
        for var_name, recs in self.recs.items():
            ceil_len = ceil(len(recs)/max_plot_on_fig)

            for i in range(ceil_len):
                current_recs = recs[i:i+max_plot_on_fig]

                fig, axs = plt.subplots(len(current_recs))
                axs = axs.flat if isinstance(axs, np.ndarray) else [axs]

                for ax, (name, rec) in zip(axs, current_recs):
                    ax.set_title("%s.%s" % (name, var_name))
                    ax.plot(self.t, rec)
                    ax.set(xlabel='t (ms)', ylabel=var_name)
