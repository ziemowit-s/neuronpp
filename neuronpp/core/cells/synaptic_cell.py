from collections import defaultdict
from typing import List

import numpy as np

from neuronpp.core.cells.netcon_cell import NetConCell
from neuronpp.core.decorators import distparams
from neuronpp.core.hocwrappers.sec import Sec
from neuronpp.core.hocwrappers.synapses.single_synapse import SingleSynapse


class SynapticCell(NetConCell):
    def __init__(self, name=None, compile_paths=None):
        NetConCell.__init__(self, name, compile_paths=compile_paths)
        self.syns = []
        self._syn_num = defaultdict(int)

    def filter_synapses(self, mod_name: str = None, obj_filter=None, name=None, source=None,
                        point_process=None, parent=None, tag=None, **kwargs):
        """
        Currently all filter passed are treated as AND statements.

        * Whole object callable function passed to the obj_filter param.
            eg. (lambda expression) returns sections which name contains 'apic' or
            their distance > 1000 um from the soma:
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
            single string defining name of point process type name, eg. concere synaptic mechanisms
            like Syn4PAChDa
        :param obj_filter:
            Whole object callable functional filter. If you added also any kwargs they will be
            together with the
            obj_filter treated as AND statement.
        :param name:
            start with 'regex:any pattern' to use regular expression. If without 'regex:' -
            will look which Hoc objects contain the str
        :param source:
            string of source compound name (if source is provided)
        :param point_process:
            string of point process compound name
        :return:
        """
        return self.filter(self.syns, obj_filter=obj_filter, mod_name=mod_name, name=name,
                           source=source, point_process=point_process, parent=parent,
                           tag=tag, **kwargs)

    def remove_synapses(self, mod_name: str = None, obj_filter=None, name=None, source=None,
                        point_process=None, parent=None, tag=None, **kwargs):
        """
        Currently all filter passed are treated as AND statements.

        * Whole object callable function passed to the obj_filter param.
            eg. (lambda expression) returns sections which name contains 'apic' or
            their distance > 1000 um from the soma:
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
            single string defining name of point process type name, eg. concere synaptic mechanisms
            like Syn4PAChDa
        :param obj_filter:
            Whole object callable functional filter. If you added also any kwargs they will be
            together with the
            obj_filter treated as AND statement.
        :param name:
            start with 'regex:any pattern' to use regular expression. If without 'regex:' -
            will look which Hoc objects contain the str
        :param source:
            string of source compound name (if source is provided)
        :param point_process:
            string of point process compound name
        :return:
        """
        return self.remove(self.syns, obj_filter=obj_filter, mod_name=mod_name, name=name,
                           source=source, point_process=point_process, parent=parent,
                           tag=tag, **kwargs)

    @distparams
    def add_synapse(self, source, mod_name: str, seg, netcon_weight=1, delay=1, threshold=10,
                    tag: str = None, **synaptic_params):
        """

        :param source:
            Can be only: hocwrappers.NetStim, hocwrappers.VecStim, Seg or None.
            If None it will create NetConn with no source, which can be use as external event source
        :param netcon_weight:
        :param tag:
        :param mod_name:
        :param seg:
        :param source_loc:
        :param target_loc:
        :param delay:
        :param threshold:
        :param synaptic_params:
        :return:
        """
        pp = self.add_point_process(mod_name=mod_name, seg=seg, tag=tag, **synaptic_params)
        nn = self.add_netcon(source=source, netcon_weight=netcon_weight, point_process=pp,
                             delay=delay, threshold=threshold)

        syn_name = "%s[%s]" % (pp.name, self._syn_num[mod_name])
        syn = SingleSynapse(source, point_process=pp, netcon=nn, name=syn_name, tag=tag)
        self.syns.append(syn)
        self._syn_num[mod_name] += 1

        return syn

    @distparams
    def add_random_uniform_synapses(self, number, source, mod_name: str, secs: List[Sec],
                                    netcon_weight=1, delay=1, threshold=10, tag: str = None,
                                    **synaptic_params):
        """
        """
        max_l = int(sum([s.hoc.L for s in secs]))
        locations = np.random.rand(number)
        locations *= max_l

        results = []
        for syn_loc in locations:
            current_L = 0
            for sec in secs:
                s = sec.hoc
                current_L += s.L

                # if synapse will be located in this section
                if current_L > syn_loc:
                    section_loc = (syn_loc - current_L + s.L) / s.L

                    seg = sec(section_loc)
                    r = self.add_synapse(source=source, mod_name=mod_name, seg=seg,
                                         netcon_weight=netcon_weight, delay=delay,
                                         threshold=threshold, tag=tag, **synaptic_params)
                    results.append(r)
                    break

        return results
