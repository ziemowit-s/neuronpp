import time
import numpy as np
from neuron import h

try:
    from neuron.hoc import HocObject
except ImportError:
    from neuron.hoc36 import HocObject
from neuron.units import ms, mV

h.load_file('stdrun.hoc')


class Simulation:
    def __init__(self, init_v=None, dt=0.025, warmup=1, init_sleep=0, shape_plots=(),
                 constant_timestep=True, with_neuron_gui=False, check_pointers=False):
        """
        :param init_v:
            initial value in mV for the neuron function finitialize().
            In many cases it is -70 mV but you need to specify it explicitely.
            If left None it will take h.v_init param as default init_v.
        :param warmup:
            in ms, default is 1 ms.
        :param init_sleep
            sleep time in seconds. To sleep before first run
        :param with_neuron_gui
        :param check_pointers
            WARNING: This is an experimental feature, so use it carefully.
            By default it is False, meaning it is turned off.

            If True it will check if all pointers are correctly pointed to the required variables.

            Turn off this feature if the simulation ends unexpectedly without error but with the
            information (in Linux):
            `Process finished with exit code 139 (interrupted by signal 11: SIGSEGV)`
        """
        if with_neuron_gui:
            from neuron import gui

        if isinstance(shape_plots, HocObject):
            shape_plots = [shape_plots]

        if init_v is None:
            init_v = h.v_init
        self.init_v = init_v
        self.dt = dt
        self.shape_plots = shape_plots
        self.last_runtime = 0
        self.init_sleep = init_sleep
        self.warmup = warmup
        self.check_pointers = check_pointers

        h.CVode().active(not constant_timestep)

        self.warmup_done = False

    def reset(self):
        print("Simulation initialization.")
        if self.check_pointers:
            self._check_point_process_pointers()
        h.initnrn()
        h.frecord_init()
        h.finitialize(self.init_v * mV)

        if self.init_sleep > 0:
            print("sleep before run for: %s seconds" % self.init_sleep)
            time.sleep(self.init_sleep)

        if self.warmup > 0:
            h.dt = self.warmup / 10
            h.continuerun(self.warmup * ms)
        h.dt = self.dt

    @property
    def t(self):
        return h.t

    def run(self, runtime, stepsize=None, delay_between_steps=1, debug=False):
        """
        :param runtime:
            in ms (simulation time)
        :param stepsize:
            in ms. Default None -> stepsize is the size of runtime
        :param delay_between_steps:
            in ms (computer real time)
        :param debug
            if True, print debug information:
            * Current time (in ms)
            * Computation time (in ms)
            * Simulation stepsize
        """
        if not self.warmup_done:
            self.reset()
            self.warmup_done = True
        if stepsize is None:
            stepsize = runtime

        delay_between_steps = delay_between_steps * 1e-3  # between steps

        # prepare run array
        max_runtime = runtime + self.t

        if runtime == stepsize:
            run_array = [self.t + stepsize]
        else:
            run_array = np.arange(0 + self.t + stepsize, max_runtime, stepsize)
            left_run = max_runtime - max(run_array)
            if left_run > 0:
                run_array = np.concatenate([run_array, [max_runtime]])

        # run main loop
        before = time.time()  # compute time before
        for r in run_array:

            # step till i-th ms
            h.continuerun(r * ms)
            current = time.time()
            computation_time = current - before

            # adjust delay
            delay = delay_between_steps - computation_time
            if delay < 0:
                delay = 0
            time.sleep(delay)
            before = time.time()  # compute time before

            self._plot_shapes()
            if debug:
                print("Current time:", round(r, 2), "ms\n",
                      'Computation time:', round(computation_time * 1000, 2), "ms\n",
                      'Simulation stepsize:', stepsize)

        self.last_runtime = runtime

    def _plot_shapes(self):
        # flush shape and console log
        for ps in self.shape_plots:
            ps.fastflush()

    @classmethod
    def _check_point_process_pointers(cls):
        """
        WARNING: This is an experimental feature, so use it carefully.
        By default it is turned off.

        It will check if all pointers are correctly pointed to the required variables.

        Turn off this feature if the simulation ends unexpectedly without error but with the
        information (in Linux):
        `Process finished with exit code 139 (interrupted by signal 11: SIGSEGV)`
        """
        for pp in cls.get_all_point_processes():
            for name in pp.__dict__:

                try:
                    getattr(pp, name)
                except AttributeError as e:
                    if e.args[0].lower() == 'pointer is null':
                        raise AttributeError("RANGE Variable: %s in Point_Process: %s is a NULL "
                                             "POINTER. Set the POINTER before simulation init.\n"
                                             "Located in the section: %s.\n"
                                             "For more information about MOD POINTERs setup check "
                                             "h.setpointer() in NEURON's documentation." %
                                             (name, pp, pp.get_segment().sec))

    @classmethod
    def get_all_point_processes(cls):
        for sec in h.allsec():
            for pp in sec.psection()['point_processes'].values():
                for p in pp:
                    yield p
