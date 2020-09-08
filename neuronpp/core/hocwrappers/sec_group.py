from typing import List, Optional

from neuronpp.core.hocwrappers.sec import Sec
from neuronpp.core.decorators import non_removable_fields
from neuronpp.core.hocwrappers.group_hoc_wrapper import GroupHocWrapper


@non_removable_fields("cell")
class SecGroup(GroupHocWrapper):
    def __init__(self, secs: List[Sec], name: str, tag: Optional[str] = None):
        """
        It is a dictionary containing Seg where key is name of the
        Seg of the same type, eg. self["ExpSyn"] = list(syn1, syn2, syn3)

        All synapses in the group need to have a single target

        It not derives from the HocWrapper because HocWrapper is a wrapper for a single HOC object

        :param secs:
            list of Sec.
            All secs need to have the same parent object.
        :param name:
            string name for the group
        :param tag:
            string tag which will be attached to the synaptic group as tag.
            you can filter by this tag
        """
        self.tag = tag
        self.mod_name = '_'.join([s.name for s in secs])
        name = "%s[%s]" % (self.mod_name, name)

        GroupHocWrapper.__init__(self, objs=secs, name=name)
        self.cell = self.parent
