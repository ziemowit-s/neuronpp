from collections import defaultdict

from neuronpp.core.cells.synaptic_cell import SynapticCell
from neuronpp.core.hocwrappers.composed.complex_synapse import ComplexSynapse


class ComplexSynapticCell(SynapticCell):
    def __init__(self, name=None, compile_paths=None):
        SynapticCell.__init__(self, name, compile_paths=compile_paths)
        self.complex_syns = []
        self._complex_syn_num = defaultdict(int)

    def filter_complex_synapses(self, mod_name: str = None, name=None, parent=None, tag=None, obj_filter=None,
                                **kwargs):
        """
        Currently all filter passed are treated as AND statements.

        * Whole object callable function passed to the obj_filter param.
            eg. (lambda expression) returns sections which name contains 'apic' or their distance > 1000 um from the soma:
          ```
           soma = cell.filter_secs("soma")
           cell.filter_secs(obj_filter=lambda o: 'apic' in o.name or h.distance(soma.hoc(0.5), o.hoc(0.5)) > 1000)
          ```

        * Single object field filter based on callable function passed to the obj_filter param.
          eg. (lambda expression) returns sections which parent's name contains less than 10 characters
          ```
          cell.filter_secs(parent=lambda o: len(o.parent.name) < 10)
          ```

        :param mod_name:
            single string defining name of point process type name, eg. concere synaptic mechanisms like Syn4PAChDa
        :param name:
            start with 'regex:any pattern' to use regular expression. If without 'regex:' - will look which Hoc objects contain the str
        :param obj_filter:
            Whole object callable functional filter. If you added also any kwargs they will be together with the
            obj_filter treated as AND statement.
        :return:
        """
        return self.filter(self.complex_syns, obj_filter=obj_filter, mod_name=mod_name, name=name, parent=parent,
                           tag=tag, **kwargs)

    def group_complex_synapses(self, tag=None, *synapses):
        """

        :param synapses:
        :param tag:
        :return:
        """
        if isinstance(synapses[0], (list, tuple, set)):
            synapses = [s for syns in synapses for s in syns]

        mod_names = '+'.join([s.mod_name for s in synapses])

        name = str(self._complex_syn_num[mod_names])
        comp_syn = ComplexSynapse(synapses=synapses, name=name, tag=tag)
        self.complex_syns.append(comp_syn)
        self._complex_syn_num[mod_names] += 1

        return comp_syn
