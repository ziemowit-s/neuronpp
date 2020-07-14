from collections import Iterable
from typing import Union, List

from neuronpp.core.cells.core_cell import CoreCell
from neuronpp.core.cells.section_cell import SectionCell
from neuronpp.core.hocwrappers.sec import Sec
from neuronpp.core.hocwrappers.seg import Seg
from neuronpp.core.hocwrappers.netstim import NetStim
from neuronpp.core.hocwrappers.vecstim import VecStim


def check_and_prepare_sources(source):
    """
    Check source type and return source(s) as a list

    :param source:
        single source or list of sources
    :return:
        list of sources based on provided source(s)
    """
    source_ok = True
    if isinstance(source, Iterable):
        if not all([isinstance(s, (Seg, VecStim, NetStim)) for s in source]):
            source_ok = False
    else:
        if source is not None and not isinstance(source, (Seg, VecStim, NetStim)):
            source_ok = False
        else:
            source = [source]

    if not source_ok:
        raise TypeError("Source can be of type: None or List of Seg, VecStim, NetStim or Seg, "
                        "VecStim, NetStim, but provided: %s" % source.__class__)
    return source


def check_and_prepare_target(targ: Union[List[Sec], List[Seg], List[CoreCell], Seg, Sec, CoreCell]):
    target_ok = False
    if isinstance(targ, Iterable):
        if all([isinstance(s, Seg) for s in targ]):
            target_ok = True
        if all([isinstance(s, Sec) for s in targ]):
            target_ok = True
            # remove 0 and 1 ends
            targ = [seg for sec in targ for seg in sec.segs[1:-1]]
        elif all([isinstance(c, SectionCell) for c in targ]):
            target_ok = True
            # remove 0 and 1 ends
            targ = [seg for c in targ for sec in c.secs for seg in sec.segs[1:-1]]
    else:
        if targ is None:
            target_ok = True
        elif isinstance(targ, Seg):
            target_ok = True
            targ = [targ]
        elif isinstance(targ, Sec):
            target_ok = True
            # remove 0 and 1 ends
            targ = [seg for seg in targ.segs[1:-1]]
        elif isinstance(targ, SectionCell):
            target_ok = True
            # remove 0 and 1 ends
            targ = [seg for sec in targ.secs for seg in sec.segs[1:-1]]

    if not target_ok:
        raise TypeError("Target can be an instance or list of: Sec or Cell.")
    return targ
