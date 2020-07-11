from neuronpp.core.cells.spine_cell import SpineCell
from neuronpp.core.decorators import distparams
from neuronpp.core.cells.synaptic_group_cell import SynapticGroupCell


class SynapticSpineCell(SpineCell, SynapticGroupCell):
    def __init__(self, name=None, compile_paths=None):
        SpineCell.__init__(self, name, compile_paths=compile_paths)
        SynapticGroupCell.__init__(self, name, compile_paths=compile_paths)

    @distparams
    def add_synapses_with_spine(self, source, mod_name: str, segs,
                                netcon_weight=1, delay=0,
                                head_nseg=2, neck_nseg=2, tag: str = None,
                                **synaptic_params):
        """

        :param source:
            Can be only: hocwrappers.NetStim, hocwrappers.VecStim, hocwrappers.Seg or None. If it
             is Sec also loc param need to be defined. If None it will create NetConn with no
             source, which can be use as external event source
        :param netcon_weight:
        :param tag:
        :param mod_name:
        :param delay:
        :param segs:
        :param head_nseg:
        :param neck_nseg:
        :param synaptic_params:
        :return:
        """
        spines = self.add_spines(segs=segs, head_nseg=head_nseg, neck_nseg=neck_nseg)

        syns, heads = self._add_synapses(spines, source, mod_name, netcon_weight, delay, tag,
                                         synaptic_params)
        return syns, heads

    @distparams
    def add_random_synapses_with_spine(self, source, mod_name: str, secs,
                                       netcon_weight=1, number=1, delay=0,
                                       head_nseg=2, neck_nseg=2, tag: str = None,
                                       **synaptic_params):
        """
        :param source:
            Can be only: hocwrappers.NetStim, hocwrappers.VecStim, hocwrappers.Seg or None. If it
             is Sec also loc param need to be defined. If None it will create NetConn with no
             source, which can be use as external event source
        :param netcon_weight:
        :param number:
        :param tag:
        :param mod_name:
        :param delay:
        :param secs:
        :param head_nseg:
        :param neck_nseg:
        :param synaptic_params:
        :return:
        """
        spines = self.add_randuniform_spines(spine_number=number, secs=secs, head_nseg=head_nseg,
                                             neck_nseg=neck_nseg)

        syns, heads = self._add_synapses(spines, source, mod_name, netcon_weight, delay, tag,
                                         synaptic_params)
        return syns, heads

    def _add_synapses(self, spines, source, mod_name: str, netcon_weight, delay, tag,
                      synaptic_params):
        # loc=1.0 put synase on the top of the spine's head
        syns = []
        for s in spines:
            syn = self.add_synapse(source=source, seg=s.head(1.0), mod_name=mod_name,
                                   netcon_weight=netcon_weight, delay=delay, tag=tag,
                                   **synaptic_params)
            syns.append(syn)
        heads = [spine.sections[0] for spine in spines]
        return syns, heads
