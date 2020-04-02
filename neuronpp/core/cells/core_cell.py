import re

from neuronpp.core.cells.filters.filter_function import FilterFunction
from neuronpp.utils.compile_mod import compile_and_load_mods


class CoreCell:

    path_compiled = False

    def __init__(self, name=None, compile_paths=None):
        """
        :param name:
            Name of the cell
        :param compile_paths:
            paths to folders containing mods. Can be list or string separated by spaces.
        """
        if compile_paths:
            compile_and_load_mods(compile_paths)

        if name is None:
            name = ""
        self.name = name

    @staticmethod
    def filter(searchable, obj_filter=None, as_list=False, **kwargs):
        """
        Currently all filter passed are treated as AND statements.

        * Whole object callable function passed to the obj_filter param.
            eg. (lambda expression) returns sections which name contains 'apic' or their distance > 1000 um from the soma:
          ```
           soma = cell.filter_secs("soma")
           cell.filter_secs(obj_filter=lambda o: 'apic' in o.name or h.distance(soma.hoc(0.5), o.hoc(0.5)) > 1000)
          ```

        * Single object field filter based on callable function passed to the obj_filter param.
          eg. (lambda expression) returns sections which parent's name contains less than 10 characters
          ```
          cell.filter_secs(parent=lambda o: len(o.parent.name) < 10)
          ```

        :param searchable:
            is a list or list-like structure where filter will be performed
        :param obj_filter:
            Whole object callable functional filter. If you added also any kwargs they will be together with the
            obj_filter treated as AND statement.
        :param kwargs:
            keys are name of fields in the hoc objects in the particular list
            values are regex patterns to find in those fields
            currently only str fields to filter are supported
        :param as_list:
            If always returns list. Otherwise if filter results in a single object - will return that object not list.
        :return:
            list of hoc objects which match the filter
        """
        def is_regex(pattern):
            return "SRE_Pattern" == pattern.__class__.__name__

        patterns = CoreCell._prepare_patterns(kwargs)
        pat_len = len(patterns)
        if obj_filter:
            pat_len += 1

        filtered = []
        for obj in searchable:
            pat_found = 0

            # If FilterFunction object with filter() function pass
            if obj_filter and obj_filter(obj):
                pat_found += 1

            for attr_name, pat in patterns:

                # Get attribute
                try:
                    value = getattr(obj, attr_name)
                except AttributeError:
                    break

                # Check pattern of the attribute

                # If there is no filter
                if pat is None:
                    pat_found += 1

                # If filter is a callable function (like lambda expression)
                elif callable(pat):
                    if pat(value):
                        pat_found += 1

                # if not - assume value is a string
                else:
                    value = str(value)
                    # If filter is a string
                    if isinstance(pat, str):
                        if pat in value:
                            pat_found += 1
                    # If filter is a regex
                    elif is_regex(pat):
                        if pat.search(value) is not None:
                            pat_found += 1

            # functional AND for all patterns: If all patterns match - add object to the filtered list
            if pat_found == pat_len:
                filtered.append(obj)

        if len(filtered) == 1 and as_list is False:
            filtered = filtered[0]
        return filtered

    @staticmethod
    def _prepare_patterns(kwargs):
        result = []
        for attr_name, v in kwargs.items():

            if v is not None and isinstance(v, str):
                if "regex:" in v:
                    v = v.replace("regex:", "")
                    v = re.compile(v)
                elif "," in v:
                    v = '|'.join(["(%s)" % re.escape(p) for p in v.split(",")])
                    v = re.compile(v)
            result.append((attr_name, v))

        return result

    @staticmethod
    def _is_array_name(name):
        return "[" in name

    def __repr__(self):
        return "{}[{}]".format(self.__class__.__name__, self.name)
