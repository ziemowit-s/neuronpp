from collections import Iterable

from neuronpp.core.hocwrappers.netstim import NetStim
from neuronpp.core.hocwrappers.seg import Seg
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


def check_and_prepare_target(target):
    target_ok = True
    if isinstance(target, Iterable):
        check = [isinstance(s, Seg) for s in target]
        if not all(check):
            target_ok = False
    else:
        if target is not None and not isinstance(target, Seg):
            target_ok = False
        else:
            target = [target]

    if not target_ok:
        raise TypeError("Target can be of type: None or Seg or List[Seg], but provided: %s"
                        % target.__class__)
    return target
