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

    def plot(self, max_plot_on_fig=4):
        for var_name, section_recs in self.recs.items():
            ceil_len = ceil(len(section_recs)/max_plot_on_fig)

            for i in range(ceil_len):
                current_recs = section_recs[i:i+max_plot_on_fig]

                fig, axs = plt.subplots(len(current_recs))
                axs = axs.flat if isinstance(axs, np.ndarray) else [axs]

                for ax, (name, rec) in zip(axs, current_recs):
                    ax.set_title("%s.%s" % (name, var_name))
                    ax.plot(self.t, rec)
                    ax.set(xlabel='t (ms)', ylabel=var_name)

    def to_csv(self, filename):
        cols = ['time']
        data = [self.t.as_numpy().tolist()]

        for var_name, rec_data in self.recs.items():
            for sec_name, vec in rec_data:
                cols.append(sec_name)
                data.append(vec.as_numpy().tolist())

        df = pd.DataFrame(list(zip(*data)), columns=cols)
        df.to_csv(filename, index=False)
