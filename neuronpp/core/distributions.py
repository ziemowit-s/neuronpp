import numpy as np
from typing import Optional

# ----------------------------------------- DISTS -----------------------------------------


class Dist:
    seed = None

    def __init__(self, dtype="float"):
        self.dtype = dtype

    @classmethod
    def set_seed(cls, seed):
        np.random.seed(seed)
        cls.seed = seed


class TruncatedDist(Dist):
    pass


class UniformDist(Dist):
    def __init__(self, low=0, high=1, dtype="float"):
        Dist.__init__(self, dtype=dtype)
        self.low = low
        self.high = high


class UniformTruncatedDist(UniformDist, TruncatedDist):
    def __init__(self, low=0, high=1, dtype="float"):
        UniformDist.__init__(self, low=low, high=high, dtype=dtype)
        if low < 0:
            raise ValueError("low cannot be < 0 for TruncatedUniformDist.")


class NormalDist(Dist):
    def __init__(self, mean, std, dtype="float"):
        Dist.__init__(self, dtype=dtype)
        self.mean = mean
        self.std = std


class NormalTruncatedDist(NormalDist, TruncatedDist):
    def __init__(self, mean, std, dtype="float"):
        Dist.__init__(self, dtype=dtype)
        if mean < 0 or std < 0:
            raise ValueError("mean and std cannot be < 0 for Truncated Normal Distribution.")
        NormalDist.__init__(self, mean=mean, std=std)


class LogNormalDist(NormalDist):
    def __init__(self, mean, std, dtype="float"):
        NormalDist.__init__(self, mean=mean, std=std, dtype=dtype)


class LogNormalTruncatedDist(LogNormalDist, TruncatedDist):
    def __init__(self, mean, std, dtype="float"):
        Dist.__init__(self, dtype=dtype)
        if mean < 0 or std < 0:
            raise ValueError("mean and std cannot be < 0 for Truncated Normal Distribution.")
        LogNormalDist.__init__(self, mean=mean, std=std)


# ----------------------------------------- SEG DISTS -----------------------------------------


class NormalTruncatedSegDist(NormalTruncatedDist):
    def __init__(self, std, mean: Optional[float] = None):
        """
        Normal distribution for segment choosing.
        Normal means that choosing segments are clustered around mean with standard deviation std.

        :param std:
            Provided in um.
            standard deviation of the cluster of distribution.
        :param mean:
            Provided in normalized arbitrary unit between 0-1.

            Default is None, which means - mean will be selected with random uniform distribution
            from all provided segments. It is used to cluster randomly synapses around this mean
            point and with std spread.

            It is normalized mean (between 0-1), where all provided segments are organized as list
            and first element has location=0 and the last location=1
            During computation this number will be change for appropriate mean in um.
        """
        Dist.__init__(self, dtype="float")

        if mean > 1:
            raise ValueError("Param mean cannot be > 1")
        if mean < 0 or std < 0:
            raise ValueError("mean and std cannot be < 0 for Truncated Normal Distribution.")
        NormalTruncatedDist.__init__(self, mean=mean, std=std)

# ----------------------------------------- CON PROBAS -----------------------------------------


class ConnectionProba(Dist):
    def __init__(self, threshold: float, dtype="float"):
        Dist.__init__(self, dtype=dtype)
        if 0 > threshold > 1:
            raise ValueError("Threshold for connection probability must be between 0 and 1.")
        self.expected = threshold


class UniformConnectionProba(ConnectionProba, UniformDist):
    def __init__(self, threshold: float):
        """
        Defines probability of the occurrence of connection between 2 neurons.

        If the threshold value > Uniform distribution number -> it will return True to the binary
        event.
        
        :param threshold:
            the value which is a threshold.
            If the threshold > Uniform distribution number the event is True. Otherwise False.
        """
        Dist.__init__(self)
        ConnectionProba.__init__(self, threshold=threshold)
        UniformDist.__init__(self, low=0, high=1)


class NormalConnectionProba(ConnectionProba, NormalTruncatedDist):
    def __init__(self, threshold: float, mean: float, std: float):
        """
        Defines probability of the occurrence of connection between 2 neurons.

        Values are obtain from the Truncated Normal Distribution,
        so mean and std cannot be less than 0.

        If the threshold value > Normal distribution number -> it will return True to the binary
        event.

        :param threshold:
            the value which is a threshold.
            If the threshold > Normal distribution number the event is True. Otherwise False.
        :param mean:
            mean of the normal distribution. Must be bewteen 0 and 1.
        :param std:
            standard deviation of the normal distribution. Must be bewteen 0 and 1.
        """
        if 0 > mean > 1:
            raise ValueError("Mean value for connection probability must be between 0 and 1.")
        if 0 > std > 1:
            raise ValueError("Mean value for connection probability must be between 0 and 1.")
        Dist.__init__(self)
        ConnectionProba.__init__(self, threshold=threshold)
        NormalTruncatedDist.__init__(self, mean=mean, std=std)


class LogNormalConnectionProba(NormalConnectionProba):
    def __init__(self, threshold: float, mean: float, std: float):
        """
        Defines probability of the occurrence of binary event.

        If the threshold value > Normal distribution number -> it will return True to the binary
        event.

        :param threshold:
            the value which is a threshold.
            If the threshold > Normal distribution number the event is True. Otherwise False.
        :param mean:
            mean of the normal distribution
        :param std:
            standard deviation of the normal distribution
        """
        NormalConnectionProba.__init__(self, threshold=threshold, mean=mean, std=std)
