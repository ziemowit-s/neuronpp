from neuron import h
from threading import Thread

from pynput.keyboard import Listener


def make_shape_plot(variable=None, min_val=-70, max_val=40):
    ps = h.PlotShape(True)
    if variable:
        ps.variable(variable)
        ps.scale(min_val, max_val)
    ps.show(0)
    h.fast_flush_list.append(ps)
    ps.exec_menu('Shape Plot')
    return ps


def key_release_listener(on_press_func):
    def listen():
        with Listener(on_press=on_press_func, on_release=None) as listener:
            listener.join()

    listenThread = Thread(target=listen)
    listenThread.start()
