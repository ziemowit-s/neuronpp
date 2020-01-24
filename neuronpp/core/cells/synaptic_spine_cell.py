from neuronpp.core.cells.spine_cell import SpineCell
from neuronpp.core.cells.complex_synaptic_cell import ComplexSynapticCell


class SynapticSpineCell(SpineCell, ComplexSynapticCell):
    def __init__(self, name=None, compile_paths=None):
        ComplexSynapticCell.__init__(self, name, compile_paths=compile_paths)
        SpineCell.__init__(self, name)

    def make_spine_with_synapse(self, source, weight, rand_weight=False, number=1, tag: str = None, mod_name: str = None, delay=0,
                                sec=None, head_nseg=2, neck_nseg=2, source_loc=None, **synaptic_params):
        """

        :param source:
            Can be only: hocwrappers.NetStim, hocwrappers.VecStim, hocwrappers.Sec or None. If it is Sec also loc param need to be defined.
            If None it will create NetConn with no source, which can be use as external event source
        :param weight:
        :param rand_weight:
            if True, will find rand weight [0,1) and multiply this by weight.
        :param number:
        :param tag:
        :param mod_name:
        :param delay:
        :param sec:
        :param head_nseg:
        :param neck_nseg:
        :param source_loc:
        :param synaptic_params:
        :return:
        """

        heads, _ = self.make_spines(spine_number=number, sec=sec, head_nseg=head_nseg, neck_nseg=neck_nseg)

        # loc=1.0 put synase on the top of the spine's head
        syns = self.make_sypanses(source=source, weight=weight, tag=tag, mod_name=mod_name, sec=heads, source_loc=source_loc,
                                  rand_weight=rand_weight, target_loc=1.0, delay=delay, **synaptic_params)
        return syns, heads
