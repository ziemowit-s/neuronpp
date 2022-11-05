import os

from neuron import h
from typing import cast
from threading import Thread
from Xlib.error import DisplayConnectionError

from pyvis.network import Network
try:
    from pynput.keyboard import Listener
    KEY_LISTENER_IMPORTED = True

except DisplayConnectionError as e:
    print("Warning: key listeners and interactive debugging (on key press) won't work "
          "due to the error: %s" % str(e))
    KEY_LISTENER_IMPORTED = False

from neuronpp.core.hocwrappers.seg import Seg
from neuronpp.core.hocwrappers.netcon import NetCon


def is_derived_from(test_class, template_class):
    """
    Decide if the test_class derived from template_class
    :param test_class:
        class which be tested if it derived from template_class
    :param template_class:
        class to test if test_class derived from it
    :return:
    """
    for c in test_class.mro():
        if c == template_class:
            return True
    else:
        return False


def make_shape_plot(variable: str = None, min_val=-70, max_val=40):
    """
    Create a shape plot in NEURON GUI
    :param variable:
        variable name to show on the neural shape. By default (None) it will show voltage
    :param min_val:
        min value of variable specified
    :param max_val:
        max valie of the variable specified
    :return:
        HOC's plot shape object
    """
    ps = h.PlotShape(True)
    if variable:
        ps.variable(variable)
        ps.scale(min_val, max_val)
    ps.show(0)
    h.fast_flush_list.append(ps)
    ps.exec_menu('Shape Plot')
    return ps


def show_connectivity_graph(cells, result_folder=None, file_name="conectivity_graph.html",
                            height="800px", width="1280px",
                            bgcolor="#222222", font_color="white", stim_color="#f5ce42",
                            cell_color="#80bfff",
                            edge_excitatory_color="#7dd100", edge_inhibitory_color="#d12d00",
                            is_excitatory_func=lambda pp: pp.hoc.e >= -20,
                            is_show_edge_func=lambda pp: hasattr(pp.hoc, "e"),
                            node_distance=100, spring_strength=0, show_buttons=False):
    """
    Creates graph of connections between passed cells. It will create a HTML file presenting the
    graph in the result_folder as well as run the graph in your browser.

    It will create a file cell_graph_[DATE].html in the result_folder, where [DATE] is the current
    date with seconds, from the template: "%Y-%m-%d_%H-%M-%S".

    :param cells:
        All cells must be of type NetConCell or just Cell
    :param result_folder:
        Any folder where to put your graph, eg. "graphs". The default is None, meaning that the graph
        html file will be saved to the current working directory
    :param file_name:
    :param height:
    :param width:
    :param bgcolor:
    :param font_color:
    :param stim_color:
    :param cell_color:
    :param edge_excitatory_color:
        Color for the excitatory connection; By default it is default edge color
    :param edge_inhibitory_color:
        Color for the inhibitory connection
    :param is_excitatory_func:
        This is the default function:
            lambda point_process = point_process.hoc.e >= -20
        If returns true - a particular connection is excitatory, otherwise inhibitory.
    :param is_show_edge_func:
        This is the default function:
            lambda point_process = hasattr(point_process.hoc, "e"),
        Define whether to show the edge.
    :param node_distance:
    :param spring_strength:
    """
    g = Network(height=height, width=width, bgcolor=bgcolor, font_color=font_color, directed=True)
    nodes = []
    for c in cells:
        nodes.append(c.name)
        g.add_node(c.name, color=cell_color)
        for nc in c.ncs:
            nc = cast(NetCon, nc)
            if "SpikeDetector" in nc.name:
                continue
            elif isinstance(nc.source, Seg):
                nc_node = nc.source.parent.cell.name
                node_color = cell_color
            elif nc.source is None:
                nc_node = "External Stim"
                node_color = stim_color
            else:
                nc_node = nc.source.name
                node_color = stim_color

            if nc_node not in nodes:
                nodes.append(nc_node)
                g.add_node(nc_node, color=node_color)
            if is_show_edge_func is not None and not is_show_edge_func(nc.target):
                continue

            g.add_edge(nc_node, c.name)
            if is_excitatory_func is None:
                g.edges[-1]['color'] = edge_excitatory_color
            else:
                if is_excitatory_func(nc.target):
                    g.edges[-1]['color'] = edge_excitatory_color
                else:
                    g.edges[-1]['color'] = edge_inhibitory_color
    if show_buttons:
        g.show_buttons()
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
    """
    Listener which will execute the function: on_press_func after pressing any key on the keyboard.

    This function is intended to use with the neural interactive debugger (SynapticDebugger)
    for synaptic stimulation.

    It will start a separated thread for the listener.
    :param on_press_func:
        The function which is intented do distinguish if it a pressed key is the required key.
    :return:
    """

    def final_func(key):
        if key is not None and hasattr(key, 'char'):
            on_press_func(key.char)

    def listen():
        with Listener(on_press=final_func, on_release=None) as listener:
            listener.join()

    listenThread = Thread(target=listen)
    listenThread.start()
