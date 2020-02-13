import os
from time import gmtime, strftime

from pyvis.network import Network

from neuronpp.cells.cell import Cell


def graph(cells, result_folder, height="100%", width="100%", bgcolor="#222222", font_color="white", cell_color="#f5ce42",
          stim_color="#80bfff", node_distance=140, spring_strength=0.001):
    g = Network(height=height, width=width, bgcolor=bgcolor, font_color=font_color, directed=True)
    nodes = []
    for c in cells:
        node = str(c)
        nodes.append(node)
        g.add_node(node, color=cell_color)
        for nc in c.ncs:
            nc_node = str(nc.source)
            if nc_node not in nodes:
                nodes.append(nc_node)
                if isinstance(nc, Cell):
                    g.add_node(nc_node, color=cell_color)
                else:
                    g.add_node(nc_node, color=stim_color)
            g.add_edge(nc_node, node)

    g.show_buttons(filter_=['physics'])
    g.hrepulsion(node_distance=node_distance, spring_strength=spring_strength)

    os.makedirs(result_folder, exist_ok=True)
    date = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
    g.show('%s/cell_graph_%s.html' % (result_folder, date))