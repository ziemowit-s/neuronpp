from neuronpp.core.filters.filter import Filter


class SectionFilter(Filter):
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name