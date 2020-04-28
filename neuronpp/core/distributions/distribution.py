class Dist:
    pass


class AllDist(Dist):
    pass


class OneDist(Dist):
    pass


class UniformDist(Dist):
    def __init__(self, dmin=0, dmax=1):
        self.min = dmin
        self.max = dmax


class NormalDist(Dist):
    def __init__(self, mean, std):
        self.mean = mean
        self.std = std


class TruncatedNormal(NormalDist):
    def __init__(self, mean, std):
        if mean <= 0 or std <= 0:
            raise ValueError("mean and std cannot be <= 0 for Truncated Normal Distribution.")
        NormalDist.__init__(self, mean=mean, std=std)


class Proba(Dist):
    def __init__(self, expected=0.5):
        self.expected = expected


class UniformProba(Proba, UniformDist):
    def __init__(self, expected=0.5):
        Proba.__init__(self, expected=expected)
        UniformDist.__init__(self, dmin=0, dmax=1)


class NormalProba(Proba, TruncatedNormal):
    def __init__(self, expected=0.5, mean=0.5, std=0.1):
        Proba.__init__(self, expected=expected)
        TruncatedNormal.__init__(self, mean=mean, std=std)