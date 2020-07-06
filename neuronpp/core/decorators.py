import functools
import numpy as np
from typing import List

from neuronpp.core.distributions import Dist, UniformDist, NormalDist, NormalTruncatedDist


def distparams(_func=None, *, exlude: List[str] = None, include: List[str] = None):
    """
    Check numerical parameters if contains Dist object:
      * If so it will take the value from the appropriate distribution and pass it to the function.
      * If the value is numerical type (int, float) it will remain as it is

    By default it will check all parameters of the function. But if are not Dist implementation it
    won't do any changes.

    If one of your parameters may be a Dist implementation but you want to handle it by yourself
    pass the name of that param to the exclude list.

    It may only affect numerical types of params (int, float). The other types cannot be affected.
    :param _func:
        function which have been decorated
    :param exlude:
        Works only if include is not specified. Otherwise ommited.
        a list of excluded params from check if they are a Dist implementation.
    :param include:
        if not specify it will take all params except "exclude".
        if specified - it will only take those params. Exclude won't apply here
    :return:
        the same value as the function decorated
    """
    def _distparams(func):
        @functools.wraps(func)
        def _wrapper_distparams(*args, **kwargs):

            if exlude and not isinstance(exlude, list):
                raise ValueError("Parameter 'exclude' in @distparam decorator must be list or None")
            if include and not isinstance(include, list):
                raise ValueError("Parameter 'include' in @distparam decorator must be list or None")

            for key, value in kwargs.items():
                if include and key in include:
                    pass
                elif not include and exlude and key in exlude:
                    continue
                if isinstance(value, Dist):

                    if isinstance(value, UniformDist):
                        result = np.random.uniform(size=1)[0]
                    elif isinstance(value, NormalDist):
                        result = np.random.normal(loc=value.mean, scale=value.std)

                        if isinstance(value, NormalTruncatedDist):
                            result = np.abs(result)
                    else:
                        raise TypeError("Not allowed value type for Dist: %s" % value)

                    if "int" in value.dtype.lower():
                        result = round(result)

                    kwargs[key] = result

            return func(*args, **kwargs)

        return _wrapper_distparams

    if _func is None:
        return _distparams
    else:
        return _distparams(_func)
