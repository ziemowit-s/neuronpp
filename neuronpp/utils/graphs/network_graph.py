import numpy as np
from typing import List
import matplotlib.pyplot as plt

from neuronpp.core.populations.population import Population


class NetworkGraph:
    def __init__(self, populations: List[Population], additional_weight_name='w', soma_name='soma'):
        """
        Create a Network Graph

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
        self._check_and_add_spike_detector(soma_name)
        self.population_names = [p.name for p in populations]

        self.colors = []
        self.texts = []
        self.lines = []
        self.x_list = []
        self.y_list = []
        self.nodes = []

        self.correct_position = (0.1, 0.1)

        self.edges = self._get_edges(additional_weight_name)
        self.fig = None

    def plot(self, with_weight_thickness=True):
        """
        :param with_weight_thickness:
            if True - it will show weight as the thickness of the edge between nodes
        """
        self.fig = plt.figure()
        ax = plt.subplot(111)
        self.nodes = []

        for cell_num in range(len(self.x_list)):
            self.nodes.append(ax.scatter(self.x_list[cell_num], self.y_list[cell_num], s=300,
                                         color=self.colors[cell_num], alpha=0.5))

        for xs, ys, weight in self.edges:
            if not with_weight_thickness:
                weight = 1
            line, = ax.plot(xs, ys, linewidth=weight, color='grey')
            self.lines.append(line)

        n = 0
        for _ in self.populations:
            self.texts.append(ax.text(self.x_list[n] - self.correct_position[0],
                                      self.y_list[n] - self.correct_position[1], ''))
            n += 1
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        plt.xticks([i for i in range(len(self.population_names))], self.population_names)
        plt.yticks([i for i in range(max(self.y_list) + 1)],
                   ["Cell %s" % i for i in range(max(self.y_list) + 1)])

    def update_weights(self, additional_weight_name='w'):
        """
        Update weights display on the network graph

        :param additional_weight_name:
            name of additional weight which is point_process's additional weight
            (which change with plasticity), if a point_process don't contains this name
            it will be ignored. In such case only weight from netcon will be displayed.
        """
        new_weights = []
        for p in self.populations:
            for c in p.cells:
                for weight in self._get_new_weights(c, additional_weight_name):
                    new_weights.append(weight)

        for i, weight in enumerate(new_weights):
            self.lines[i].set_linewidth(weight)
        self.redraw()

    def update_spikes(self, sim_time=1):
        """
        Update spikes display on the network graph
        :param sim_time:
            simulation time in ms
        """
        n = 0
        for p in self.populations:
            for c in p.cells:
                spikes = np.asarray(c.spikes())
                if spikes.size == 0:
                    n += 1
                    continue
                else:
                    self.texts[n].set_text(str(spikes.shape[0]))
                    alpha = spikes > (sim_time - 50)
                    self.nodes[n].set_alpha(np.sum(alpha) / 10)
                    n += 1
        self.redraw()

    def redraw(self):
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def _check_and_add_spike_detector(self, soma_name='soma'):
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

                        weight = nc.get_weight()
                        if hasattr(target_syn.hoc, additional_weight_name):
                            weight *= getattr(target_cell.hoc, additional_weight_name)

                        target_y_pos = int(target_cell.name.split('[')[-1][:-1])
                        xs = source_x_pos, target_x_pos
                        ys = source_y_pos, target_y_pos
                        result.append((xs, ys, weight))
        return result

    @staticmethod
    def _get_new_weights(cell, additional_weight_name):
        result = []
        for syn in cell.syns:
            for nc in syn.netcons:
                try:
                    target_x_pos = nc.source.parent.cell.population.name
                except AttributeError:
                    # get only connections from other cells as source
                    continue

                weight = nc.get_weight()
                if hasattr(syn.hoc, additional_weight_name):
                    weight *= getattr(cell.hoc, additional_weight_name)

                result.append(weight)
        return result
