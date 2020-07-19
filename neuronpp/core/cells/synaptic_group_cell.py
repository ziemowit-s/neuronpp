from collections import defaultdict
from typing import Optional, Iterable

from neuronpp.core.cells.synaptic_cell import SynapticCell
from neuronpp.core.hocwrappers.synapses.single_synapse import SingleSynapse
from neuronpp.core.hocwrappers.synapses.synaptic_group import SynapticGroup


class SynapticGroupCell(SynapticCell):
    def __init__(self, name=None, compile_paths=None):
        """
        Create a single synapse composed from existing synapses
        :param name:
        :param compile_paths:
        """
        SynapticCell.__init__(self, name, compile_paths=compile_paths)
        self.group_syns = []
        self._group_syn_num = defaultdict(int)

    def filter_synaptic_group(self, mod_name: str = None, name=None, parent=None, tag=None,
                              obj_filter=None, **kwargs):
        """
        Currently all filter passed are treated as AND statements.

        * Whole object callable function passed to the obj_filter param.
            eg. (lambda expression) returns sections which name contains 'apic'
            or their distance > 1000 um from the soma:
          ```
           soma = cell.filter_secs("soma")
           cell.filter_secs(obj_filter=lambda o: 'apic' in o.name or
                                                 h.distance(soma.hoc(0.5), o.hoc(0.5)) > 1000)
          ```

        * Single object field filter based on callable function passed to the obj_filter param.
          eg. (lambda expression) returns sections which parent's name contains less than 10
          characters
          ```
          cell.filter_secs(parent=lambda o: len(o.parent.name) < 10)
          ```

        :param mod_name:
            single string defining name of point process type name
            eg. concere synaptic mechanisms like Syn4PAChDa
        :param name:
            start with 'regex:any pattern' to use regular expression.
            If without 'regex:' - will look which Hoc objects contain the str
        :param parent
        :param tag
        :param obj_filter:
            Whole object callable functional filter.
            If you added also any kwargs they will be together with the
            obj_filter treated as AND statement.
        :return:
        """
        return self.filter(self.group_syns, obj_filter=obj_filter, mod_name=mod_name, name=name,
                           parent=parent, tag=tag, **kwargs)

    def remove_synaptic_group(self, mod_name: str = None, name=None, parent=None, tag=None,
                              obj_filter=None, **kwargs):
        """
        Currently all filter passed are treated as AND statements.

        * Whole object callable function passed to the obj_filter param.
            eg. (lambda expression) returns sections which name contains 'apic'
            or their distance > 1000 um from the soma:
          ```
           soma = cell.filter_secs("soma")
           cell.filter_secs(obj_filter=lambda o: 'apic' in o.name or
                                                 h.distance(soma.hoc(0.5), o.hoc(0.5)) > 1000)
          ```

        * Single object field filter based on callable function passed to the obj_filter param.
          eg. (lambda expression) returns sections which parent's name contains less than 10
          characters
          ```
          cell.filter_secs(parent=lambda o: len(o.parent.name) < 10)
          ```

        :param mod_name:
            single string defining name of point process type name
            eg. concere synaptic mechanisms like Syn4PAChDa
        :param name:
            start with 'regex:any pattern' to use regular expression.
            If without 'regex:' - will look which Hoc objects contain the str
        :param parent
        :param tag
        :param obj_filter:
            Whole object callable functional filter.
            If you added also any kwargs they will be together with the
            obj_filter treated as AND statement.
        :return:
        """
        return self.remove(self.group_syns, obj_filter=obj_filter, mod_name=mod_name, name=name,
                           parent=parent, tag=tag, **kwargs)

    def group_synapses(self, synapses: Iterable[SingleSynapse], name: Optional[str] = None,
                       tag: Optional[str] = None):
        """
        Group existing synapses as a single SynapticGroup

        :param synapses:
            list of synapses of type SingleSynapse
        :param name:
            string name, if None it will be a number from 0 to n, where n is the number of
            synaptic group creation.
        :param tag:
            string tag which will be attached to the synaptic group as tag.
            you can filter by this tag
        :return
            created synaptic group object
        """
        if isinstance(synapses[0], (list, tuple, set)):
            synapses = [s for syns in synapses for s in syns]

        mod_names = '+'.join([s.point_process_name for s in synapses])
        numerical_name = str(self._group_syn_num[mod_names])

        if name is None:
            name = numerical_name

        result = SynapticGroup(synapses=synapses, name=name, tag=tag)
        self.group_syns.append(result)
        self._group_syn_num[mod_names] += 1

        return result
