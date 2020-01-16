from neuronpp.core.cells.spine_cell import SpineCell
from neuronpp.core.cells.synaptic_cell import SynapticCell


class SynapticSpineCell(SpineCell, SynapticCell):
    def __init__(self, name=None):
        SynapticCell.__init__(self, name)
        SpineCell.__init__(self, name)

    def make_spine_with_synapse(self, source, weight, spine_number, tag: str = None, mod_name: str = None, delay=0,
                                sec=None, head_nseg=2, neck_nseg=2):
        """

        :param source:
        :param weight:
        :param tag:
        :param mod_name:
        :param delay:
        :param sec:
        :param head_nseg:
        :param neck_nseg:
        :return:
        """
        # loc=1.0 put synase on the top of the spine's head
        heads = self.make_spines(spine_number=spine_number, sec=sec, head_nseg=head_nseg, neck_nseg=neck_nseg)
        syns = self.make_sypanses(source=source, weight=weight, tag=tag, mod_name=mod_name, sec=heads, loc=1.0, delay=delay)
        return syns
