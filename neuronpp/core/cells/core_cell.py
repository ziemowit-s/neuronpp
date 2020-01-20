import os
import re

import neuron
from neuronpp.utils.compile_mod import CompileMOD


class CoreCell:
    def __init__(self, name=None, compile_paths=None):
        """
        :param name:
            Name of the cell
        :param compile_paths:
            paths to folders containing mods. Can be list or string separated by spaces.
        """
        if compile_paths:
            comp = CompileMOD()
            comp.compile(source_paths=compile_paths, target_path=os.getcwd())

        neuron.load_mechanisms("%s%scompiled" % (os.getcwd(), os.sep))

        if name is None:
            name = ""
        self.name = name

    @staticmethod
    def filter(searchable, **kwargs):
        """
        Currently all patterns in kwargs are treated as AND statements
        :param searchable:
            is a list or list-like structure where filter will be pefrormed

        :param kwargs:
            keys are name of fields in the hoc objects in the particular list
            values are regex patterns to find in those fields
            currently only str fields to filter are supported
        :return:
            list of hoc objects which match the filter
        """
        patterns = []
        for attr_name, v in kwargs.items():
            if v is not None and "regex:" in v:
                v = v.replace("regex:", "")
                v = re.compile(v)
            patterns.append((attr_name, v))
        pat_len = len(patterns)

        result = []
        for hoc_obj in searchable:
            pat_found = 0

            for attr_name, pat in patterns:
                try:
                    attr = getattr(hoc_obj, attr_name)
                except AttributeError:
                    break

                if not isinstance(attr, str):
                    attr = str(attr)

                if pat is None:
                    pat_found += 1
                elif "SRE_Pattern" == pat.__class__.__name__:
                    if pat.search(attr) is not None:
                        pat_found += 1
                elif pat in attr:
                    pat_found += 1

            if pat_found == pat_len:
                result.append(hoc_obj)

        return result

    @staticmethod
    def _is_array_name(name):
        return "[" in name

    def __repr__(self):
        return "{}[{}]".format(self.__class__.__name__, self.name)
