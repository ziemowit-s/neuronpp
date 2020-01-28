from neuronpp.utils.record import Record
from neuronpp.utils.run_sim import RunSim
from neuronpp.utils.utils import key_release_listener


class SynapticDebugger:
    def __init__(self, init_v=-70, warmup=0):
        self.syns = {}
        self.secs = []

        self.syn_recs = []
        self.sec_recs = []

        self.init_v = init_v
        self.warmup_time = warmup
        self.sim = None

    def add_syns(self, syns, syn_variables="w", key_press=None):
        rec = Record(elements=syns, variables=syn_variables)
        self.syn_recs.append(rec)

        name = key_press
        if name is None:
            name = str(len(self.syns))
        self.syns[name] = syns

    def add_secs(self, secs, sec_variables='v', sec_loc=0.5):
        rec = Record(elements=secs, variables=sec_variables, loc=sec_loc)
        self.sec_recs.append(rec)

    def warmup(self):
        if self.sim is None:
            self.sim = RunSim(init_v=self.init_v, warmup=self.warmup_time)

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
            self._make_plots(plot_steps)

    def debug_interactive(self, index=None, plot_steps=10000, interval=1):
        """
        :param index:
            Index of the synapse. If None - all will be stim
        :param interval:
            in ms
        :return:
        """
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
