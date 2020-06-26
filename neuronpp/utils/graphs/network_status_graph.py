import numpy as np
from typing import cast, List
import matplotlib.pyplot as py

from neuronpp.core.hocwrappers.point_process import PointProcess
from neuronpp.core.populations.population import Population


class NetworkStatusGraph:
    def __init__(self, populations: List[Population], additional_weight_name='w', soma_name='soma'):
        """
        
        :param populations: 
            list of population to create a graph
        :param additional_weight_name: 
            name of additional weight which is point_process's additional weight
            (which change with plasticity), if a point_process don't contains this name
            it will be ignored. In such case only weight from netcon will be displayed.
        :param soma_name:
            name of soma segment. It will be used if you haven't put a spike detector into the cell
        """
        self.populations = populations
        self.check_and_add_spike_detector(soma_name)
        self.population_names = [p.name for p in populations]

        self.colors = []
        self.texts = []
        self.lines = []
        self.x_list = []
        self.y_list = []
        self.nodes = []

        self.correct_position = (0.1, 0.1)

        self.edges = self._get_edges(additional_weight_name)

    def plot(self):
        py.figure()
        ax = py.subplot(111)
        self.nodes = []

        for cell_num in range(len(self.x_list)):
            self.nodes.append(ax.scatter(self.x_list[cell_num], self.y_list[cell_num], s=300,
                                          color=self.colors[cell_num], alpha=0.5))

        for xs, ys, weight in self.edges:
            line, = ax.plot(xs, ys, lw=weight, color='grey')
            self.lines.append(line)

        n = 0
        for _ in self.populations:
            self.texts.append(ax.text(self.x_list[n] - self.correct_position[0],
                                       self.y_list[n] - self.correct_position[1], ''))
            n += 1
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        py.xticks([i for i in range(len(self.population_names))], self.population_names)
        py.yticks([i for i in range(max(self.y_list) + 1)],
                  [f"Cell {i}" for i in range(max(self.y_list) + 1)])

    def update_weights(self, weight_name):
        n = 0
        for p in self.populations:
            for c in p.cells:
                for target in self._find_weights(c, weight_name):
                    self.lines[n].set_linewidth(target)
                    n += 1
                    py.draw()

    def update_spikes(self, sim_time):
        n = 0
        for p in self.populations:
            for c in p.cells:
                spikes = np.asarray(c.get_spikes())
                self.texts[n].set_text(str(spikes.shape[0]))
                alpha = spikes > (sim_time - 50)
                self.nodes[n].set_alpha(np.sum(alpha) / 10)
                n += 1
            py.draw()

    def check_and_add_spike_detector(self, soma_name='soma'):
        for p in self.populations:
            for c in p.cells:
                soma = c.filter_secs(soma_name)
                if c._spike_detector is None:
                    c.make_spike_detector(soma(0.5))

    def _get_edges(self, additional_weight_name):
        result = []
        for population in self.populations:
            source_x_pos = self.population_names.index(population.name)

            for i, target_cell in enumerate(population.cells):
                self.x_list.append(source_x_pos)
                self.y_list.append(i)
                if 'inh' in target_cell.name:
                    self.colors.append('red')
                elif 'hid' in target_cell.name:
                    self.colors.append('blue')
                else:
                    self.colors.append('green')

                for i, target_syn in enumerate(target_cell.syns):
                    for nc in target_syn.netcons:
                        source_y_pos = i

                        try:
                            target_x_pos = nc.source.parent.cell.population.name
                        except AttributeError:
                            # show only connections from other cells as source
                            continue

                        target_y_pos = int(target_cell.name.split('[')[-1][:-1])

                        weight = nc.get_weight()
                        if hasattr(target_syn.hoc, additional_weight_name):
                            weight *= getattr(target_cell.hoc, additional_weight_name)

                        xs = source_x_pos, target_x_pos
                        ys = source_y_pos, target_y_pos
                        result.append((xs, ys, weight))
        return result

    @staticmethod
    def _find_weights(c, weight_name):
        targets = []
        for pp in c.pps:
            pp = cast(PointProcess, pp)
            if hasattr(pp.hoc, weight_name):
                weight = getattr(pp.hoc, weight_name)
                targets.append(weight)
        return targets
