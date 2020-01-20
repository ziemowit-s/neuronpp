

class ComposedHocWrapper:
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

    def __repr__(self):
        return "{}+{}+{}".format(self.parent, self.__class__.__name__, self.name)