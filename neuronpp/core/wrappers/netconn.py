from neuronpp.core.wrappers.hoc import Hoc


class NetConn(Hoc):
    def __init__(self, hoc_obj, name, parent):
        Hoc.__init__(self, hoc_obj=hoc_obj, parent=parent, name=name)