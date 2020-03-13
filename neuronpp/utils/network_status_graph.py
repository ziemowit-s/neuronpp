# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 17:39:28 2020

@author: Wladek
"""
import re
import math
import numpy as np
import matplotlib.pyplot as py

from neuronpp.core.hocwrappers.seg import Seg
from neuronpp.core.hocwrappers.point_process import PointProcess


class NetworkStatusGraph:
    def __init__(self, cells, weight_name='w', plot_fixed_weight_edges=True):
        self.cells = cells
        self.colors = []
        self.texts = []
        self.lines = []
        self.x_list = []
        self.y_list = []
        self.nodes = []
        self.plot_constant_connections = plot_fixed_weight_edges

        self.correct_position = (0.1, 0.1)

        self.population_names = self._get_population_names()
        self.edges = self._get_edges(weight_name)

    def plot(self):
        py.figure()
        ax2 = py.subplot(111)
        self.nodes = []
        for cell_num, edge in enumerate(self.edges):
            self.nodes.append(ax2.scatter(self.x_list[cell_num],
                                          self.y_list[cell_num], s=300,
                                          color=self.colors[cell_num], alpha=0.5))
            for target in edge:
                line, = ax2.plot(target[0], target[1], lw=target[2], color='grey')
                self.lines.append(line)
        n = 0
        for c in self.cells:
            self.texts.append(ax2.text(self.x_list[n] - self.correct_position[0],
                                       self.y_list[n] - self.correct_position[1], ''))
            n += 1
        ax2.spines['right'].set_visible(False)
        ax2.spines['top'].set_visible(False)
        py.xticks([i for i in range(0, len(self.population_names))], self.population_names)

    def update_weights(self, weight_name):
        n = 0
        for c in self.cells:
            for target in self._find_weights(c, weight_name):
                self.lines[n].set_linewidth(target)
                n += 1
                py.draw()

    def update_spikes(self, sim_time):
        n = 0
        for c in self.cells:
            spikes = np.asarray(c.get_spikes())
            self.texts[n].set_text(str(spikes.shape[0]))
            alpha = spikes > (sim_time - 50)
            self.nodes[n].set_alpha(np.sum(alpha) / 10)
            n += 1
            py.draw()

    def _get_edges(self, weight_name):
        result = []
        for c in self.cells:
            soma = c.filter_secs('soma')
            if c._spike_detector is None:
                c.make_spike_detector(soma(0.5))
            split_name = c.name.split('[')
            pop_name = split_name[0]

            try:
                x_pos = int(pop_name[-1])
            except ValueError:
                x_pos = self.population_names.index(pop_name)

            y_pos = int(split_name[-1][:-1])

            if 'inh' in c.name:
                self.colors.append('red')
                y_pos -= 5
            elif 'hid' in c.name:
                self.colors.append('blue')
            else:
                self.colors.append('green')

            self.x_list.append(x_pos)
            self.y_list.append(y_pos)
            result.append(self._find_target(c, x_pos, y_pos, weight_name))
        return result

    def _find_target(self, c, x_pos, y_pos, weight_name):
        result = []
        for nc in c.ncs:
            if "SpikeDetector" in nc.name:
                continue
            elif isinstance(nc.source, Seg) and isinstance(nc.target, PointProcess):
                split_target = nc.source.parent.parent.name.split('[')
                pop_name = split_target[0]

                try:
                    x_trg = int(pop_name[-1])
                except ValueError:
                    x_trg = self.population_names.index(pop_name)

                y_trg = int(split_target[-1][:-1])

                weight = None
                if self.plot_constant_connections and hasattr(nc.target.hoc, weight_name):
                    weight = getattr(nc.target.hoc, weight_name)

                result.append(((x_pos, x_trg), (y_pos, y_trg), weight))
        return result

    @staticmethod
    def _find_weights(c, weight_name):
        targets = []
        for nc in c.ncs:
            if "SpikeDetector" in nc.name:
                continue
            elif isinstance(nc.source, Seg) and isinstance(nc.target, PointProcess) and hasattr(nc.target.hoc, weight_name):
                weight = getattr(nc.target.hoc, weight_name)
                targets.append(weight)
        return targets

    def _get_population_names(self):
        result = []
        for c in self.cells:
            population_name = c.name.split('[')[0]
            if population_name not in result:
                result.append(population_name)

        regs = [(re.findall("[0-9]+", n), n) for n in result]
        # sort by number in population name (if contains)
        result = sorted([(int(l[0]) if len(l) > 0 else math.inf, n) for l, n in regs], key=lambda x: x[0])

        return [n for i, n in result]
