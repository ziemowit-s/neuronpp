from neuron import h
from collections import defaultdict
from typing import List, Union

import numpy as np

from neuronpp.core.cells.netcon_cell import NetConCell
from neuronpp.core.decorators import distparams
from neuronpp.core.hocwrappers.netcon import NetCon
from neuronpp.core.hocwrappers.point_process import PointProcess
from neuronpp.core.hocwrappers.sec import Sec
from neuronpp.core.hocwrappers.seg import Seg
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

        return self._add_raw_synapse(source=source, mod_name=mod_name, point_process=pp, netcon=nn,
                                     tag=tag)

    def add_random_uniform_synapses(self, number, source, mod_name: str, secs: List[Sec],
                                    netcon_weight=1, delay=1, threshold=10, tag: str = None,
                                    uniform_by="lenght", **synaptic_params):
        """
        Add synapses on selected sections with random uniform distribution.

        :param number:
            The number of synapses
        :param source:
            The source of stimulation.
            Can be only: hocwrappers.NetStim, hocwrappers.VecStim, Seg or None.
            If None it will create NetConn with no source, which can be use as external event source
        :param mod_name:
            The name of the Point Process to load
        :param secs:
            Sections over which synapses will be randomly distributed
        :param netcon_weight:
            Weight of the connection (the unit depends of the mod mechanism, but in
            most cases it is uS
        :param delay:
            Delay of the synapse in ms (between the pre-synaptic stimulation and the effect on
            the post-synaptic cell)
        :param threshold:
            The threshold of the synapse in mV. If it pass the associated netcon emits event that
            there was a spike. It may be use for spike detection in axonal compartment to detect
            that cell spiked, but in the case of regular synapse it is mostly irrelevant.
        :param tag:
            String tag name added to the synapse to easily search for similar synapses
        :param uniform_by:
            string. How to uniformly draw sections:
                'lenght' - draw by section lenght
                'sec' - draw by section on the list (choose of each section has equal probability)
                        after that loc on the selected section will be also uniformly draw
                        between 0 and 1.
        :param synaptic_params:
            Additional parameters of the synapse related to the mod mechanism
        :return:
            A list of added synapses
        """
        results = []

        if uniform_by == 'sec':
            locs = np.random.rand(number)
            idxs = np.random.randint(low=0, high=len(secs), size=number)
            for si, loc in zip(idxs, locs):
                seg = secs[si](loc)
                r = self.add_synapse(source=source, mod_name=mod_name, seg=seg,
                                     netcon_weight=netcon_weight, delay=delay,
                                     threshold=threshold, tag=tag, **synaptic_params)
                results.append(r)

        elif uniform_by == 'lenght':
            max_l = int(sum([s.hoc.L for s in secs]))
            locations = np.random.rand(number)
            locations *= max_l

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
        else:
            raise ValueError("Wrong type of uniform_by. It can be: lenght or sec.")

        return results

    def add_random_centroid_normal_dist_synapses(self, number, source, mod_name: str, centroid: Seg,
                                                 std: float, secs: List[Sec] = None,
                                                 netcon_weight=1, delay=1, threshold=10, tag: str = None,
                                                 **synaptic_params):
        """
        Add synapses with random normal distribution around the centroid section.

        :param number:
            The number of synapses
        :param centroid:
            The segment around which points will be randomly generated
        :param std:
            The standard deviation for the normal distribution (in um)
        :param secs:
            Sections over which synapses will be randomly distributed. If None it will use all
            sectons available
        :param source:
            The source of stimulation.
            Can be only: hocwrappers.NetStim, hocwrappers.VecStim, Seg or None.
            If None it will create NetConn with no source, which can be use as external event source
        :param mod_name:
            The name of the Point Process to load
        :param netcon_weight:
            Weight of the connection (the unit depends of the mod mechanism, but in
            most cases it is uS
        :param delay:
            Delay of the synapse in ms (between the pre-synaptic stimulation and the effect on
            the post-synaptic cell)
        :param threshold:
            The threshold of the synapse in mV. If it pass the associated netcon emits event that
            there was a spike. It may be use for spike detection in axonal compartment to detect
            that cell spiked, but in the case of regular synapse it is mostly irrelevant.
        :param tag:
            String tag name added to the synapse to easily search for similar synapses
        :param synaptic_params:
            Additional parameters of the synapse related to the mod mechanism
        :return:
            A list of added synapses
        """

        if secs is None:
            secs = self.secs
        segs = [seg for sec in secs for seg in sec.segs if seg.area > 0]
        dists_seg_ids = [(h.distance(centroid.hoc, seg.hoc), segi) for segi, seg in enumerate(segs)]
        dists_seg_ids = sorted(dists_seg_ids, key=lambda d: d[0])
        dists = [d[0] for d in dists_seg_ids]

        locations = np.abs(np.random.normal(loc=0, scale=std, size=number*100))
        locations = np.array([l for l in locations if min(dists) <= l <= max(dists)])[:number]

        results = []
        for l in locations:
            seg = None
            min_diff = np.inf

            for dst, seg_i in dists_seg_ids:
                diff = abs(l - dst)
                if diff < min_diff:
                    min_diff = diff
                    seg = segs[seg_i]
                if diff > min_diff:
                    break

            if seg is None:
                raise ValueError("Couldn't file the nearest segment.")

            r = self.add_synapse(source=source, mod_name=mod_name, seg=seg,
                                 netcon_weight=netcon_weight, delay=delay,
                                 threshold=threshold, tag=tag, **synaptic_params)
            results.append(r)

        return results

    def _add_raw_synapse(self, source, mod_name, point_process: PointProcess, netcon: NetCon,
                         tag=None):
        """
        Adds raw synapse from existing Point Process and NetCon objects
        """
        syn_name = "%s[%s]" % (point_process.name, self._syn_num[mod_name])
        syn = SingleSynapse(source, point_process=point_process, netcon=netcon,
                            name=syn_name, tag=tag)
        self.syns.append(syn)
        self._syn_num[mod_name] += 1

        return syn
