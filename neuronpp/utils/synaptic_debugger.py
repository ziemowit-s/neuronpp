import time

from neuron.units import ms
from pynput.keyboard import Key

from neuronpp.utils.record import Record
from neuronpp.utils.run_sim import RunSim
from neuronpp.utils.utils import key_release_listener


class SynapticDebugger:
    def __init__(self, syns, secs=None, syn_variables="w", sec_variables='v', sec_loc=0.5, init_v=-70, warmup=0):
        self.syns = syns
        self.secs = secs

        self.syn_rec = Record(elements=syns, variables=syn_variables)

        self.sec_rec = None
        if secs:
            self.sec_rec = Record(elements=secs, variables=sec_variables, loc=sec_loc)

        self.sim = RunSim(init_v=init_v, warmup=warmup)

    def debug(self, i=None, stim_time=0, run_time=1):
        if run_time <= stim_time:
            raise ValueError("Param 'run_time' cannot be smaller than 'stim_time'.")

        if i is None:
            for s in self.syns:
                s.make_event(stim_time)
        else:
            self.syns[i].make_event(stim_time)

        self.run(run_time)

    def stim(self, index=None, stim_time=1):
        """
        :param index:
            Index of the synapse. If None - all will be stim
        :param stim_time:
            in ms
        :return:
        """
        if index is None:
            for s in self.syns:
                s.make_event(stim_time)
        else:
            self.syns[index].make_event(stim_time)

    def run(self, run_time=1, plot_steps=10000):
        """

        :param run_time:
        in ms
        :return:
        """
        for _ in range(run_time):
            self.sim.run(1)
            self.syn_rec.plot(animate=True)
            if self.sec_rec:
                self.sec_rec.plot(animate=True, steps=plot_steps)

    def debug_interactive(self, index=None, stim_key='w', plot_steps=10000, interval=1):
        """
        :param index:
            Index of the synapse. If None - all will be stim
        :param stim_key:
            Which key on the keyboard you will press to stimulate synapse/synapses
        :param interval:
            in ms
        :return:
        """
        keys = ['']
        def key_press(key):
            keys[0] = key
        key_release_listener(key_press)
        while True:
            key_pressed = keys[0]
            if key_pressed == stim_key:
                self.stim(index=index)
                keys[0] = None
            self.run(interval, plot_steps=plot_steps)
