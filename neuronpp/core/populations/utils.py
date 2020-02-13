import os
from time import gmtime, strftime
from pyvis.network import Network

from neuronpp.cells.cell import Cell


def make_cell_graph(cells, result_folder="graphs", height="100%", width="100%", bgcolor="#222222", font_color="white",
                    cell_color="#f5ce42", stim_color="#80bfff", node_distance=140, spring_strength=0.001):
    """
    Creates graph of connections between passed cells. It will create a HTML file presenting the graph in
    the result_folder as well as run the graph in your browser.

    It will create a file cell_graph_[DATE].html in the result_folder, where [DATE is the current date with seconds,
    from the template: "%Y-%m-%d_%H-%M-%S".

    :param cells:
        All cells must be of type NetConCell or just Cell
    :param result_folder:
        Any folder where to put your graph, eg. "graphs". The default is 'graphs' in your working directory.
    :param height:
    :param width:
    :param bgcolor:
    :param font_color:
    :param cell_color:
    :param stim_color:
    :param node_distance:
    :param spring_strength:
    :return:
    """
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

    date = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
    save_path = '%s/cell_graph_%s.html' % (result_folder, date)

    os.makedirs(result_folder, exist_ok=True)
    g.show(save_path)
    print("Saved cell graph into: %s" % save_path)
