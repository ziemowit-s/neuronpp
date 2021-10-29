import numpy as np

from neuronpp.core.dists.distributions import Dist, UniformDist, NormalDist, TruncatedDist, \
    LogNormalDist


def get_rand(value: Dist):
    if isinstance(value, UniformDist):
        result = np.random.uniform(low=value.low, high=value.high)
    elif isinstance(value, NormalDist):
        result = np.random.normal(loc=value.mean, scale=value.std)
    elif isinstance(value, LogNormalDist):
        result = np.random.lognormal(mean=value.mean, sigma=value.std)
    else:
        raise TypeError("Not allowed value type for Dist: %s" % value)

    if isinstance(value, TruncatedDist):
        result = np.abs(result)
    if "int" in value.dtype.lower():
        result = round(result)

    return result
