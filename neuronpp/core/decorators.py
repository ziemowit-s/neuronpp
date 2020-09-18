import functools
import inspect

import numpy as np
from typing import List, cast

from neuronpp.core.distributions import Dist, UniformDist, NormalDist, NormalTruncatedDist, \
    TruncatedDist, LogNormalDist
from neuronpp.core.neuron_removable import NON_REMOVABLE_FIELD_NAME


def non_removable_fields(*fields):
    """
    Class decorator for objects which implements NeuronRemovable.

    By default calling remove_immediate_from_neuron() method or deleting object will remove all its
    fields (attributes) of the object, however by decorating class with @non_removable_field()
    you can specify fields not to remove:

    eg. if you don't want to remove fields of cell in MySec object add on top of the class:

        @non_removable_field("cell")
        class MySec(NeuronRemovable):
            ...

    :param fields:
        list of strings defining names of class fields which you don't want to remove during
        remove_immediate_from_neuron() call or del
    """
    def decorate(cls):
        if not inspect.isclass(cls):
            raise ValueError("Decorator non_removable_field can decorate only a class not "
                             "a function.")

        if not hasattr(cls, NON_REMOVABLE_FIELD_NAME):
            setattr(cls, NON_REMOVABLE_FIELD_NAME, [])

        non_removable_list = getattr(cls, NON_REMOVABLE_FIELD_NAME)
        for field in fields:
            if not isinstance(field, str):
                raise TypeError("Field name passed to @non_removable_fields must be string.")
            if field not in non_removable_list:
                non_removable_list.append(field)
        return cls
    return decorate


def distparams(_func=None, *, exclude: List[str] = None, include: List[str] = None):
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
    :param exclude:
        Works only if include is not specified. Otherwise omitted.
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

            if exclude and not isinstance(exclude, list):
                raise ValueError("Parameter 'exclude' in @distparam decorator must be list or None")
            if include and not isinstance(include, list):
                raise ValueError("Parameter 'include' in @distparam decorator must be list or None")

            for key, value in kwargs.items():
                if include and key in include:
                    pass
                elif not include and exclude and key in exclude:
                    continue
                if isinstance(value, Dist):

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

                    kwargs[key] = result

            return func(*args, **kwargs)

        return _wrapper_distparams

    if _func is None:
        return _distparams
    else:
        return _distparams(_func)
