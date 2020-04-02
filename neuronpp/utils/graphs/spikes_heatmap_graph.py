from neuron import h
from typing import List

from neuronpp.core.cells.netcon_cell import NetConCell
from neuronpp.utils.graphs.heatmap_graph import HeatmapGraph


class SpikesHeatmapGraph(HeatmapGraph):
    def __init__(self, name, cells: List[NetConCell], shape=None, sec="soma", loc=0.5):
        print("Heatmap %s - number -> cell_name mapping:" % name)
        for i, c in enumerate(cells):
            print("%s:" % i, c.name)
            if c._spike_detector is None:
                c.make_spike_detector(c.filter_secs(sec)(loc))

        def extract_func(cell):
            spikes = [ms for ms in cell.get_spikes() if ms > self.last_sim_time]
            return len(spikes)

        super().__init__(name=name, elements=cells, extract_func=extract_func, shape=shape)
