import os
from neuron import h
from threading import Thread
from time import gmtime, strftime

from pyvis.network import Network
from pynput.keyboard import Listener

from neuronpp.cells.cell import Cell
from neuronpp.core.hocwrappers.seg import Seg


def make_shape_plot(variable=None, min_val=-70, max_val=40):
    ps = h.PlotShape(True)
    if variable:
        ps.variable(variable)
        ps.scale(min_val, max_val)
    ps.show(0)
    h.fast_flush_list.append(ps)
    ps.exec_menu('Shape Plot')
    return ps


def show_connectivity_graph(cells, result_folder=None, file_name="conectivity_graph.html", height="100%", width="100%",
                            bgcolor="#222222", font_color="white", stim_color="#f5ce42", cell_color="#80bfff", node_distance=200,
                            spring_strength=0.001):
    """
    Creates graph of connections between passed cells. It will create a HTML file presenting the graph in
    the result_folder as well as run the graph in your browser.

    It will create a file cell_graph_[DATE].html in the result_folder, where [DATE is the current date with seconds,
    from the template: "%Y-%m-%d_%H-%M-%S".

    :param cells:
        All cells must be of type NetConCell or just Cell
    :param result_folder:
        Any folder where to put your graph, eg. "graphs". The default is None, meaning that the graph
        html file will be saved to the current working directory
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
        nodes.append(c.name)
        g.add_node(c.name, color=cell_color)
        for nc in c.ncs:
            if isinstance(nc.source, Seg):
                nc_node = nc.source.parent.parent.name
            else:
                nc_node = nc.source.name
            if nc_node not in nodes:
                nodes.append(nc_node)
                if isinstance(nc, Cell):
                    g.add_node(nc_node, color=cell_color)
                else:
                    g.add_node(nc_node, color=stim_color)
            g.add_edge(nc_node, c.name)

    g.show_buttons(filter_=['physics'])
    g.hrepulsion(node_distance=node_distance, spring_strength=spring_strength)

    if result_folder:
        save_path = '%s/%s' % (result_folder, file_name)
    else:
        save_path = file_name

    if result_folder:
        os.makedirs(result_folder, exist_ok=True)
    g.show(save_path)
    print("Saved cell graph into: %s" % save_path)


def key_release_listener(on_press_func):
    def final_func(key):
        if key is not None and hasattr(key, 'char'):
            on_press_func(key.char)

    def listen():
        with Listener(on_press=final_func, on_release=None) as listener:
            listener.join()

    listenThread = Thread(target=listen)
    listenThread.start()
