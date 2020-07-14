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


def check_and_prepare_target(target: Union[List[Sec], Sec, List[Seg], Seg, List[CoreCell], CoreCell]):
    target_ok = False
    if isinstance(target, Iterable):
        if all([isinstance(s, Sec) for s in target]):
            target_ok = True
        elif all([isinstance(c, SectionCell) for c in target]):
            target_ok = True
    else:
        if target is None:
            target_ok = True
        elif isinstance(target, Seg):
            target_ok = True
        elif isinstance(target, Sec):
            target_ok = True
        elif isinstance(target, SectionCell):
            target_ok = True
            target = target.secs

    if not target_ok:
        raise TypeError("Target can be an instance or list of: Sec or Cell.")
    return target
