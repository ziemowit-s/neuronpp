from neuron import h

from neuronpp.core.decorators import distparams
from neuronpp.core.cells.utils import get_netstim
from neuronpp.core.cells.core_cell import CoreCell
from neuronpp.core.hocwrappers.netstim import NetStim


class NetStimCell(CoreCell):
    def __init__(self, name: str = None):
        """
        Making NetStim after simulation run() makes it has no effect on the current simulation.
        However it will appear in the next simulation if:
         * you call reinit() on the Simulation object
         * or create a new Simulation object

        :param name:
            the name of the NetStim
        """
        CoreCell.__init__(self, name)
        self.nss = []

    def filter_netstim(self, name: str, obj_filter=None, **kwargs):
        """
        Currently all filter passed are treated as AND statements.

        * Whole object callable function passed to the obj_filter param.
            eg. (lambda expression) returns sections which name contains 'apic' or their
            distance > 1000 um from the soma:
          ```
           soma = cell.filter_secs("soma")
           cell.filter_secs(obj_filter=lambda o: 'apic' in o.name or
           h.distance(soma.hoc(0.5), o.hoc(0.5)) > 1000)
          ```

        * Single object field filter based on callable function passed to the obj_filter param.
          eg. (lambda expression) returns sections which parent's name contains less than
          10 characters
          ```
          cell.filter_secs(parent=lambda o: len(o.parent.name) < 10)
          ```

        :param name:
            start with 'regex:any pattern' to use regular expression. If without 'regex:' - will
            look which Hoc objects contain the str
        :param obj_filter:
            Whole object callable functional filter. If you added also any kwargs they will be
            together with the
            obj_filter treated as AND statement.
        :return:
        """
        return self.filter(searchable=self.nss, obj_filter=obj_filter, name=name, **kwargs)

    def remove_netstim(self, name: str, obj_filter=None, **kwargs):
        """
        Currently all filter passed are treated as AND statements.

        * Whole object callable function passed to the obj_filter param.
            eg. (lambda expression) returns sections which name contains 'apic' or their
            distance > 1000 um from the soma:
          ```
           soma = cell.filter_secs("soma")
           cell.filter_secs(obj_filter=lambda o: 'apic' in o.name or
           h.distance(soma.hoc(0.5), o.hoc(0.5)) > 1000)
          ```

        * Single object field filter based on callable function passed to the obj_filter param.
          eg. (lambda expression) returns sections which parent's name contains less than
          10 characters
          ```
          cell.filter_secs(parent=lambda o: len(o.parent.name) < 10)
          ```

        :param name:
            start with 'regex:any pattern' to use regular expression. If without 'regex:' - will
            look which Hoc objects contain the str
        :param obj_filter:
            Whole object callable functional filter. If you added also any kwargs they will be
            together with the
            obj_filter treated as AND statement.
        :return:
        """
        return self.remove(searchable=self.nss, obj_filter=obj_filter, name=name, **kwargs)

    @distparams
    def add_netstim(self, start, number, interval=1, noise=0):
        """
        Making NetStim after simulation run() makes it has no effect on the current simulation.
        However it will appear in the next simulation if:
         * you call reinit() on the Simulation object
         * or create a new Simulation object

        :param start:
            The absolute value of start in ms.

            The absolute value means that you need to count warmup time as well.
        :param number:
        :param interval:
        :param noise:
        :return:
            created NetStim
        """
        if h.t > 0:
            # TODO: Change all warnings and prints to loggers
            print("Warning: NetStim created after simulation have been initiated, will not affect "
                  "this simulation, but rather the next one after you execute reinit() method on "
                  "the Simulation object.")

        ns_hoc = get_netstim(start=start, number=number, interval=interval, noise=noise)
        name = str(len(self.nss))

        ns = NetStim(ns_hoc, parent=self, name="NetStim[%s]" % name)
        self.nss.append(ns)
        return ns
