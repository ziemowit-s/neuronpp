import numpy as np


class Dist:
    _seed = None

    def __init__(self, dtype="float"):
        self.dtype = dtype

    @classmethod
    def set_seed(cls, seed):
        if cls._seed:
            raise ValueError("Seed have been already set. Seed can be set once.")
        np.random.seed(seed)
        cls._seed = seed


class UniformDist(Dist):
    def __init__(self, dmin=0, dmax=1, dtype="float"):
        Dist.__init__(self, dtype=dtype)
        self.min = dmin
        self.max = dmax


class NormalDist(Dist):
    def __init__(self, mean, std, dtype="float"):
        Dist.__init__(self, dtype=dtype)
        self.mean = mean
        self.std = std


class NormalTruncatedDist(NormalDist):
    def __init__(self, mean, std, dtype="float"):
        Dist.__init__(self, dtype=dtype)
        if mean <= 0 or std <= 0:
            raise ValueError("mean and std cannot be <= 0 for Truncated Normal Distribution.")
        NormalDist.__init__(self, mean=mean, std=std)


class Proba(Dist):
    def __init__(self, expected=0.5, dtype="float"):
        Dist.__init__(self, dtype=dtype)
        self.expected = expected


class UniformProba(Proba, UniformDist):
    def __init__(self, expected=0.5, dtype="float"):
        Dist.__init__(self, dtype=dtype)
        Proba.__init__(self, expected=expected)
        UniformDist.__init__(self, dmin=0, dmax=1)


class NormalProba(Proba, NormalTruncatedDist):
    def __init__(self, mean=0.5, std=0.1, dtype="float"):
        Dist.__init__(self, dtype=dtype)
        Proba.__init__(self, expected=mean)
        NormalTruncatedDist.__init__(self, mean=mean, std=std)
