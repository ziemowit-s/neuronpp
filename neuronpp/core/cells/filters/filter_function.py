import abc


class FilterFunction:
    def __init__(self):
        pass

    @staticmethod
    @abc.abstractmethod
    def filter(obj) -> bool:
        raise NotImplementedError()
