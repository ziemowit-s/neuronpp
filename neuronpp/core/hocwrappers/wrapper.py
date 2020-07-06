

class Wrapper:
    def __init__(self, parent, name):
        try:
            self.parent = parent
        except AttributeError:
            pass
        self.name = name

    def __repr__(self):
        return "{}[{}]".format(self.__class__.__name__, self.name)
