from neuronpp.core.cells.spine_cell import SpineCell
from neuronpp.core.cells.complex_synaptic_cell import ComplexSynapticCell


class SynapticSpineCell(SpineCell, ComplexSynapticCell):
    def __init__(self, name=None):
        ComplexSynapticCell.__init__(self, name)
        SpineCell.__init__(self, name)

    def make_spine_with_synapse(self, source, weight, number=1, tag: str = None, mod_name: str = None, delay=0,
                                sec=None, head_nseg=2, neck_nseg=2, source_loc=None, **synaptic_params):

        heads, _ = self.make_spines(spine_number=number, sec=sec, head_nseg=head_nseg, neck_nseg=neck_nseg)

        # loc=1.0 put synase on the top of the spine's head
        syns = self.make_sypanses(source=source, weight=weight, tag=tag, mod_name=mod_name, sec=heads, source_loc=source_loc,
                                  target_loc=1.0, delay=delay, **synaptic_params)
        return syns, heads
