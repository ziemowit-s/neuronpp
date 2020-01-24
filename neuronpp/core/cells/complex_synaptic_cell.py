from collections import defaultdict

from neuronpp.core.cells.synaptic_cell import SynapticCell

from neuronpp.core.hocwrappers.composed.complex_synapse import ComplexSynapse


class ComplexSynapticCell(SynapticCell):
    def __init__(self, name=None, compile_paths=None):
        SynapticCell.__init__(self, name, compile_paths=compile_paths)
        self.complex_syns = []
        self._syn_num = defaultdict(int)

    def filter_complex_synapses(self, mod_name: str = None, name=None, parent=None, tag=None):
        """
        :param mod_name:
            single string defining name of point process type name, eg. concere synaptic mechanisms like Syn4PAChDa
        :param name:
            start with 'regex:any pattern' to use regular expression. If without 'regex:' - will look which Hoc objects contain the str
        :param source:
            string of source compound name (if source is provided)
        :param point_process:
            string of point process compound name
        :return:
        """
        return self.filter(self.complex_syns, mod_name=mod_name, name=name, parent=parent, tag=tag)

    def group_complex_sypanses(self, tag=None, *synapses):
        """

        :param synapses:
        :param tag:
        :return:
        """
        if isinstance(synapses[0], (list, tuple, set)):
            synapses = [s for syns in synapses for s in syns]
        mod_names = '+'.join([s.mod_name for s in synapses])
        i = self._syn_num[mod_names]
        self._syn_num[mod_names] += 1

        comp_syn = ComplexSynapse(synapses=synapses, name=str(i), tag=tag)
        self.complex_syns.append(comp_syn)

        return comp_syn
