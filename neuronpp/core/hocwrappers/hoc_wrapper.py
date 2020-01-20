

class HocWrapper:
    def __init__(self, hoc_obj, parent, name):
        self.hoc = hoc_obj
        self.parent = parent
        self.name = name

    def __repr__(self):
        return "{}+{}+{}".format(self.parent, self.__class__.__name__, self.name)

