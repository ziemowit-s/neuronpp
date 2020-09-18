import time
from typing import List, Optional

import numpy as np
from neuron import h

from neuronpp.core.neuron_removable import NeuronRemovable

try:
    from neuron.hoc import HocObject
except ImportError:
    from neuron.hoc36 import HocObject
from neuron.units import ms, mV

h.load_file('stdrun.hoc')


class Simulation(NeuronRemovable):
    def __init__(self, init_v: float = None, dt: float = 0.025, warmup: float = 0, warmup_dt=None,
                 init_sleep: float = 0, shape_plots: Optional[List[h.PlotShape]] = None,
                 constant_timestep: bool = True, with_neuron_gui: bool = False,
                 check_pointers: bool = False, warmup_on_create=False):
        """
        Create an Simulation object to control the NEURON's simulation.

        Simulation WILL NOT create a NEURON environment but rather allows to access to the
        NEURON's simulator state. So if you create many Simulation objects, all of them will have
        access to the same NEURON's state.

        After creating the Simulation object and execute the run() method for the first time
        reinit() will be called. You can also call reinit() to re-init the NEURON any time.

        :param init_v
            initial value in mV for the neuron function finitialize().
            In many cases it is -70 mV but you need to specify it explicitely.
            If left None it will take h.v_init param as default init_v.
        :param dt
            value of the fundamental integration time step, dt, used by fadvance().
            When a value is entered into the field editor it is rounded down so that an integral
            multiple of fadvance’s make up a SingleStep.

            With constant_timestep=False, the dt arg, fadvance returns at t+dt, it means that any
            variable timestep choose by the simulator is computed as next_timestep+dt.
        :param warmup
            in ms, default is 0 ms. Warmup is executed during the first call of run() method,
            before executing the first run.

            By default dt during warmup is warmup/10, so there will be 10 steps during warmup,
            however due to param constant_timestep, the number of steps and their size may vary.
            You can also define custom dt for warmup by warmup_dt param
        :param init_sleep
            sleep time in seconds. To sleep before first run.
            It performs time.sleep(init_sleep) before the first run.
        :param shape_plots:
            a list of objects returned by the function utils.utils.make_shape_plot().
            It allows to create shape plots in NEURON GUI
        :param constant_timestep
            Default is True. Decide if you want a constant timestep of the simulation.

            Multi order variable time step integration method which may be used in place of the
            default staggered fixed time step method. The performance benefits can be substantial
            (factor of more than 10) for problems in which all states vary slowly for long periods
            of time between fast spikes.

            With constant_timestep=False, the dt arg, fadvance returns at t+dt, it means that any
            variable timestep choose by the simulator is computed as next_timestep+dt.

            It perform NEURON'S call h.CVode().active(not constant_timestep)
        :param with_neuron_gui
            default False
        :param check_pointers
            WARNING: This is an experimental feature, so use it carefully.
            By default it is False, meaning it is turned off.

            If True it will check if all pointers are correctly pointed to the required variables.

            Turn off this feature if the simulation ends unexpectedly without error but with the
            information (in Linux):
            `Process finished with exit code 139 (interrupted by signal 11: SIGSEGV)`
        :param warmup_on_create:
            Default False. If True warmup will be done on Simulation object creation
        """
        if with_neuron_gui:
            from neuron import gui

        if isinstance(shape_plots, HocObject):
            shape_plots = [shape_plots]

        if init_v is None:
            init_v = h.v_init
        self.init_v = init_v
        self.dt = dt
        self.warmup_dt = warmup_dt
        self.shape_plots = shape_plots
        self.current_runtime = 0
        if init_sleep < 0:
            raise ValueError("init_sleep time must be >= 0.")
        self.init_sleep = init_sleep
        if warmup < 0:
            raise ValueError("warmup time must be >= 0.")
        self.warmup = warmup
        self.check_pointers = check_pointers

        h.CVode().active(not constant_timestep)

        self.warmup_done = False
        if warmup_on_create:
            self._make_warmup()

    def reinit(self):
        """
        This method restart simulation time to 0, reinitialize the voltage to the init value and
        clear all recorded values in Record objects (its clear inside vector for each segment
        recorded).

        After creating the Simulation object and execute the run() method for the first time
        reinit() will be called. You can also call reinit() to re-init the NEURON any time.

        No other Hoc object is removed, eg. all sections remains. If you want to remove NEURON from
        objects you can:
          * call remove_immediate_from_neuron() method on each Wrapper object (eg. Sec, Seg, NetCon)
          * call remove_immediate_from_neuron() method on each Cell object, which automatically
            removes also containing wrappers
          * delete or reassign all references to the object you want to delete

        To check how many Sections in NEURON remains check simulation.size property.
        """
        if self.check_pointers:
            self._check_point_process_pointers()
        h.fcurrent()
        h.finitialize(self.init_v * mV)

        if self.init_sleep > 0:
            print("sleep before run for: %s seconds" % self.init_sleep)
            time.sleep(self.init_sleep)

        self.warmup_done = False
        h.dt = self.dt

    @property
    def t(self):
        return h.t

    @property
    def size(self) -> int:
        """
        Returns number of sections in the current NEURON environment.
        """
        return len(list(h.allsec()))

    def is_neuron_empty(self) -> bool:
        """
        Returns True if the current NEURON environment has no sections created.
        """
        return self.size == 0

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
            self._make_warmup()

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

            if self.shape_plots is not None:
                self._plot_shapes()
            if debug:
                print("Current time:", round(r, 2), "ms\n",
                      'Computation time:', round(computation_time * 1000, 2), "ms\n",
                      'Simulation stepsize:', stepsize)

        self.current_runtime = runtime

    def _make_warmup(self):
        self.reinit()

        if self.warmup > 0:
            if self.warmup_dt is None:
                h.dt = self.warmup / 10
            else:
                h.dt = self.warmup_dt
            h.continuerun(self.warmup * ms)
            h.dt = self.dt
        self.warmup_done = True

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
