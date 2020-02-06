

class Filter:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def add(self, name, value):
        setattr(self, name, value)

    def remove(self, name):
        delattr(self, name)

    def parse(self):
        result = {}
        for k in dir(self):
            result[k] = getattr(self, k)
        return result

