import time
from collections import defaultdict

from neuronpp.core.neuron_removable import NeuronRemovable
from neuronpp.utils.record import Record
from neuronpp.core.hocwrappers.seg import Seg
from neuronpp.utils.simulation import Simulation
from neuronpp.core.hocwrappers.netcon import NetCon
from neuronpp.core.hocwrappers.synapses.synapse import Synapse
from neuronpp.utils.utils import key_release_listener, KEY_LISTENER_IMPORTED


class SynapticDebugger(NeuronRemovable):
    def __init__(self, init_v=-70, warmup=0, delay_between_steps=0):
        """

        :param init_v:
        :param warmup:
        :param delay_between_steps:
            in ms
        """
        self.syns = defaultdict(list)
        self.secs = []

        self.syn_recs = []
        self.sec_recs = []

        self.init_v = init_v
        self.warmup_time = warmup
        self.delay_between_steps = delay_between_steps / 1000
        self.sim = None

    def add_syn(self, syn: Synapse, syn_variables=None, key_press=None, plot=False):
        if not isinstance(syn, Synapse):
            raise TypeError(f"Param 'syn' must be of type Synapse, but provided '{syn.__class__}'")
        if plot and not syn_variables:
            raise ValueError("You must define synaptic variable befor plotting or set plot=False")

        if plot and syn_variables:
            rec = Record(elements=syn, variables=syn_variables)
            self.syn_recs.append(rec)

        name = key_press
        if name is None:
            name = str(len(self.syns))
        self.syns[name].append(syn)

    def add_con(self, con: NetCon, key_press=None):
        if not isinstance(con, NetCon):
            raise TypeError("Param 'con' must be of type NetCon, but provided '%s'" % con.__class__)
        name = key_press
        if name is None:
            name = str(len(self.syns))
        self.syns[name].append(con)

    def add_seg(self, seg: Seg, sec_variables='v'):
        if not isinstance(seg, Seg):
            raise TypeError("Param 'seg' must be of type Seg, but provided '%s'" % seg.__class__)
        rec = Record(elements=seg, variables=sec_variables)
        self.sec_recs.append(rec)

    def warmup(self):
        if self.sim is None:
            self.sim = Simulation(init_v=self.init_v, warmup=self.warmup_time)

    def debug(self, i=None, name=None, stim_time=0, run_time=1):
        self.warmup()

        if run_time <= stim_time:
            raise ValueError("Param 'run_time' cannot be smaller than 'stim_time'.")

        for syns in self._get_syns(name):
            if i is None:
                for s in syns:
                    s.make_event(stim_time)
            else:
                self.syns[i].make_event(stim_time)

        self.run(run_time)

    def stim(self, index=None, name=None, stim_time=1):
        """
        :param index:
            Index of the synapse. If None - all will be stim
        :param stim_time:
            in ms
        :return:
        """
        self.warmup()

        if index is None:
            for s in self._get_syns(name):
                s.make_event(stim_time)
        else:
            self.syns[index].make_event(stim_time)

    def run(self, run_time=1, plot_steps=10000):
        """

        :param run_time:
        in ms
        :return:
        """
        self.warmup()

        for _ in range(run_time):
            self.sim.run(1)
            if self.delay_between_steps > 0:
                time.sleep(self.delay_between_steps)
            self._make_plots(plot_steps)

    def debug_interactive(self, index=None, plot_steps=10000, interval=1):
        """
        :param index:
            Index of the synapse. If None - all will be stim
        :param interval:
            in ms
        :return:
        """
        if not KEY_LISTENER_IMPORTED:
            raise ImportError("Interactive debugging won't work due to import error related to:"
                              " pynput.keyboard.Listener.\n"
                              "Do not use Interactive debugging unless you fix this issue.\n"
                              "Bear in mind that Interactive debugging requires a machine with a "
                              "display. Interactive debugging won't work no the server.")

        self.warmup()
        keys = ['']

        def key_press(key):
            keys[0] = key
        key_release_listener(key_press)

        while True:
            key_pressed = keys[0]

            for stim_key_name in self.syns.keys():
                if len(key_pressed) > 0:
                    if key_pressed == stim_key_name:
                        self.stim(index=index, name=stim_key_name)
                        keys[0] = ''
                        break

            self.run(interval, plot_steps=plot_steps)

    def _get_syns(self, name):
        if name is None:
            return [s for syns in self.syns.values() for s in syns]
        else:
            return self.syns[name]

    def _make_plots(self, plot_steps):
        for syn_rec in self.syn_recs:
            syn_rec.plot(animate=True, steps=plot_steps)
        for sec_rec in self.sec_recs:
            sec_rec.plot(animate=True, steps=plot_steps)
