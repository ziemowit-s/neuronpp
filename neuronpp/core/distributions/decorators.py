import functools
import numpy as np
from typing import List

from neuronpp.core.distributions.distribution import Dist, UniformDist, NormalDist, TruncatedNormal


def distparams(_func=None, *, exlude: List[str] = None):
    """
    Check numerical parameters if contains Dist object:
      * If so it will take the value from the appropriate distribution and pass it to the function.
      * If the value is numerical type (int, float) it will remain as it is

    By default it will check all parameters of the function. But if are not Dist implementation
     it won't do any changes.
     
    If one of your parameters may be a Dist implementation but you want to handle it by yourself
    pass the name of that param to the exclude list.

    It may only affect numerical types of params (int, float). The other types cannot be affected.
    
    :param _func:
        function which was decorated
    :param exlude:
        a list of excluded params from check if they are a Dist implementation.
    :return:
        the same value as the function decorated
    """
    def _distparams(func):
        @functools.wraps(func)
        def _wrapper_distparams(*args, **kwargs):
            for key, value in kwargs.items():
                if exlude and key in exlude:
                    continue
                if not isinstance(value, Dist):
                    continue

                if isinstance(value, UniformDist):
                    result = np.random.uniform(size=1)[0]
                elif isinstance(value, NormalDist):
                    result = np.random.normal(loc=value.mean, scale=value.std)
                    if isinstance(value, TruncatedNormal):
                        result = np.abs(result)
                else:
                    raise TypeError("Not allowed value type for Dist: %s" % value)

                kwargs[key] = result

            return func(*args, **kwargs)

        return _wrapper_distparams

    if _func is None:
        return _distparams
    else:
        return _distparams(_func)
